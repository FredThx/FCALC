#from pyperclip import copy, paste
import pyperclip
import logging

def copy(*args, **kwargs):
    try:
        return pyperclip.copy(*args, **kwargs)
    except pyperclip.PyperclipException:
        logging.error("Copy or Paste error. on linux : sudo apt-get install xclip")

def paste(*args, **kwargs):
    try:
        return pyperclip.paste(*args, **kwargs)
    except pyperclip.PyperclipException:
        logging.error("Copy or Paste error. on linux : sudo apt-get install xclip")
