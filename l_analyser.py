#
#resource r2(f1,f2,f3);
#resource R={r1,r2};
#
#            ****Grammar**** 
#resource_def::= resource <id> ( <id_list> )
#	       | resource <id>= { <resource_ids> }


from sets import Set
import re
import sys
import os.path
from sys import argv

class lexer(object):

	line_count=0
	file_ptr=16
	keywords=set(["resource","policy","actor","exists","all","access","allow"])

	def __init__(self):
		print "***************************************************"
		self.f = open(sys.argv[1], 'r')
		self.p()

	def eat_whitespace(self):
		char =self.f.read(1)
		if(char==" "):
			print "eat white space"
			while(self.f.read(1)==" "):
				print "skip"
			self.f.seek(-1,1)
		elif(char=="\n"):
			self.line_count+=1
		else:
			self.f.seek(-1,1)	
		
	def lex(self):
	
		self.eat_whitespace()

		char =self.f.read(1)
  
                #print "char=%s"%char

		if (char==""):
			  return "EOF"
	
		if (char.isalpha()):
			s=""
			while(char.isalnum()):
	    			s = "".join((s, char))                                
	    			char=self.f.read(1)
                        
			self.f.seek(-1,1)        		
			#print s
			if s in self.keywords:
				return s
			return "identifier"

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
			return "colon"
		if(char=="->"):
			return "arrow"
		if(char=="*"):
			return "asterisk"
		if(char=="!"):
			return "exclamation"
		if(char=="="):
			return "equals"

	def p(self):
	
		tok=self.lex()
		print tok
		if(tok!="resource"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)			
		
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"			
			sys.exit(0)
		
		tok=self.lex()
		print tok
		if(tok=="equals"):
			tok=self.lex()
			if(tok!="curlyopen"):
				print "Error-keep curly open brace"
				sys.exit(0)

			self.id_list()
		
			tok=self.lex()		
			print tok
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)
		elif(tok=="simpleopen"):
			
			self.id_list()
		
			tok=self.lex()		
			print tok
			if(tok!="simpleclose"):
				print "Error-closebrace"
				sys.exit(0)

		else:
			print "put either equals or simple brace"
			sys.exit(0)

		tok=self.lex()
		print tok
		if(tok!="semi"):
			print "Error-no semi"
			sys.exit(0)

		tok=self.lex()
		#print tok
		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.p()
		print "Parsed successfully :D"
	def id_list(self):
	
		#print "entered the id list"

		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)
		
		tok=self.lex()
		print tok
		if(tok!="simpleclose" and tok!="comma" and tok!="curlyclose"):
			print "Error-idlist"
			sys.exit(0)
		if(tok=="comma"):
			self.id_list()
		if(tok=="simpleclose" or tok=="curlyclose"):
			self.f.seek(-1,1)  
					 							
lexer()
