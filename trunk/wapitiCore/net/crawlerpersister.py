#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Wapiti project (http://wapiti.sourceforge.net)
# Copyright (C) 2009-2014 Nicolas Surribas
#
# Original authors :
# David del Pozo
# Alberto Pastor
# Copyright (C) 2008 Informatica Gesfor
# ICT Romulus (http://www.ict-romulus.eu)
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
import os
from xml.parsers import expat
from xml.dom.minidom import Document
from urllib import quote, unquote
from wapitiCore.net import HTTP


class CrawlerPersister(object):
    """
    This class makes the persistence tasks for persisting the crawler parameters
    in other to can continue the process in the future.
    """

    CRAWLER_DATA_DIR_NAME = "scans"
    HOME_DIR = os.getenv('HOME') or os.getenv('USERPROFILE')
    BASE_DIR = os.path.join(HOME_DIR, ".wapiti")
    CRAWLER_DATA_DIR = os.path.join(BASE_DIR, CRAWLER_DATA_DIR_NAME)

    ROOT_URL = "rootURL"
    TO_BROWSE = "toBrowse"
    BROWSED = "browsed"
    RESOURCE = "resource"
    METHOD = "method"
    PATH = "path"
    INPUT = "input"
    INPUT_NAME = "name"
    INPUT_VALUE = "value"
    HEADERS = "headers"
    HEADER = "header"
    HEADER_NAME = "name"
    HEADER_VALUE = "value"
    ENCODING = "encoding"
    REFERER = "referer"
    GET_PARAMS = "get_params"
    POST_PARAMS = "post_params"
    FILE_PARAMS = "file_params"

    def __init__(self):
        # toBrowse can contain GET and POST resources
        self.to_browse = []
        # browsed contains only GET resources
        self.browsed_links = []
        # forms contains only POST resources
        self.browsed_forms = []
        self.uploads = []
        self.headers = {}
        self.root_url = ""

        self.tag = ""
        self.array = None

        self.method = ""
        self.path = ""
        self.encoding = ""
        self.referer = ""
        self.get_params = []
        self.post_params = []
        self.file_params = []

        self._parser = expat.ParserCreate("UTF-8")

    @staticmethod
    def isDataForUrl(filename):
        return os.path.exists(filename)

    def saveXML(self, filename):
        """
        Exports the crawler parameters to an XML file.
        @param filename The file where is loaded the crawler data
        """
        xml = Document()
        root = xml.createElement("root")
        xml.appendChild(root)

        root_url_element = xml.createElement(self.ROOT_URL)
        root_url_element.appendChild(xml.createTextNode(self.root_url.url))
        root.appendChild(root_url_element)

        # 1 - URLs and FORMs not yet browsed
        # we don't know several informations yet like the response headers
        to_browse_element = xml.createElement(self.TO_BROWSE)
        for http_resource in self.to_browse:
            # <resource method="" path="" encoding ="">
            resource_element = xml.createElement(self.RESOURCE)
            resource_element.setAttribute(self.METHOD, http_resource.method)
            resource_element.setAttribute(self.PATH, http_resource.path)
            resource_element.setAttribute(self.ENCODING, http_resource.encoding)
            #   <referer>
            referer_element = xml.createElement(self.REFERER)
            referer_element.appendChild(xml.createTextNode(http_resource.referer))
            resource_element.appendChild(referer_element)
            #   <get_params>
            get_params_element = xml.createElement(self.GET_PARAMS)
            for k, v in http_resource.get_params:
                input_element = xml.createElement(self.INPUT)
                input_element.setAttribute(self.INPUT_NAME, quote(k))
                if v is not None:
                    input_element.setAttribute(self.INPUT_VALUE, quote(v))
                get_params_element.appendChild(input_element)
            resource_element.appendChild(get_params_element)

            #   <post_params>
            post_params_element = xml.createElement(self.POST_PARAMS)
            for k, v in http_resource.post_params:
                input_element = xml.createElement(self.INPUT)
                input_element.setAttribute(self.INPUT_NAME, quote(k))
                input_element.setAttribute(self.INPUT_VALUE, quote(v))
                post_params_element.appendChild(input_element)
            resource_element.appendChild(post_params_element)

            #   <file_params>
            file_params_element = xml.createElement(self.FILE_PARAMS)
            for k, v in http_resource.file_params:
                input_element = xml.createElement(self.INPUT)
                input_element.setAttribute(self.INPUT_NAME, quote(k))
                input_element.setAttribute(self.INPUT_VALUE, quote(v))
                file_params_element.appendChild(input_element)
            resource_element.appendChild(file_params_element)

            to_browse_element.appendChild(resource_element)
        root.appendChild(to_browse_element)

        # 2 - URLs and FORMs already browsed
        browsed_element = xml.createElement(self.BROWSED)
        for http_resource in self.browsed_links + self.browsed_forms:
            # <resource method="" path="" encoding ="">
            resource_element = xml.createElement(self.RESOURCE)
            resource_element.setAttribute(self.METHOD, http_resource.method)
            resource_element.setAttribute(self.PATH, http_resource.path)
            resource_element.setAttribute(self.ENCODING, http_resource.encoding)
            #   <referer>
            referer_element = xml.createElement(self.REFERER)
            referer_element.appendChild(xml.createTextNode(http_resource.referer))
            resource_element.appendChild(referer_element)
            #   <get_params>
            get_params_element = xml.createElement(self.GET_PARAMS)
            for k, v in http_resource.get_params:
                input_element = xml.createElement(self.INPUT)
                input_element.setAttribute(self.INPUT_NAME, quote(k))
                if v is not None:
                    input_element.setAttribute(self.INPUT_VALUE, quote(v))
                get_params_element.appendChild(input_element)
            resource_element.appendChild(get_params_element)

            #   <post_params>
            post_params_element = xml.createElement(self.POST_PARAMS)
            for k, v in http_resource.post_params:
                input_element = xml.createElement(self.INPUT)
                input_element.setAttribute(self.INPUT_NAME, quote(k))
                input_element.setAttribute(self.INPUT_VALUE, quote(v))
                post_params_element.appendChild(input_element)
            resource_element.appendChild(post_params_element)

            #   <file_params>
            file_params_element = xml.createElement(self.FILE_PARAMS)
            for k, v in http_resource.file_params:
                input_element = xml.createElement(self.INPUT)
                input_element.setAttribute(self.INPUT_NAME, quote(k))
                input_element.setAttribute(self.INPUT_VALUE, quote(v[0]))
                file_params_element.appendChild(input_element)
            resource_element.appendChild(file_params_element)

            #   <headers>
            headers_element = xml.createElement(self.HEADERS)
            for k, v in http_resource.headers.items():
                if v is None:
                    v = ""
                header_element = xml.createElement(self.HEADER)
                header_element.setAttribute(self.HEADER_NAME, k)
                header_element.setAttribute(self.HEADER_VALUE, v)
                headers_element.appendChild(header_element)
            resource_element.appendChild(headers_element)

            browsed_element.appendChild(resource_element)
        root.appendChild(browsed_element)

        f = open(filename, "w")
        try:
                xml.writexml(f, "    ", "    ", "\n", "UTF-8")
        finally:
                f.close()

    def loadXML(self, filename):
        """
        Loads the crawler parameters from an XML file.
        @param filename The file from where is loaded the crawler data
        """
        self._parser.StartElementHandler = self.__start_element
        self._parser.EndElementHandler = self.__end_element
        self._parser.CharacterDataHandler = self.__char_data
        self._parser.returns_unicode = False

        f = None
        try:
            f = open(filename)
            content = f.read()
            self.__feed(content.replace("\n", ""))
        finally:
            if f is not None:
                f.close()

    def __feed(self, data):
        self._parser.Parse(data, 0)

    def __close(self):
        self._parser.Parse("", 1)
        del self._parser

    def __start_element(self, name, attrs):
        if name == self.TO_BROWSE:
            self.array = self.to_browse

        elif name == self.BROWSED:
            self.array = self.browsed_links

        elif name == self.RESOURCE:
            self.method = attrs[self.METHOD]
            self.path = attrs[self.PATH]
            self.encoding = attrs[self.ENCODING]
            self.referer = ""
            self.headers = {}
            self.get_params = []
            self.post_params = []
            self.file_params = []

        elif name in [self.GET_PARAMS, self.POST_PARAMS, self.FILE_PARAMS, self.REFERER, self.ROOT_URL]:
            self.tag = name

        elif name == self.HEADER:
            self.headers[attrs[self.HEADER_NAME]] = attrs[self.HEADER_VALUE]

        elif name == self.INPUT:
            param_name = unquote(attrs[self.INPUT_NAME])
            if self.INPUT_VALUE in attrs:
                param_value = unquote(attrs[self.INPUT_VALUE])
            else:
                param_value = None

            if self.tag == self.GET_PARAMS:
                self.get_params.append([param_name, param_value])
            if self.tag == self.POST_PARAMS:
                self.post_params.append([param_name, param_value])
            if self.tag == self.FILE_PARAMS:
                self.file_params.append([param_name, [param_value, 'GIF89a', 'image/gif']])

    def __end_element(self, name):
        if name == self.RESOURCE:
            http_res = HTTP.HTTPResource(self.path,
                                         method=self.method,
                                         encoding=self.encoding,
                                         referer=self.referer,
                                         get_params=self.get_params,
                                         post_params=self.post_params,
                                         file_params=self.file_params)
            http_res.setHeaders(self.headers)

            if self.array is self.to_browse:
                self.to_browse.append(http_res)
            else:
                if self.method == "GET":
                    self.browsed_links.append(http_res)
                elif self.method == "POST":
                    self.browsed_forms.append(http_res)

    def __char_data(self, data):
        if self.tag == self.ROOT_URL:
            self.root_url = data.strip(" ")
        elif self.tag == self.REFERER:
            self.referer = data.strip(" ")

    def setRootURL(self, root_url):
        self.root_url = root_url

    def getRootURL(self):
        return self.root_url

    def setToBrose(self, to_browse):
        self.to_browse = to_browse

    def getToBrose(self):
        return self.to_browse

    def setLinks(self, links):
        self.browsed_links = links

    def getLinks(self):
        return self.browsed_links

    def setForms(self, forms):
        self.browsed_forms = forms

    def getForms(self):
        return self.browsed_forms

    def setUploads(self, uploads):
        self.uploads = uploads

    def getUploads(self):
        return self.uploads
