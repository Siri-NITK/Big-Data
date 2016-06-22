import re
import sys
import os.path
from sys import argv

class lexer(object):

	line_count=0
	file_ptr=16
    	token_exprs = {
	    "equals":'=',
	    "simpleopen":'(',
	    "simpleclose":')',
	    "semi":';',
            "comma":',',
            "dot":'.',
            "colon":':',
            "curlyopen":'{',
            "curlyclose":'}',
            "asterisk":'*',
            "arrow":'->',
            "exclamation":'!',
            "policy":'policy',
            "actor":'actor',
            "resource":'resource',
            "allow":'allow',
            "exists":'exists',
            "access":'access',
            "all":'all',
	    "ID":r'[A-Za-z][A-Za-z0-9_]*',
	}

	def __init__(self):
		print self.token_exprs["resource"]
		print self.lex()

	def lex(self):

		file = open(sys.argv[1], 'r')
		file.seek(self.file_ptr)	
		char =file.read(1)

		if (char==""):
			  return "EOF"
		if (char.isalpha()):
			s=""
        		while(char.isalpha()):
            			s = "".join((s, char))
            			char=file.read(1)
			return "identifier"
		if(char=="\n"):
			count+=1
		if(char==";"):
			return "semi"
		if(char=="("):
			return "simpleopen"
		if(char==")"):
			return "simpleclose"
		if(char=="{"):
			return "curlyopen"
		if(char=="}"):
			return "curlyclose"
		if(char==","):
			return "comma"
		if(char=="."):
			return "dot"
		if(char==":"):
			print "colon"
		if(char=="*"):
			print "asterisk"
		if(char=="->"):
			return "arrow"
		if(char=="!"):
			return "exclamation"
		if(char=="="):
			return "equals"
	

lexer()
