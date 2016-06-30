#
#resource r2(f1,f2,f3);
#resource R={r1,r2};
#actor a1 
#   {
#    uses: r1.(f1, f2, f4), r2.(f3, f7,f5);
#   }
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
		self.start()

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

		

	def actor_def(self):
		tok=self.lex()
		print tok
		if(tok!="actor"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)
		#################################
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"			
			sys.exit(0)
		#################################
		tok=self.lex()
		print tok
		if(tok!="curlyopen"):
				print "Error-keep curly open brace"
				sys.exit(0)
		#################################
		self.actor_list()
		################################
		tok=self.lex()		
		print tok
		if(tok!="curlyclose"):
			print "Error-keep curly close brace"
			sys.exit(0)
		##################################
		tok=self.lex()
		#print tok
		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.resource_def()

		elif(tok=="actor"):
			self.f.seek(-len("actor"),1)
			self.actor_def()
		else:
			self.f.seek(-1,1)
		

	def actor_list(self):
		tok=self.lex()
		print tok
		if(tok!="identifier"):
			print "Error-iden"			
			sys.exit(0)
		##########################
		tok=self.lex()
		print tok
		if(tok!="colon"):
			print "Error-colon"			
			sys.exit(0)
		##########################
		self.resource_id()
		##########################
		'''tok=self.lex()
		print tok
		
		if(tok!="curlyclose"):
			print "Error-no curly %d ***********"%self.line_count			
			sys.exit(0)'''
		##########################
		curr_fileptr=self.f.tell()		
		tok=self.lex()
		print tok
		if(tok=="identifier"):
			self.f.seek(curr_fileptr)
			self.actor_list()
		self.f.seek(curr_fileptr)

				
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

		if(tok=="actor"):
			self.f.seek(-len("actor"),1)
			self.actor_def()


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


lexer()
