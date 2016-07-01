from sets import Set

import pdb
import re
import sys
import os.path
from sys import argv

listchk = []
class lexer(object):
      
	line_count=0
	file_ptr=16
	keywords=set(["resource","policy","actor","exists","all","access","allow"])

	def __init__(self):
		print "***************************************************"
		self.f = open("res.txt", 'r')
		self.start()

	############################## LEXICAL ANALYSER ########################################	

	def eat_whitespace(self):
		char =self.f.read(1)
		if(char==" "):
			print "eat white space"
			while(self.f.read(1)==" "):
				print "skip space"
			self.f.seek(-1,1)
			self.eat_whitespace()
		elif(char=="\n"):
			print "skip line"
			self.line_count+=1
			self.eat_whitespace()
		else:
			self.f.seek(-1,1)
		
	def lex(self):
	        
		self.eat_whitespace()

		char =self.f.read(1)
		print char
		if (char==""):
			  return "EOF"
	
		if (char.isalpha()):
			s=""
			while(char.isalnum()):
	    			s = "".join((s, char))                                
	    			char=self.f.read(1)
                        
			self.f.seek(-1,1)        		
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
                
	############################# START PARSER #############################################

	def start(self):
		tok=self.lex()
		print tok
		if(tok!="resource" and tok!="actor"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)

		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.resource_def()
		else:
			self.actor_def()

		print "Parsed successfully :D"
		print "***************************************************"

	############################## ID/RESOURCE/ACTOR LIST ##################################

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
	
	def resource_id(self):
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)				 							

		tok=self.lex()
		print tok
		if(tok!="dot" ):
			print "Error-no dot"
			sys.exit(0)

		tok=self.lex()
		print tok
	
		if(tok!="simpleopen" and tok!="identifier"):
			print "Error-define resources properly"
			sys.exit(0)
	
		if(tok=="simpleopen"):
			self.id_list()

			tok=self.lex()
			print tok		
			if(tok!="simpleclose"):
				print "Error-closebrace"
				sys.exit(0)
						
			tok=self.lex()
			print tok
			if(tok!="semi" and tok!="comma"):
				print "Error-add ; OR ,"
				sys.exit(0)
		
			if(tok=="comma"):
				self.resource_id()
			
		else:
			print "Its identifier"
			tok=self.lex()			
			print tok
			if(tok!="comma" and tok!="semi"):
				print "Error no , or ;"
				sys.exit(0)
			if(tok=="comma"):
				self.resource_id()

		


	def actor_list(self):
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"			
			sys.exit(0)
		
		tok=self.lex()
		print tok
		if(tok!="colon"):
			print "Error-colon"			
			sys.exit(0)
		
		self.resource_id()
		
		curr_fileptr=self.f.tell()		
		tok=self.lex()
		print tok
		if(tok=="identifier"):
			self.f.seek(curr_fileptr)
			self.actor_list()
		self.f.seek(curr_fileptr)

	################################# ACTOR DEFINITION #####################################

	def actor_def(self):
		tok=self.lex()
		print tok
		if(tok!="actor"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)
		
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"			
			sys.exit(0)
	
		
		tok=self.lex()
		print tok
		if(tok!="curlyopen" and tok!="equals"):
				print "Error-keep curly open brace or equals"
				sys.exit(0)
		
		if(tok=="curlyopen"):
			self.actor_list()

			tok=self.lex()		
			print tok
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)
		else:
			tok=self.lex()
			print tok

			if(tok!="curlyopen"):
				print "ERROR- no curly open :( "
				sys.exit(0)
			self.id_list()

			tok=self.lex()		
			print tok
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)

			tok=self.lex()
			print tok
			if(tok!="semi"):
				print "Error-no semi %d"%self.line_count
				sys.exit(0)
		
		tok=self.lex()
		print tok
		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.resource_def()

		elif(tok=="actor"):
			self.f.seek(-len("actor"),1)
			self.actor_def()
		elif(tok=="policy"):
			self.f.seek(-len("resource"),1)
			self.policy_def()
		else:
			self.f.seek(-1,1)
	############################## RESOURCE DEFINITION #####################################	
			
	def resource_def(self):
	
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
			print "Error-no semi %d++++++++++++++++++++"%self.line_count
			sys.exit(0)

		tok=self.lex()
		#print tok
		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.resource_def()

		elif(tok=="actor"):
			self.f.seek(-len("actor"),1)
			self.actor_def()
		elif(tok=="policy"):
			self.f.seek(-len("resource"),1)
			self.policy_def()
		else:
			self.f.seek(-1,1)

	
	############################## POLICY DEFINITION #######################################
	
	def policy_def(self):
		tok=self.lex()
		print tok
		if(tok!="policy"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)			
		
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"			
			sys.exit(0)
		
		tok=self.lex()
		print tok
		if(tok!="colon"):	
			print "Error- no Colon"
			sys.exit(0)
		
		tok=self.lex()
		print tok
		if(tok=="allow"):	
			self.f.seek(-len("allow"),1)
			self.policy_1()

	def  policy_1(self):

		tok=self.lex()
		print tok
		if(tok!="allow"):
			print "Error- no allow/all/exists"
			sys.exit(0)
		 
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"			
			sys.exit(0)		
		
		tok=self.lex()
		print tok
		if(tok!="access"):
			print "Error-no access"
			sys.exit(0)

		self.resource_id()
		
		tok=self.lex()
		print tok
		if(tok=="allow"):	
			self.f.seek(-len("allow"),1)
			self.policy_1()						
lexer() 
