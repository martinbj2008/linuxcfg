#!/usr/bin/python

import sys, time, os, re, difflib
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

	def __init__(self, id, t, s, o, d, p, m):
		self.id=id
		self.title=t
		self.status=s
		self.owner=o
		self.deadline=d
		self.priority=p
		self.milestone=m

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

def backlog_bugs():
	P1bugs=[]
	P2bugs=[]
	ReviewBugs=[]
	hqbugs=[]

	mysql_result = backlogbugs(db)
	for k in mysql_result:
		usrname=userid2name(db, k[3])
		pr = BUG(k[0], k[1], k[2], usrname, k[4], k[5], k[6])
		if pr.IsFixed():
			continue;

		if pr.IsImport() == 0:
			continue;

		if pr.owner == "qian.he@6wind.com":
			hqbugs.append(pr)
		elif pr.IsReviewed():
			ReviewBugs.append(pr)
		elif pr.priority == "P1":
			P1bugs.append(pr)
		elif pr.priority == "P2":
			P2bugs.append(pr)

	print "========= P1 ========="
	for pr in P1bugs:
		pr.show()
	print "========= P2 ========="
	for pr in P2bugs:
		pr.show()

	print "========= Review ========"
	for pr in ReviewBugs:
		pr.show()

	print "===== NOT ASSING ====="
	for pr in hqbugs:
		pr.show()

def list_PR_by_owner(db, name):
	PRs = [];
	user_id = name2userid(db, name);

	req =  "select bug_id, short_desc, bug_status, assigned_to, deadline, \
			priority, target_milestone from bugs.bugs where assigned_to=%d and bug_status != 'RESOLVED' and bug_status != 'CLOSED' and bug_status != 'VERIFIED' " % user_id;
	c = db.cursor()
	n = c.execute(req, ())
	sql_result = c.fetchall()
	c.close()
	for k in sql_result:
		pr = BUG(k[0], k[1], k[2], name, k[4], k[5], k[6])
		PRs.append(pr)
		pr.show();
	return PRs;

for i in sys.argv:
	print i

# connect to db
db = MySQLdb.connect(dbhost, dbuser, dbpass, dbbase)
if db == None:
	print "Cannot connect mysql database"
	sys.exit(1)

#list_PR_by_owner(db, "huibin.du@6wind.com");
