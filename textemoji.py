#!/usr/bin/env python3

# textemoji.py:
# Description: Converts a string into AlTeRnAtInG cASe and copies it to the clipboard.
# Usage: ./textemoji.py [prefix] "[text to convert to text-emoji]" [suffix]
# Requires: Python 3 and pyperclip library
# dev notes: this is designed primarily to generate text from emoji shortcodes, in particular Discord's :regional_indicator_*: emojis. it's in this repo just so i have it on hand when i need it on my machines.
import sys, pyperclip

def textemoji(prefix, string, suffix):
    ret = ""
    for letter in string:
        if letter.isalpha():
            ret += prefix + letter + suffix
        else:
            ret += letter
    return ret

prefix = sys.argv[1]
text = sys.argv[2]
sufffix = sys.argv[3]
pyperclip.copy(textemoji(prefix, text, suffix))
