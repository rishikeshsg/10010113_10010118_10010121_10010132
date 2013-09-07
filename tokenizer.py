#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""*********************************************************************
* Program	: tokenizer.py
* Author 	: Arpit Agarwal
* Date of open	: 23/09/2013
* Details	: Simple tokenization algorithm. Feel free to expand and extend it.
                  Returns a list of tokens from some raw text file.
*********************************************************************"""


import sys, os, os.path, glob, codecs


delimiterSet = ";.,?\"()':[]\n/+-—==={}><!@#$%^&*’”“|"
digits = "0123456789"
chars = "abcdefghijklmnopqrstuvwxyz"
chars = "".join( (chars, chars.upper()) )
spaces = " \t\n"
stopwords=[]

numberdelimiters = ",."
def stopword(fname):
	try:
	  inStream = open(fname,"r")
	  sw = inStream.readline()
	  sw = sw[:-1]
	  while sw:
		  stopwords.append(sw)
		  sw = inStream.readline()
		  sw = sw[:-1]
	  inStream.close()
	except IOError:
	  print("Cannot read from file:"+ fname)

def tokenize_and_remove_stopword(fname):
   token_list=[]
   global delimiterSet
   doc_stream = []
   output = ""
   if not os.path.isfile(fname):
      print("Error: Not a file", fname, "\n")
      usage()
      return

   try:
      inStream = open(fname,"r")
      token = ""
      ch = inStream.read(1)
      lookahead = inStream.read(1)
      #ch = StringIO(fname).read(1)
      #lookahead = StringIO(fname).read(1)
      while True:
         if not ch:
            if token_list:
               for tok in token_list:
                   output += tok+" "
            return output       
            break
         if ch in delimiterSet:
            if token:
               if token[-1] in digits and lookahead in digits and ch in numberdelimiters:
                  token = "".join( (token, ch) )
               elif not token in stopwords and len(token) > 1:
                  token_list.append(token)
                  token = ""
               else:
                  token = ""
         elif ch in spaces:
            if token: 
               if not token in stopwords and len(token) > 1:
                  token_list.append(token)
               token = ""
         else:
            token = "".join( (token, ch) )
         ch = lookahead
         #lookahead = StringIO(fname).read(1)
         lookahead = inStream.read(1)
      inStream.close()
   except IOError:
      print ("Cannot read from file:"+ fname)

def usage():
   print ("""
tokenizer.py

Usage:
python3 tokenizer.py 
""")
