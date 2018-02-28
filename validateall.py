#!/usr/bin/env python3

## Validate all HTML files through Validator.nu.

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

# pwd
dir = os.listdir('.')
# check if any files are html
for listing in dir:
    if listing[-3:] == "css":
        print(listing+":")
        pass
        # open valid html file
        with open(listing) as file:
            # run through HTMLValidator
            with CSSValidator(file) as errors:
                for error in errors:
                    print(error)
    if listing[-4:] == "html":
        print(listing+":")
        # open valid html file
        with open(listing) as file:
            # run through HTMLValidator
            with HTMLValidator(file) as errors:
                for error in errors:
                    print(error)
