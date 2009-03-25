#!/usr/bin/env python

# lswww v2.1.5 - A web spider library
# Copyright (C) 2006 Nicolas Surribas
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
import re
import socket
import getopt
import os
import HTMLParser
import urllib
import urllib2
import httplib2
from htmlentitydefs import name2codepoint as n2cp
from xml.dom import minidom

try:
	import cookielib
except ImportError:
	cookielibhere = 0
else:
	cookielibhere = 1

try:
	import tidy
except ImportError:
	tidyhere = 0
else:
	tidyhere = 1

try:
	import BeautifulSoup
except ImportError:
	BeautifulSouphere = 0
else:
	BeautifulSouphere = 1

class lswww:
  """
	lswww explore a website and extract links and forms fields.

Usage: python lswww.py http://server.com/base/url/ [options]

Supported options are:
-s <url>
--start <url>
	To specify an url to start with

-x <url>
--exclude <url>
	To exclude an url from the scan (for example logout scripts)
	You can also use a wildcard (*)
	Exemple : -x "http://server/base/?page=*&module=test"
	or -x http://server/base/admin/* to exclude a directory

-p <url_proxy>
--proxy <url_proxy>
	To specify a proxy
	Exemple: -p http://proxy:port/

-c <cookie_file>
--cookie <cookie_file>
	To use a cookie

-a <login%password>
--auth <login%password>
	Set credentials for HTTP authentication
	Doesn't work with Python 2.4

-r <parameter_name>
--remove <parameter_name>
	Remove a parameter from URLs

-v <level>
--verbose <level>
	Set verbosity level
	0: only print results
	1: print a dot for each url found (default)
	2: print each url

-t <timeout>
--timeout <timeout>
	Set the timeout (in seconds)

-n <limit>
--nice <limit>
  Define a limit of urls to read with the same pattern
  Use this option to prevent endless loops
  Must be greater than 0

-h
--help
	To print this usage message
  """

  root = ""
  server = ""
  tobrowse = []
  browsed = []
  proxy = ""
  excluded = []
  forms = []
  uploads = []
  allowed = ['php', 'html', 'htm', 'xml', 'xhtml', 'xht', 'xhtm',
            'asp', 'aspx', 'php3', 'php4', 'php5', 'txt', 'shtm',
            'shtml', 'phtm', 'phtml', 'jhtml', 'pl', 'jsp', 'cfm', 'cfml']
  verbose = 0
  cookie = ""
  auth_basic = []
  bad_params = []
  timeout = 6
  h = None
  global_headers = {}

  # 0 means no limits
  nice = 0

  def __init__(self, rooturl):
    root = rooturl
    if root[-1] != "/":
      root += "/"
    if(self.__checklink(root)):
      print "Invalid link argument"
      sys.exit(0)

    server = (root.split("://")[1]).split("/")[0]
    self.root = root
    self.server = server

    self.tobrowse.append(root)

  def setTimeOut(self, timeout = 6):
    """Set the timeout in seconds to wait for a page"""
    self.timeout = timeout

  def setProxy(self, proxy = ""):
    """Set proxy preferences"""
    self.proxy = proxy

  def setNice(self, nice=0):
    """Set the maximum of urls to visit with the same pattern"""
    self.nice = nice

  def addStartURL(self, url):
    if(self.__checklink(url)):
      print "Invalid link argument:", url
      sys.exit(0)
    if(self.__inzone(url) == 0):
      self.tobrowse.append(url)

  def addExcludedURL(self, url):
    """Add an url to the list of forbidden urls"""
    self.excluded.append(url)

  def setCookieFile(self, cookie):
    """Set the file to read the cookie from"""
    self.cookie = cookie

  def setAuthCredentials(self, auth_basic):
    self.auth_basic = auth_basic

  def addBadParam(self, bad_param):
    self.bad_params.append(bad_param)

  def browse(self, url):
    """Extract urls from a webpage and add them to the list of urls to browse if they aren't in the exclusion list"""
    # We don't need destination anchors
    current = url.split("#")[0]
    # Url without query string
    current = current.split("?")[0]
    # Get the dirname of the file
    currentdir = "/".join(current.split("/")[:-1])+"/"

    # Timeout must not be too long to block big documents (for exemple a download script)
    # and not too short to give good results
    socket.setdefaulttimeout(self.timeout)

    try:
      info, data = self.h.request(url, headers = self.global_headers)
    except socket.timeout:
      self.excluded.append(url)
      return 0

    code = info['status']

    proto = url.split("://")[0]
    if proto == "http" or proto == "https":
      # Check the content-type first
      #if not u.info().get("Content-Type"):
      if not info.has_key("content-type"):
        # Sometimes there's no content-type... so we rely on the document extension
        if (current.split(".")[-1] not in self.allowed) and current[-1] != "/":
          return 1
      elif info["content-type"].find("text") == -1:
        return 1
    # Manage redirections
    #if u.headers.dict.has_key("location"):
    if info.has_key("location"):
      redir = self.correctlink(info["location"], current, currentdir, proto)
      if redir != None:
        if(self.__inzone(redir) == 0):
          # Is the document already visited of forbidden ?
          if (redir in self.browsed) or (redir in self.tobrowse) or \
              self.isExcluded(redir):
            pass
          else:
            # No -> Will browse it soon
            self.tobrowse.append(redir)

    htmlSource = data
    p = linkParser(url)
    try:
      p.feed(htmlSource)
    except HTMLParser.HTMLParseError, err:
      if tidyhere == 1:
        options = dict(output_xhtml = 1, add_xml_decl = 1,
            indent = 1, tidy_mark = 0)
        htmlSource = str(tidy.parseString(htmlSource, **options))
        try:
          p.reset()
          p.feed(htmlSource)
        except HTMLParser.HTMLParseError, err:
          pass
      elif BeautifulSouphere == 1:
        htmlSource = BeautifulSoup.BeautifulSoup(htmlSource).prettify()
        try:
          p.reset()
          p.feed(htmlSource)
        except HTMLParser.HTMLParseError, err:
          p = linkParser2(url, self.verbose)
          p.feed(htmlSource)
      # last chance
      else:
        p = linkParser2(url, self.verbose)
        p.feed(htmlSource)

    for lien in p.uploads:
      self.uploads.append(self.correctlink(lien, current, currentdir, proto))
    for lien in p.liens:
      lien = self.correctlink(lien, current, currentdir, proto)
      if lien != None:
        if(self.__inzone(lien) == 0):
          # Is the document already visited of forbidden ?
          if (lien in self.browsed) or (lien in self.tobrowse) or self.isExcluded(lien):
            pass
          elif self.nice>0:
            if self.__countMatches(lien) >= self.nice:
              # don't waste time next time we found it
              self.excluded.append(lien)
              return 0
            else:
              self.tobrowse.append(lien)
          else:
            # No -> Will browse it soon
            self.tobrowse.append(lien)
    for form in p.forms:
      action = self.correctlink(form[0], current, currentdir, proto)
      if action == None: action = current
      form = (action, form[1], url)
      if form not in self.forms: self.forms.append(form)
    # We automaticaly exclude 404 urls
    if code == 404:
      self.excluded.append(url)
      return 0
    return 1


  def correctlink(self, lien, current, currentdir, proto):
    """Transform relatives urls in absolutes ones"""
    # No leading or trailing whitespaces
    lien = lien.strip()
    if lien == "..":
      lien = "../"
    # bad protocols
    llien = lien.lower()
    if llien.find("telnet:", 0) == 0 or llien.find("ftp:", 0) == 0 or \
    llien.find("mailto:", 0) == 0 or llien.find("javascript:", 0) == 0 or \
    llien.find("news:", 0) == 0 or llien.find("file:", 0) == 0 or \
    llien.find("gopher:", 0) == 0 or llien.find("irc:", 0) == 0 or lien == "":
      return None
    # Good protocols or relatives links
    else:
      # full url, nothing to do :)
      if (lien.find("http://", 0) == 0) or (lien.find("https://", 0) == 0):
        pass
      else:
        # root-url related link
        if(lien[0] == '/'):
          lien = proto+"://"+self.server+lien
        else:
          # same page + query string
          if(lien[0] == '?'):
            lien = current+lien
          # current directory related link
          else:
            lien = currentdir+lien
      # No destination anchor
      if lien.find("#") != -1:
        lien = lien.split("#")[0]
      # reorganize parameters in alphabetical order
      if lien.find("?") != -1:
        args = lien.split("?")[1]
        if args.find("&") != -1 :
          args = args.split("&")
          args.sort()
          args = [i for i in args if i != "" and i.find("=") >= 0]
          for i in self.bad_params:
            for j in args:
              if j.startswith(i+"="): args.remove(j)
          args = "&".join(args)

        # a hack for auto-generated Apache directory index
        if args in ["C=D;O=A", "C=D;O=D", "C=M;O=A", "C=M;O=D",
            "C=N;O=A", "C=N;O=D", "C=S;O=A", "C=S;O=D"]:
          lien = lien.split("?")[0]
        else:
          lien = lien.split("?")[0]+"?"+args
      # Remove the trailing '?' if its presence doesn't make sense
      if lien[-1:] == "?":
        lien = lien[:-1]
      # remove useless slashes
      if lien.find("?") != -1:
        file = lien.split("?")[0]
        file = re.sub("[^:]//+", "/", file)
        lien = file+"?"+lien.split("?")[1]
      # links going to a parrent directory (..)
      while re.search("/([~:!,;a-zA-Z0-9\.\-+_]+)/\.\./", lien) != None:
        lien = re.sub("/([~:!,;a-zA-Z0-9\.\-+_]+)/\.\./", "/", lien)
      lien = re.sub("/\./", "/", lien)
      # Everything is good here
      return lien

  def __checklink(self, url):
    """Verify the protocol"""
    if (url.find("http://", 0) == 0) or (url.find("https://", 0) == 0):
      return 0
    else:
      return 1

  def __inzone(self, url):
    """Make sure the url is under the root url"""
    if(url.find(self.root, 0) == 0):
      return 0
    else:
      return 1

  def isExcluded(self, url):
    """Return True if the url is not allowed to be scan"""
    match = False
    for regexp in self.excluded:
      if self.__reWildcard(regexp, url):
        match = True
    return match
      
  def __countMatches(self, url):
    """Return the number of known urls matching the pattern of the given url"""
    matches = 0
    if url.find("?") != -1:
      if url.find("=") != -1:
        i = 0
        for x in range(0, url.count("=")):
          start = url.find("=", i)
          i = url.find("&", start)
          if i != -1:
            for u in self.browsed:
              if u.startswith(url[:start]+"=") and u.endswith(url[i:]):
                matches += 1
          else:
            for u in self.browsed:
              if u.startswith(url[:start]+"="):
                matches += 1
      else:#QUERY_STRING
        for a in [u for u in self.browsed if u.find("=")<0]:
          if a.startswith(url.split("?")[0]):
            matches += 1
    return matches

  def __reWildcard(self, regexp, string):
    """Wildcard-based regular expression system"""
    regexp = re.sub("\*+", "*", regexp)
    match = True
    if regexp.count("*") == 0:
      if regexp == string:
        return True
      else:
        return False
    blocks = regexp.split("*")
    start = ""
    end = ""
    if not regexp.startswith("*"):
      start = blocks[0]
    if not regexp.endswith("*"):
      end = blocks[-1]
    if start != "":
      if string.startswith(start):
        blocks = blocks[1:]
      else:
        return False
    if end != "":
      if string.endswith(end):
        blocks = blocks[:-1]
      else:
        return False
    blocks = [block for block in blocks if block != ""]
    if blocks == []:
      return match
    for block in blocks:
      i = string.find(block)
      if i == -1: return False
      string = string[i+len(block):]
    return match

  def go(self):
    proxy = None

    if self.proxy != "":
      (proxy_type, proxy_usr, proxy_pwd, proxy_host, proxy_port,
       path, query, fragment) = httplib2.parse_proxy(self.proxy)
      proxy = httplib2.ProxyInfo(proxy_type, proxy_host, proxy_port,
          proxy_user = proxy_usr, proxy_pass = proxy_pwd)

    self.h = httplib2.Http(cache = None, timeout = self.timeout,
                            proxy_info = proxy)

    if self.cookie != "" and cookielibhere == 1:
      cj = cookielib.LWPCookieJar()
      if os.path.isfile(self.cookie):
        cj.load(self.cookie, ignore_discard = True)
        self.global_headers["Cookie"] = "; ".join(cook.name+"="+cook.value for cook in cj)

    if self.auth_basic != []:
      self.h.add_credentials(self.auth_basic[0], self.auth_basic[1])

    # while url list isn't empty, continue browsing
    # if the user stop the scan with Ctrl+C, give him all found urls
    try:
      while len(self.tobrowse)>0:
        lien = self.tobrowse.pop(0)
        if (lien not in self.browsed and lien not in self.excluded):
          if self.browse(lien):
            self.browsed.append(lien)
            if self.verbose == 1:
              sys.stderr.write('.')
            elif self.verbose == 2:
              sys.stderr.write(lien+"\n")
    except KeyboardInterrupt: pass

  def verbosity(self, vb):
    """Set verbosity level"""
    self.verbose = vb

  def printLinks(self):
    """Print found URLs on standard output"""
    self.browsed.sort()
    sys.stderr.write("\n+ URLs :\n")
    for lien in self.browsed:
      print lien

  def printForms(self):
    """Print found forms on standard output"""
    if self.forms != []:
      sys.stderr.write("\n+ Forms Info :\n")
      for form in self.forms:
        print "From:", form[2]
        print "To:", form[0]
        for k, v in form[1].items():
          print "\t"+k, ":", v
        print

  def printUploads(self):
    """Print urls accepting uploads"""
    if self.uploads != []:
      sys.stderr.write("\n+ Upload Scripts :\n")
      for up in self.uploads:
        print up

  def exportXML(self,filename,encoding="UTF-8"):
    "Export the urls and the forms found in an XML file."
    xml = minidom.Document()
    items = xml.createElement("items")
    xml.appendChild(items)

    for lien in self.browsed:
      get = xml.createElement("get")
      get.setAttribute("url", lien)
      items.appendChild(get)

    for form in self.forms:
      post = xml.createElement("post")
      post.setAttribute("url", form[0])
      post.setAttribute("referer", form[2])

      for k, v in form[1].items():
        var = xml.createElement("var")
        var.setAttribute("name", k)
        var.setAttribute("value", v)
        post.appendChild(var)
      items.appendChild(post)

    for up in self.uploads:
      upl = xml.createElement("upload")
      upl.setAttribute("url", up)
      items.appendChild(upl)

    fd = open(filename,"w")
    xml.writexml(fd, "    ", "    ", "\n", encoding)
    fd.close()
 
  def getLinks(self):
    self.browsed.sort()
    return self.browsed

  def getForms(self):
    return self.forms

  def getUploads(self):
    self.uploads.sort()
    return self.uploads
    
class linkParser(HTMLParser.HTMLParser):
  """Extract urls in 'a' href HTML tags"""
  def __init__(self, url = ""):
    HTMLParser.HTMLParser.__init__(self)
    self.liens = []
    self.forms = []
    self.form_values = {}
    self.inform = 0
    self.current_form_url = url
    self.uploads = []
    self.current_form_method = "get"
    self.url = url

  def handle_starttag(self, tag, attrs):
    tmpdict = {}
    val = None
    for k, v in dict(attrs).items():
      tmpdict[k.lower()] = v
    if tag.lower() == 'a':
      if "href" in tmpdict.keys():
        self.liens.append(tmpdict['href'])

    if tag.lower() == 'form':
      self.inform = 1
      self.form_values = {}
      self.current_form_url = self.url
      if "action" in tmpdict.keys():
        self.liens.append(tmpdict['action'])
        self.current_form_url = tmpdict['action']

      # Forms use GET method by default
      self.current_form_method = "get"
      if "method" in tmpdict.keys():
        if tmpdict["method"].lower() == "post":
          self.current_form_method = "post"

    if tag.lower() == 'input':
      if self.inform == 1:
        if "type" not in tmpdict.keys():
          tmpdict["type"] = "text"
        if "name" in tmpdict.keys():
          if tmpdict['type'].lower() in ['text', 'password', 'radio',
              'checkbox', 'hidden', 'submit', 'search']:
          # use default value if present or set it to 'on'
            if "value" in tmpdict.keys():
              if tmpdict["value"] != "": val = tmpdict["value"]
              else: val = "on"
            else: val = "on"
            self.form_values.update(dict([(tmpdict['name'], val)]))
          if tmpdict['type'].lower() == "file":
            self.uploads.append(self.current_form_url)

    if tag.lower() in ["textarea", "select"]:
      if self.inform == 1:
        if "name" in tmpdict.keys():
          self.form_values.update(dict([(tmpdict['name'], 'on')]))

    if tag.lower() in ["frame", "iframe"]:
      if "src" in tmpdict.keys():
        self.liens.append(tmpdict['src'])

  def handle_endtag(self, tag):
    if tag.lower() == 'form':
      self.inform = 0
      if self.current_form_method == "post":
        self.forms.append((self.current_form_url, self.form_values))
      else:
        l = ["=".join([k, v]) for k, v in self.form_values.items()]
        l.sort()
        self.liens.append(self.current_form_url.split("?")[0]+"?"+"&".join(l))

class linkParser2():
  verbose = 0
    
  """Extract urls in 'a' href HTML tags"""
  def __init__(self, url = "", verb = 0):
    self.liens = []
    self.forms = []
    self.form_values = {}
    self.inform = 0
    self.current_form_url = ""
    self.uploads = []
    self.current_form_method = "get"
    self.verbose = verb

  def __findTagAttributes(self, tag):
    attDouble = re.findall('<\w*[ ]| *(.*?)[ ]*=[ ]*"(.*?)"[ +|>]', tag)
    attSingle = re.findall('<\w*[ ]| *(.*?)[ ]*=[ ]*\'(.*?)\'[ +|>]', tag)
    attNone   = re.findall('<\w*[ ]| *(.*?)[ ]*=[ ]*["|\']?(.*?)["|\']?[ +|>]', tag)
    attNone.extend(attSingle)
    attNone.extend(attDouble)
    return attNone

  def feed(self, htmlSource):
    htmlSource = htmlSource.replace("\n", "")
    htmlSource = htmlSource.replace("\r", "")
    htmlSource = htmlSource.replace("\t", "")

    links = re.findall('<a.*?>', htmlSource)
    linkAttributes = []
    for link in links:
      linkAttributes.append(self.__findTagAttributes(link))

    #Finding all the forms: getting the text from "<form..." to "...</form>"
    #the array forms will contain all the forms of the page
    forms = re.findall('<form.*?>.*?</form>', htmlSource)
    formsAttributes = []
    for form in forms:
      formsAttributes.append(self.__findTagAttributes(form))

    #Processing the forms, obtaining the method and all the inputs
    #Also finding the method of the forms
    inputsInForms    = []
    textAreasInForms = []
    selectsInForms   = []
    for form in forms:
      inputsInForms   .append(re.findall('<input.*?>', form))
      textAreasInForms.append(re.findall('<textarea.*?>', form))
      selectsInForms  .append(re.findall('<select.*?>', form))

    #Extracting the attributes of the <input> tag as XML parser
    inputsAttributes = []
    for i in range(len(inputsInForms)):
      inputsAttributes.append([])
      for inputt in inputsInForms[i]:
        inputsAttributes[i].append(self.__findTagAttributes(inputt))

    selectsAttributes = []
    for i in range(len(selectsInForms)):
      selectsAttributes.append([])
      for select in selectsInForms[i]:
        selectsAttributes[i].append(self.__findTagAttributes(select))

    textAreasAttributes = []
    for i in range(len(textAreasInForms)):
      textAreasAttributes.append([])
      for textArea in textAreasInForms[i]:
        textAreasAttributes[i].append(self.__findTagAttributes(textArea))

    if(self.verbose == 3):
      print "\n\nForms"
      print "====="
      for i in range(len(forms)):
        print "Form "+str(i)
        tmpdict = {}
        for k, v in dict(formsAttributes[i]).items():
          tmpdict[k.lower()] = v
        print " * Method:  "+self.__decode_htmlentities(tmpdict['action'])
        print " * Intputs: "
        for j in range(len(inputsInForms[i])):
          print "    + "+inputsInForms[i][j]
          for att in inputsAttributes[i][j]:
            print "       - "+str(att)
        print " * Selects: "
        for j in range(len(selectsInForms[i])):
          print "    + "+selectsInForms[i][j]
          for att in selectsAttributes[i][j]:
            print "       - "+str(att)
        print " * TextAreas: "
        for j in range(len(textAreasInForms[i])):
          print "    + "+textAreasInForms[i][j]
          for att in textAreasAttributes[i][j]:
            print "       - "+str(att)
      print "\nURLS"
      print "===="

    for i in range(len(links)):
      tmpdict = {}
      for k, v in dict(linkAttributes[i]).items():
        tmpdict[k.lower()] = v
      if "href" in tmpdict.keys():
        self.liens.append(self.__decode_htmlentities(tmpdict['href']))
        if(self.verbose == 3):
          print self.__decode_htmlentities(tmpdict['href'])

    for i in range(len(forms)):
      tmpdict = {}
      for k, v in dict(formsAttributes[i]).items():
        tmpdict[k.lower()] = v
      self.form_values = {}
      if "action" in tmpdict.keys():
        self.liens.append(self.__decode_htmlentities(tmpdict['action']))
        self.current_form_url = self.__decode_htmlentities(tmpdict['action'])

      # Forms use GET method by default
      self.current_form_method = "get"
      if "method" in tmpdict.keys():
        if tmpdict["method"].lower() == "post":
          self.current_form_method = "post"

      for j in range(len(inputsAttributes[i])):
        tmpdict = {}
        for k, v in dict(inputsAttributes[i][j]).items():
          tmpdict[k.lower()] = v
          if "type" not in tmpdict.keys():
            tmpdict["type"] = "text"
          if "name" in tmpdict.keys():
            if tmpdict['type'].lower() in \
              ['text', 'password', 'radio', 'checkbox', 'hidden',
                  'submit', 'search']:
              # use default value if present or set it to 'on'
              if "value" in tmpdict.keys():
                if tmpdict["value"] != "": val = tmpdict["value"]
                else: val = "on"
              else: val = "on"
              self.form_values.update(dict([(tmpdict['name'], val)]))
            if tmpdict['type'].lower() == "file":
              self.uploads.append(self.current_form_url)

      for j in range(len(textAreasAttributes[i])):
        tmpdict = {}
        for k, v in dict(textAreasAttributes[i][j]).items():
          tmpdict[k.lower()] = v
        if "name" in tmpdict.keys():
          self.form_values.update(dict([(tmpdict['name'], 'on')]))

      for j in range(len(selectsAttributes[i])):
        tmpdict = {}
        for k, v in dict(selectsAttributes[i][j]).items():
          tmpdict[k.lower()] = v
        if "name" in tmpdict.keys():
          self.form_values.update(dict([(tmpdict['name'], 'on')]))

      if self.current_form_method == "post":
        self.forms.append((self.current_form_url, self.form_values))
      else:
        l = ["=".join([k, v]) for k, v in self.form_values.items()]
        l.sort()
        self.liens.append(self.current_form_url.split("?")[0]+"?"+"&".join(l))

  def __substitute_entity(self, match):
    ent = match.group(2)
    if match.group(1) == "#":
      return unichr(int(ent))
    else:
      cp = n2cp.get(ent)

      if cp:
        return unichr(cp)
      else:
        return match.group()

  def __decode_htmlentities(self, string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(self.__substitute_entity, string)[0]

if __name__ == "__main__":
  try:
    prox = ""
    auth = []
    xmloutput = ""

    if len(sys.argv)<2:
      print lswww.__doc__
      sys.exit(0)
    if '-h' in sys.argv or '--help' in sys.argv:
      print lswww.__doc__
      sys.exit(0)
    myls = lswww(sys.argv[1])
    myls.verbosity(1)
    try:
      opts, args = getopt.getopt(sys.argv[2:], "hp:s:x:c:a:r:v:t:n:e:",
          ["help", "proxy=", "start=", "exclude=", "cookie=", "auth=",
            "remove=", "verbose=", "timeout=", "nice=", "export="])
    except getopt.GetoptError, e:
      print e
      sys.exit(2)
    for o, a in opts:
      if o in ("-h", "--help"):
        print lswww.__doc__
        sys.exit(0)
      if o in ("-s", "--start"):
        if (a.find("http://", 0) == 0) or (a.find("https://", 0) == 0):
          myls.addStartURL(a)
      if o in ("-x", "--exclude"):
        if (a.find("http://", 0) == 0) or (a.find("https://", 0) == 0):
          myls.addExcludedURL(a)
      if o in ("-p", "--proxy"):
          myls.setProxy(a)
      if o in ("-c", "--cookie"):
        myls.setCookieFile(a)
      if o in ("-r", "--remove"):
        myls.addBadParam(a)
      if o in ("-a", "--auth"):
        if a.find("%") >= 0:
          auth = [a.split("%")[0], a.split("%")[1]]
          myls.setAuthCredentials(auth)
      if o in ("-v", "--verbose"):
        if str.isdigit(a):
          myls.verbosity(int(a))
      if o in ("-t", "--timeout"):
        if str.isdigit(a):
          myls.setTimeOut(int(a))
      if o in ("-n", "--nice"):
        if str.isdigit(a):
          myls.setNice(int(a))
      if o in ("-e", "--export"):
        xmloutput = a

    myls.go()
    myls.printLinks()
    myls.printForms()
    myls.printUploads()
    if xmloutput != "":
      myls.exportXML(xmloutput)
  except SystemExit:
    pass