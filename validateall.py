#!/usr/bin/env python3

# validateall.py
# Description: Validate all HTML and CSS files in a given directory, returning any errors in the terminal by line number.
# Usage: launch script in directory of files to validate
# Requires: default Python 3 libraries
#
# dev notes:
# if there's any one script i've gotten the most mileage out of, it's this one. as of the time of this writing, I work as a TA, and when grading HTML/CSS student work, we generally ensure they pass an HTML and CSS validator as part of the grade. earlier on I would use the web front-end (same as the students), but they're a bit slow and clunky. eventually I got tired of it, and wrote a script to leverage the HTTP APIs they have exposed on the sites (presumably for exactly this kind of purpose!).
# every time i start a grading run, I alias this script in my terminal, and run it whenever i start grading a submission to catch the most blatant errors. as such, it gets run a hundred times or more during a work week, saving me quite a bit of time on each one, while still returning the same errors they would see when using the web interface.

import urllib.request, urllib, json, os, re
import xml.etree.ElementTree as XML
class ValidationMessage:
    def __init__(self, line, message):
        self.line = line
        self.msg = message
    def __str__(self):
        return f'On line {self.line}: {self.msg}'
class HTMLValidator:

    """ Validate HTML using the Validator.nu Web service.

    Keyword arguments:
    code -- a bytes-like object in HTML

    """

    url = 'http://html5.validator.nu?out=json'
    def __init__(self, code):
        self.code = code
    def __enter__(self):
        self.errors = []
        req = urllib.request.Request(self.url)
        req.add_header('Content-Type','text/html')
        req.data = self.code.read().encode('utf-8')
        with urllib.request.urlopen(req) as res:
            msgs = json.load(res)['messages']
            for msg in msgs:
                if msg['type'] == "error":
                    self.errors.append(ValidationMessage(msg['lastLine'],msg['message']))
        return self.errors
    def __exit__(self, errtype, errval, trace):
        return
class CSSValidator:
    url = 'https://jigsaw.w3.org/css-validator/validator?'
    def __init__(self, code):
        self.code = code
    def __enter__(self):
        self.errors = []
        data = {
                "text": self.code.read(),
                "output": "soap12",
                "profile": "css3"
                }
        req = urllib.request.Request(self.url+urllib.parse.urlencode(data))
        with urllib.request.urlopen(req) as res:
            soap = XML.fromstring(res.read())
            for errmsg in soap.iter(tag="{http://www.w3.org/2005/07/css-validator}error"):
                line = errmsg.find('{http://www.w3.org/2005/07/css-validator}line').text.strip()
                msg = errmsg.find('{http://www.w3.org/2005/07/css-validator}message').text.strip()
                msg = re.sub(r'\s+', ' ', msg)
                self.errors.append(ValidationMessage(line, msg))
        return self.errors
    def __exit__(self, errtype, errval, traceback):
        return

# ls/dir
dir = os.listdir('.')
# check if any files are html or css
for listing in dir:
    if listing[-3:] == "css":
        print(listing+":")
        pass
        # open valid css file
        with open(listing) as file:
            # run through CSSValidator
            with CSSValidator(file) as errors:
                # print errors if necessary
                for error in errors:
                    print(error)
    if listing[-4:] == "html":
        print(listing+":")
        # open valid html file
        with open(listing) as file:
            # run through HTMLValidator
            with HTMLValidator(file) as errors:
                # print errors if necessary
                for error in errors:
                    print(error)
