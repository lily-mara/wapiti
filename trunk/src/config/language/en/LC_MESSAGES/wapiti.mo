��    O      �  k         �     �     �     �     �          $     ;  '   T     |     �     �  "   �  %   �          %     E     \     y      ~     �     �     �     �     �     	      !	     B	     `	     i	     w	     �	     �	     �	  
   �	     �	     �	     �	     
     
     
     %
     ?
     ]
  &   d
     �
     �
     �
      �
     �
     �
     �
          *  	   2     <     D     ^  
   r     }     �     �     �     �  #   �     �  	   �  
   �     �  	   �                 	        #  "   (  
   K     V     b  5  n     �     �  �  �     t     �     �     �  '   �                ,  "   @  %   c     �  �   �     �  �   �     j      o  (  �  U   �       �   "  >   �     �    �  H       N     W  �  e  2  /     b     g  
   m     x     �     �     �     �     �     �     �       &        D     I     P  Y  e  `   �         g   .   �   �      N!  	   V!     `!     h!     �!  
   �!     �!     �!     �!     �!     �!  #   �!     �!  	   �!  
   "     "  	   "     %"     1"  �  4"  !  �&     .  !   ".  
   D.     O.     [.     A   (      #           C                 '           )       0   G             E   5          .   1         I           +       &      8              =             D   O   	          -      K      4          9   
             %      <   $           "          !       L   ,       6   F   B       N   3   ?       H   /   :   @             J   *   >      ;          M   7          2                 (QUERY_STRING) (QUERY_STRING) in 500 Error description 500 HTTP Error code 500 HTTP Error code coming from 500 HTTP Error code in 500 HTTP Error code with A report has been generated in the file Attacking forms (POST) Attacking urls (GET) Blind SQL Injection Blind SQL Injection (QUERY_STRING) Blind SQL Injection (QUERY_STRING) in Blind SQL Injection coming from Blind SQL Injection description Blind SQL Injection in Blind SQL Injection solution CRLF CRLF Injection (QUERY_STRING) in CRLF description CRLF solution Commands execution Commands execution description Commands execution solution Cross Site Scripting Cross Site Scripting description Cross Site Scripting solution Evil url File Handling File Handling description File Handling solution Form Forms Forms Info Found XSS in Found permanent XSS attacked by Found permanent XSS in From Intputs Invalid link argument Looking for permanent XSS Make sure the url is correct. Method No links or forms found in this page ! Open Report Resource consumption Resource consumption description Resource consumption solution SQL Injection SQL Injection description SQL Injection solution Selects TextAreas Timeout Timeout (QUERY_STRING) in Timeout coming from Timeout in To URLS URLs Upload Scripts Upload scripts found Wapiti-SVN (wapiti.sourceforge.net) XSS attackGET attackPOST attacked by caused by coming from in lswwwDoc wapityDoc with with a browser to see this report. with field with fields with params Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2009-05-05 12:45+0200
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 (QUERY_STRING) (QUERY_STRING) in Internal Server Error. The server encountered an unexpected condition which prevented it from fulfilling the request.<ul>  <li><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5'>      World Wide Web Consortium: HTTP/1.1 Status Code Definitions      </a></li>  <li><a href='http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_Error'>      Wikipedia: List of HTTP status codes      </a></li></ul> 500 HTTP Error code 500 HTTP Error code coming from 500 HTTP Error code in 500 HTTP Error code with A report has been generated in the file Attacking forms (POST) Attacking urls (GET) Blind SQL Injection Blind SQL Injection (QUERY_STRING) Blind SQL Injection (QUERY_STRING) in Blind SQL Injection coming from Blind SQL injection is a technique that exploits a vulnerability occurring in the database of an application. This kind of vulnerability is harder to detect than basic SQL injections because no error message will be displayed on the webpage. Blind SQL Injection in To protect against SQL injection, user input must not directly be embedded in SQL statements. Instead, user input must be escaped or filtered or parameterized statements must be used. CRLF CRLF Injection (QUERY_STRING) in The term CRLF refers to Carriage Return (ASCII 13, \r) Line Feed (ASCII 10, \n). They're used to note the termination of a line, however, dealt with differently in today’s popular Operating Systems. For example: in Windows both a CR and LF are required to note the end of a line, whereas in Linux/UNIX a LF is only required. This combination of CR and LR is used for example when pressing 'Enter' on the keyboard. Depending on the application being used, pressing 'Enter' generally instructs the application to start a new line, or to send a command. Check the submitted parameters and do not allow CRLF to be injected by filtering CRLF Commands execution This attack consists in executing system commands on the server. The attacker tries to inject this commands in the request parameters Prefer working without user input when using file system calls Cross Site Scripting Cross-site scripting (XSS) is a type of computer security vulnerability typically found in web applications which allow code injection by malicious web users into the web pages viewed by other users. Examples of such code include HTML code and client-side scripts. The best way to protect a web application from XSS attacks is ensure that the application performs validation of all headers, cookies, query strings, form fields, and hidden fields. Encoding user supplied output in the server side can also defeat XSS vulnerabilities by preventing inserted scripts from being transmitted to users in an executable form. Applications can gain significant protection from javascript based attacks by converting the following characters in all generated output to the appropriate HTML entity encoding:  &lt;, &gt;, &amp;, &quot;, ', (, ), #, %, ; , +, -. Evil url File Handling This attack is also known as Path Transversal or Directory Transversal, its aim is the access to files and directories that are stored outside the web root folder. The attacker tries to explore the directories stored in the web server. The attacker uses some techniques, for instance, the manipulation of variables that reference files with 'dot-dot-slash (../)' sequences and its variations to move up to root directory to navigate through the file system. Prefer working without user input when using file system calls<br>Use indexes rather than actual portions of file names when templating or using language files (ie value 5 from the user submission = Czechoslovakian, rather than expecting the user to return 'Czechoslovakian').<br>Ensure the user cannot supply all parts of the path – surround it with your path code.<br>Validate the user’s input by only accepting known good – do not sanitize the data.<br>Use chrooted jails and code access policies to restrict where the files can be obtained or saved to. Form Forms Forms Info Found XSS in Found permanent XSS attacked by Found permanent XSS in From Inputs Invalid link argument Looking for permanent XSS Make sure the url is correct. Method No links or forms found in this page ! Open Report Resource consumption An attacker can force a victim to consume more resources than should be allowed for the attacker's level of access. The program can potentially fail to release or incorrectly release a system resource. A resource is not properly cleared and made available for re-use. It can also be a false-positive due to a too short timeout used for the scan. Configure properly the software giving the ressource to avoid memory consumption or system load. SQL Injection SQL injection is a technique that exploits a vulnerability occurring in the database of an application. To protect against SQL injection, user input must not directly be embedded in SQL statements. Instead, user input must be escaped or filtered or parameterized statements must be used. Selects TextAreas Timeout Timeout (QUERY_STRING) in Timeout coming from Timeout in To URLS URLs Upload Scripts Upload scripts found Wapiti-SVN (wapiti.sourceforge.net) XSS attackGET attackPOST attacked by caused by coming from in  lswww explore a website and extract links and forms fields.
 
  Usage: python lswww.py http://server.com/base/url/ [options]
 
  Supported options are:
 -s <url>
 --start <url>
 	To specify an url to start with
 
 -x <url>
 --exclude <url>
 	To exclude an url from the scan (for example logout scripts)
 	You can also use a wildcard (*)
 	Example : -x http://server/base/?page=*&module=test
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
 	To print this usage message Wapiti-SVN - A web application vulnerability scanner 
 
 Usage: python wapiti.py http://server.com/base/url/ [options] 
 
 Supported options are: 
 -s <url> 
 --start <url> 
 	To specify an url to start with 
  
 -x <url> 
 --exclude <url> 
 	To exclude an url from the scan (for example logout scripts) 
 	You can also use a wildcard (*) 
 	Example : -x http://server/base/?page=*&module=test 
 	or -x http://server/base/admin/* to exclude a directory 
 
 -p <url_proxy> 
 --proxy <url_proxy> 
 	To specify a proxy 
 	Example: -p http://proxy:port/ 
 
 -c <cookie_file> 
 --cookie <cookie_file> 
 	To use a cookie 
 
 -t <timeout> 
 --timeout <timeout> 
 	To fix the timeout (in seconds) 
 
 -a <login%password> 
 --auth <login%password> 
 	Set credentials for HTTP authentication 
 	Doesn't work with Python 2.4 
 
 -r <parameter_name> 
 --remove <parameter_name> 
 	Remove a parameter from URLs 
 
 -n <limit> 
 --nice <limit> 
 	Define a limit of urls to read with the same pattern 
 	Use this option to prevent endless loops 
 	Must be greater than 0 
 
 -m <module> 
 --module <module> 
 	Use a predefined set of scan/attack options 
 	GET_ALL: only use GET request (no POST) 
 	GET_XSS: only XSS attacks with HTTP GET method 
 	POST_XSS: only XSS attacks with HTTP POST method 
 
 -u 
 --underline 
 	Use color to highlight vulnerables parameters in output 
 
 -v <level> 
 --verbose <level> 
 	Set the verbosity level 
 	0: quiet (default), 1: print each url, 2: print every attack 
 
 -f <type_file> 
 --reportType <type_file> 
 	Set the type of the report 
 	xml: Report in XML format 
 	html: Report in HTML format 
 
 -o <output> 
 --output <output_file> 
 	Set the name of the report file 
 	If the selected report type is 'html', this parameter must be a directory 
 
 -h 
 --help 
 	To print this usage message with with a browser to see this report with field with fields with params 