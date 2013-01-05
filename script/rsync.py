#!/usr/bin/python

import sys
import re
import time
import datetime
import os
import logging
import pexpect
import signal
import smtplib
import string
from subprocess import call

#"ip, hostname, #os"
debug_level=0
def warning(str):
	print '\033[1;31m%s\033[1;m' % str

def info(str):
	print '\033[1;32m%s\033[1;m' % str

def debug(str):
	if debug_level:
		print "    ", str

def pingProcess(self):
        pingTest = "ping -c "+ self.pingQuantity + ' ' + self.ipToPing

def run_ssh_cmd(info):
	cmd=info[0]
	passwd=info[1]
	timeout = 5
	shell_ready = 0

	exp_str = ["password:", "yes/no", "#"]

	warning("Run:%s " % cmd)
	host_spawn = pexpect.spawn(cmd)
	while shell_ready == 0:
		try:
			ret = host_spawn.expect(exp_str, timeout)
			if ret == 0:
				print "Send passwd....."
				host_spawn.sendline(passwd)
			elif ret == 1:
				print "Send yes....."
				host_spawn.sendline("yes")
			elif ret == 2:
				warning("shell is ready for %s" % cmd)
				shell_ready=1
		except pexpect.TIMEOUT:
			warning("TIMEOUT and terminate")
			host_spawn.terminate()
			return host_spawn
		except pexpect.EOF:
			warning("ssh failed, get EXPECTEOF")
			return host_spawn
	return host_spawn

def run_shell_cmd(spawn, cmd):
	timeout = 60
	spawn.sendline(cmd)
	try:
		ret = spawn.expect(["#"], timeout)
	except pexpect.TIMEOUT:
		return ""
	return spawn.before

def get_host_network_info(spawn):
	cmd_output = run_shell_cmd(spawn, "ifconfig")
	debug(cmd_output)
	m = re.search(r'10.80.2.[0-9]*', cmd_output)
	if m:
		info(m.group())
	else:
		debug("No match!!")

def get_host_os_info(spawn):
	result = []
	for cmd in ["uname -n", "uname -r"]:
		cmd_output = run_shell_cmd(spawn, cmd)
		debug(cmd_output)

		lines = cmd_output.splitlines()
		result.append(lines[1])
	return result

def get_host(ip):
	host_spawn = run_ssh_cmd(("ssh root@%s" % ip))
	if  not  host_spawn.isalive():
		return []
	os_info = get_host_os_info(host_spawn)
	os_info.insert(0, ip);
	os_info[2] = "#" + os_info[2]
#	network_info = get_host_network_info(host_spawn)
	return os_info

def import_dhcp_result(fname):
	ret = []
	f = open(fname, 'r')
	for line in f:
		if line[0] == '#':
			continue
		ret.append(line.split())
	f.close()
	return ret

def export_dhcp_result(fname, hosts):
	f = open(fname, 'w')
	for host in hosts:
		str = "%s\t%20s\t%s\n" % (host[0], host[1], host[2])
		f.write(str)
	f.close()

def update_host(hosts, host):
	for i in hosts:
		if i[0] == host[0]:
			for idx in range(1, min(len(host),len(i))):
				i[idx] =  host[idx]
			return hosts;
	return hosts.append(host)

def merge_file(f1, f2, fmerge):
	fdst = open(fmerge, 'w')

	fsrc = open(f1, 'r')
	for line in fsrc:
		fdst.write(line)
	fsrc.close

	fsrc = open(f2, 'r')
	for line in fsrc:
		fdst.write(line)
	fsrc.close

	fdst.close()

def update_etc_hosts():
	host_file="/tmp/tmp_hosts"
	etc_file="/etc/hosts"

	hosts = import_dhcp_result(dhcp_file)
	active_hosts=[]
	for i in ip_range:
		ipaddr = "10.80.2.%d" %  i
		active = call(["ping", "-c 1", ipaddr])

		if active != 0:
			info("%s:  has no response" % ipaddr)
			continue

		host = get_host(ipaddr)
		if (len(host) < 2):
			warning("failed to get host(%s) info"  % ipaddr)
			continue

		update_host(hosts, host);
		active_hosts.append(host[0]);
	export_dhcp_result(dhcp_file, hosts)

	merge_file(static_file, dhcp_file, host_file)
	for i in active_hosts:
		run_ssh_cmd("scp " + host_file + " root@" + i + ":" + etc_file)

def get_active_host():
	active_hosts=[]
	for i in ip_range:
		ipaddr = "10.80.2.%d" %  i
		active = call(["ping", "-c 1", ipaddr])

		if active != 0:
			info("%s:  has no response" % ipaddr)
			continue

		host = get_host(ipaddr)
		if (len(host) < 2):
			warning("failed to get host(%s) info"  % ipaddr)
			continue
		active_hosts.append(host[0]);
	return active_hosts

def sync_file(host, files):
	host_spawn = run_ssh_cmd(["ssh root@%s" % host[0], host[1]])
	host_spawn.logfile = sys.stdout
	prefix=host[2];

	for srcfile in files:
		d_start = datetime.datetime.now()
		info("Start : sync %s at %s" % (srcfile, d_start))
		cmd = "mkdir -p `dirname %s/%s`" % (prefix, srcfile)
		run_shell_cmd(host_spawn, cmd)

		rsync_cmd = "rsync -azv --delete 10.80.1.2::%s/  %s/%s" % (srcfile, prefix, srcfile)
		host_spawn.sendline(rsync_cmd)
		fin = 0
		while fin == 0:
			try:
				ret = host_spawn.expect(["#",], 60)
				if ret == 0:
					fin = 1
			except pexpect.TIMEOUT:
				info("rsync is still running ...")
		d_end = datetime.datetime.now()
		info("Fin : sync %s at %s.[Total cost %s]" % (srcfile, d_end, d_end - d_start))

def sync_files(hosts, files):
	for h in hosts:
		info("Start: sync %s" % h[0])
		d_start = datetime.datetime.now()
		print "Sync start at %s" % d_start

		sync_file(h, files)

		d_end = datetime.datetime.now()
		print "Sync end at %s, Total Cost: %s" % (d_end, d_end - d_start)
		info("Fin : sync %s" % h[0])

def mail_result():
	SUBJECT = "Test email from Python"
	TO = "junwei.zhang@6wind.com"
	FROM = "python@mydomain.com"
	text = "blah blah blah"
	BODY = string.join(("From: %s" % FROM, "To: %s" % TO, "Subject: %s" % SUBJECT , "", text ), "\r\n")
	server = smtplib.SMTP('127.0.0.1')
	server.sendmail(FROM, [TO], BODY)
	server.quit()

def sync_aston():
#Only do on Junwei's PC --- testing
	sync_hosts=[
		["10.80.2.243", "root2kk.", "/"],
#		["10.80.4.200", "breizh", "/home/mirror"],
	]

	files = [
		"aston/h_debit/scm/git/projects/framework",
		"aston/h_debit/scm/git/projects/delivery",
		"aston/h_debit/scm/git/projects/customers",
		"aston/h_debit/scm/git/projects/drivers",
		"aston/h_debit/scm/git/projects/infrastructure",
		"aston/h_debit/scm/git/projects/management",
		"aston/h_debit/scm/git/projects/misc",
		"aston/h_debit/scm/git/projects/network",
		"aston/h_debit/scm/git/projects/np",
		"aston/h_debit/scm/git/projects/routing",
		"aston/h_debit/scm/git/projects/security",
		"aston/h_debit/scm/git/projects/vendor",
		"aston/h_debit/scm/git/projects/kernels/linux-broadcom-sdk-2.2.4.git",
		"aston/h_debit/scm/git/projects/kernels/linux-generic-2.6.34.git",
		"aston/h_debit/scm/git/projects/kernels/linux-generic-2.6.36.git",
		"aston/h_debit/scm/git/projects/kernels/linux-generic-3.4.git",
		"aston/h_debit/scm/git/projects/kernels/linux-octeon-sdk2.3.git",
		"aston/h_debit/scm/git/projects/kernels/linux-wr-4.3-ga-cgl-bcm-sdk2.2.4-pp81-bsp1.1-ea2.git",
#		"aston/h_debit/scm/git/projects/tests",
	]

	sync_files(sync_hosts, files)

def sync_opt():
        sync_hosts=[
                 ["10.80.4.200", "breizh", ""],
        ]
	files = ["opt",]
	sync_files(sync_hosts, files)

#update IP address remotely for PCs
static_file="static.addr.txt"
dhcp_file="dhcp.addr.txt"
ip_range=range(200, 254)
#update_etc_hosts()

#sync_opt()
sync_aston()
