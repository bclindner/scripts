#!/usr/bin/env python3

# altcase.py:
# Description: Converts a string into AlTeRnAtInG cASe and copies it to the clipboard.
# Usage: ./altcase.py "[text to convert to alternating case]"
# Requires: Python 3 and pyperclip library
# dev notes: a simple one for writing dumb messages in chats, kept in this repo so i have it on hand.
import sys, pyperclip

def altcase(string):
    x = True
    ret = ""
    for letter in string:
        if x == True:
            x = False
            ret += letter.lower()
        elif x == False:
            x = True
            ret += letter.upper()
    return ret

text = sys.argv[1]
pyperclip.copy(altcase(text))
