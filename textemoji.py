#!/usr/bin/env python3

# textemoji.py:
# Description: Converts a string into emoji shortcodes and copies it to the clipboard.
# Usage: ./textemoji.py [prefix] "[text to convert to text-emoji]" [suffix]
# Requires: Python 3 and pyperclip library
# dev notes: this is designed primarily to generate text from emoji shortcodes, in particular Discord's :regional_indicator_*: emojis.
# it's in this repo just so i have it on hand when i need it on my machines.
import sys

def textemoji(prefix, string, suffix):
    ret = ""
    for letter in string:
        if letter.isalpha():
            ret += prefix + letter + suffix
        else:
            ret += letter
        ret += " "
    return ret

prefix = sys.argv[1]
text = sys.argv[2]
suffix = sys.argv[3]
print(textemoji(prefix, text, suffix))
