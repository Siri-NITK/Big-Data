from sets import Set

import pdb
import re
import sys
import os.path
from sys import argv
from cls import *

class lexer(object):

	line_count=0
	file_ptr=16
	keywords=set(["resource","policy","actor","exists","all","access","allow","in"])

	def __init__(self):
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

		elif(char==""):
			print"parsed successfully"
		else:
			self.f.seek(-1,1)

	def lex(self):

		self.eat_whitespace()

		char =self.f.read(1)

		if (char==""):
			  return "EOF",char

		if (char.isalpha()):
			s=""
			while(char.isalnum()):
	    			s = "".join((s, char))
	    			char=self.f.read(1)

			self.f.seek(-1,1)
			if s in self.keywords:
				return s,"keyword"
			return "identifier",s

		if(char==";"):
			return "semi",char
		if(char=="("):
			return "simpleopen",char
		if(char==")"):
			return "simpleclose",char
		if(char=="{"):
			return "curlyopen",char
		if(char=="}"):
			return "curlyclose",char
		if(char==","):
			return "comma",char
		if(char=="."):
			return "dot",char
		if(char==":"):
			return "colon",char
		if(char=="-"):
			char=self.f.read(1)
			print char
			if(char==">"):
				return "arrow",char
			else:
				pass
		if(char=="*"):
			return "asterisk",char
		if(char=="!"):
			return "exclamation",char
		if(char=="="):
			return "equals",char

	############################# START PARSER #############################################

	def start(self):
		tok=self.lex()[0]
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

	def id_list(self,lst):

		
		tok,val=self.lex()
		print tok
		
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)
		lst.append(val)
		

		tok=self.lex()[0]
		print tok

		if(tok!="simpleclose" and tok!="comma" and tok!="curlyclose" and tok!="access"):
			print "Error-idlist"
			sys.exit(0)
		if(tok=="comma"):
			self.id_list(lst)
		if(tok=="simpleclose" or tok=="curlyclose"):
			self.f.seek(-1,1)

		if(tok=="access"):
			self.f.seek(-len("access"),1)
		
		return lst	

	def resource_id(self):
		tok=self.lex()[0]
		print tok

		lst=[]

		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="dot" ):
			print "Error-no dot"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="simpleopen" and tok!="identifier" and tok!="asterisk"):
			print "Error-define resources properly"
			sys.exit(0)

		if(tok=="simpleopen"):
			lst=self.id_list(lst)

			print 
			tok=self.lex()[0]
			print tok
			if(tok!="simpleclose"):
				print "Error-closebrace"
				sys.exit(0)

			tok=self.lex()[0]
			print tok
			if(tok!="semi" and tok!="comma"):
				print "Error-add ; OR ,"
				sys.exit(0)

			if(tok=="comma"):
				self.resource_id()

		if(tok=="identifier"):
			print "Its identifier"
			tok=self.lex()[0]
			print tok
			if(tok!="comma" and tok!="semi"):
				print "Error no , or ;"
				sys.exit(0)
			if(tok=="comma"):
				self.resource_id()

		if(tok=="asterisk"):
			tok=self.lex()[0]
			print tok
			if(tok!="comma" and tok!="semi"):
				print "Error no , or ;"
				sys.exit(0)
			if(tok=="comma"):
				self.resource_id()



	def actor_list(self):
		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="colon"):
			print "Error-colon"
			sys.exit(0)

		self.resource_id()

		curr_fileptr=self.f.tell()
		tok=self.lex()[0]
		print tok
		if(tok=="identifier"):
			self.f.seek(curr_fileptr)
			self.actor_list()
		self.f.seek(curr_fileptr)

	################################# ACTOR DEFINITION #####################################

	def actor_def(self):
		tok=self.lex()[0]
		print tok

		lst=[]

		if(tok!="actor"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)

		tok,val=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

        	actor(val)

		tok=self.lex()[0]
		print tok
		if(tok!="curlyopen" and tok!="equals"):
				print "Error-keep curly open brace or equals"
				sys.exit(0)

		if(tok=="curlyopen"):
			self.actor_list()

			tok=self.lex()[0]
			print tok
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)
		else:
			tok=self.lex()[0]
			print tok

			if(tok!="curlyopen"):
				print "ERROR- no curly open :( "
				sys.exit(0)
			lst=self.id_list(lst)

			tok=self.lex()[0]
			print tok
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)

			tok=self.lex()[0]
			print tok
			if(tok!="semi"):
				print "Error-no semi %d"%self.line_count
				sys.exit(0)

		tok=self.lex()[0]
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

		lst=[]		
		
		tok=self.lex()[0]
		print tok
		if(tok!="resource"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)

		tok,val=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

		r=resource(val)

		tok=self.lex()[0]
		print tok
		if(tok=="equals"):
			tok=self.lex()[0]
			if(tok!="curlyopen"):
				print "Error-keep curly open brace"
				sys.exit(0)

			r.fields=self.id_list(lst)
			
			print "*******list/**************"
			print r.fields

			tok=self.lex()[0]
			print tok
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)

		elif(tok=="simpleopen"):

			r.fields=self.id_list(lst)

			print "*******list/**************"
			print r.fields

			tok=self.lex()[0]
			print tok
			if(tok!="simpleclose"):
				print "Error-closebrace"
				sys.exit(0)

		else:
			print "put either equals or simple brace"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="semi"):
			print "Error-no semi %d++++++++++++++++++++"%self.line_count
			sys.exit(0)

		tok=self.lex()[0]
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
		tok=self.lex()[0]
		print tok
		if(tok!="policy"):
			print "Start line %d with policy." %self.line_count
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="colon"):
			print "Error- no Colon"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok=="allow"):
			#self.f.seek(-len("allow"),1)
			self.policy_1()
		if(tok=="all"):
			self.policy_2()
		if(tok=="exists"):
			self.policy_3()


	def  policy_1(self):

		#print "111111111111111111111111111111111111111"
		lst=[]

		lst=self.id_list(lst)

		tok=self.lex()[0]
		print tok
		if(tok!="access"):
			print "Error-no access"
			sys.exit(0)

		self.resource_id()

		tok,val=self.lex()
		print tok
		if(tok=="allow"):
			#self.f.seek(-len("allow"),1)
			self.policy_1()
		elif(tok=="policy"):
			self.f.seek(-len("policy"),1)
			self.policy_def()
		else:
			pass

	def  policy_2(self):

		#print "222222222222222222222222222222222222222"
		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="colon"):
			print "Error-no colon"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="actor"):
			print "Error-no actor :("
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="dot" ):
			print "Error-no dot"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="dot"):
			print "Error-no dot"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="equals"):
			print "Error no equals"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="arrow"):
			print "Error-no arrow"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok=="allow"):
			self.policy_1()

	def policy_3(self):

		print "333333333333333333333333333333333333"
		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="in"):
			print "Error-no in"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="colon"):
			print "Error- no Colon"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="actor"):
			print "Error-no actor :("
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="dot"):
			print "Error-no dot"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="dot"):
			print "Error-no dot"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="equals"):
			print "Error no equals"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok!="arrow"):
			print "Error-no arrow"
			sys.exit(0)

		tok=self.lex()[0]
		print tok
		if(tok=="allow"):
			self.policy_1()
############################################################
lexer()


print ', '.join(i.id for i in actors_list)

for i in resources_list:
	print i.fields


