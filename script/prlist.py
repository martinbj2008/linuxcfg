#!/usr/bin/python

import sys, time, os, re, difflib
import getopt
import MySQLdb

###### configuration

dbhost = "core"
dbuser = "6bugs"
dbpass = "6bugs"
dbbase = "bugs"

#########
class   User:
	name=""
	id=""
	def __init__(self, name, id):
		self.name = name;
		self.id = id; 

class BUG:
	id=""
	title=""
	status=""
	owner=""
	deadline=""
	priority=""
	milestone=""
	keywords=""

	def __init__(self, id, t, s, o, d, p, m, k, product):
		self.id=id
		self.title=t
		self.status=s
		self.owner=o
		self.deadline=d
		self.priority=p
		self.milestone=m
		self.keywords=k
		self.product=product

	def show(self):
		print "[%s] %s" %(self.id, self.title)
		print "\t %s,\t%s,\t%s" %(self.owner, self.status, self.milestone) 
		print "\t %s,\t%s" %(self.priority, self.deadline) 

	def IsFixed(self):
		return (self.status == "RESOLVED" or self.status == "CLOSED" or \
			self.status == "DONE" or self.milestone == "approved")

	def IsReviewed(self):
		return self.milestone == "review"

	def IsImport(self):
		return (self.priority == "P1" or self.priority == "P2")

	def IsBacklog(self):
		return (self.keywords.find("BACKLOG") != -1)

	def IsRoutingPR(self):
		return (self.product == 17)

	def checkCC(self):
		if (self.IsBacklog()):
			if not Is_CC_qian(db, self.id):
				print "* qian.he is NOT in CC list"
			if self.IsRoutingPR() and  not Is_CC_fenglu(db, self.id):
				print "* feng.lu is NOT in CC list"

def backlogbugs(db):
	req =  "select bug_id, short_desc, bug_status, assigned_to, deadline, \
		priority, target_milestone from bugs.bugs where keywords \
		like '%%BACKLOG%%' order by priority, bug_id desc"
	c = db.cursor()
	n = c.execute(req, ())
	bugs = c.fetchall()
	c.close()
	return bugs

def userid2name(db, id):
	req =  "select login_name from profiles where userid=%d" % id
	c = db.cursor()
	n = c.execute(req, ()) 
	bugs = c.fetchone()
	c.close()
	return bugs[0]

def name2userid(db, name):
	req =  "select userid from profiles where login_name='%s'" % name
	c = db.cursor()
	n = c.execute(req, ()) 
	bugs = c.fetchone()
	c.close()
	return bugs[0]

def check_CC(db, id, user):
	req =  "select who from cc where bug_id='%d'" % id 
	c = db.cursor()
	n = c.execute(req, ()) 
	cclist = c.fetchall()
	c.close()
	for i in cclist:
		if i[0] == user:
			return 1;
	return 0

def Is_CC_qian(db, id):
	return check_CC(db, id, 132) #132 is qian.he@6wind.com

def Is_CC_fenglu(db, id):
	return check_CC(db, id, 139) #139 is lu.feng@6wind.com

def list_PR_by_owner(db, name):
	PRs = [];
	user_id = name2userid(db, name);
	req =  "select bug_id, short_desc, bug_status, assigned_to, deadline, priority,\
		target_milestone, keywords, product_id from bugs.bugs where assigned_to=%d and \
		bug_status != 'RESOLVED' and bug_status != 'CLOSED' and bug_status != 'VERIFIED' " % user_id;

	c = db.cursor()
	n = c.execute(req, ())
	sql_result = c.fetchall()
	c.close()
	for k in sql_result:
		pr = BUG(k[0], k[1], k[2], name, k[4], k[5], k[6], k[7], k[8])
		PRs.append(pr)
		pr.show();
		pr.checkCC();
	return PRs;

def usage():
	print 'prlist.py owner_email'

if len(sys.argv) != 2:
	usage()
	sys.exit();

# connect to db
db = MySQLdb.connect(dbhost, dbuser, dbpass, dbbase)
if db == None:
	print "Cannot connect mysql database"
	sys.exit(1)

#example: list all PR whose owner is xxx.
list_PR_by_owner(db, sys.argv[1]);

#example: check if qian.he is in CC list
#pr_id=33322
#CC_str="NOT "
#if Is_CC_qian(db, pr_id):
#	CC_str=""
#print "PR%d: qian.he%s in CC list" % (pr_id,  CC_str)
 


