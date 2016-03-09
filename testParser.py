#!/usr/bin/python
#-*- coding:utf-8 -*-

from optparse import OptionParser
import os
import sys
import string
from execcmd import *

DATA_DIR = 'database/'
SLEEP_TIME_AFTER_KILL_PROCESS  =  '3'
DEBUG = False

class AppBootUpTime:
	def __init__(self,
		):
		self.shell = ExecCommand()
		self.num = 18
		self.all_app_time_dic = {}
		self.app_dic = {}

	def do_Launch_App_Measure_Task(self,
		loop_count,
		product_name,
		build_version,
		):

		for obj in self.app_dic.keys():
			self.all_app_time_dic[obj] = []

		for i in range(0, loop_count):
			print "The %s Round Starting  ----->>> \n" %i
			for obj in self.app_dic.keys():
				 self.all_app_time_dic[obj].append(self.process_App_Launch_Action(self.app_dic[obj]))

		file_name = self.mkdir_File(product_name, build_version)
		self.write_Data_File(file_name)

	def get_Almost_Average_Value(self,
		):
		aver_app_time_dic = {}
		for obj in self.all_app_time_dic:
			app_time_list = self.all_app_time_dic[obj]
			sum = 0
			cnt = len(app_time_list)
			for line in app_time_list:
				sum += line
			aver_app_time_dic[obj] = sum / cnt
		print "\nAverage App BootUp Time:  %s " %aver_app_time_dic
		return aver_app_time_dic

	def write_Data_File(self,
		file_name,
		):
		if(DEBUG):print 'write_Data_File --->'
		app_aver_time_dic =  self.get_Almost_Average_Value()

		for (key, value) in app_aver_time_dic.items():
			cmd = 'echo ' + key + ':' + str(value) + ' >> ' + file_name
			if(DEBUG):print cmd 
			self.shell.execCmd(cmd)

	def mkdir_File(self,
		product,
		build_version,
		):
		self.shell.execCmd('mkdir ' + product)
		self.shell.execCmd('touch ' + product + '/' + build_version + '_data.txt' )
		if(DEBUG): print 'mkdir _File ---> %s/%s_data.txt' %(product, build_version)
		return product + '/' + build_version + '_data.txt'

	def process_App_Launch_Action(self,
		activity_name,
		):
		package_name = activity_name.split('/')[0]
		self.kill_Process(package_name)
		self.shell.execCmd('sleep ' + SLEEP_TIME_AFTER_KILL_PROCESS)
		if(self.check_Process(package_name)):
			if (DEBUG): print "Error: Can't Kill %s \n" %package_activity_name

		consumed_time = self.launch_Process(activity_name)
		self.kill_Process(package_name)
		self.shell.execCmd('sleep ' + SLEEP_TIME_AFTER_KILL_PROCESS)

		return string.atoi(consumed_time)

	def launch_Process(self,
		activity_name
		):
		print 'Launch_Process : %s' %activity_name
		app_time_list = {}
		cmd = 'adb shell am start -W ' + activity_name
		self.shell.execCmd(cmd.strip())
		app_time_list = self.shell.getOutput().split('\r')

		for str in app_time_list:
			if(str.find('aitTime') > 0):
				consume_time = str.split(': ')[1]
				print 'Need Time ---> %s \n'  %consume_time
				return consume_time

	def check_Process(self,
		activity_name,
		):
		all_process_list = {}
		self.shell.execCmd('adb shell ps')
		all_process_list = self.shell.getOutput().split('\n')
		for str in all_process_list:
			if(str.find(activity_name) > 0):
				if(DEBUG): print "check_Process: Found process \n"
				return True
		return False

	def kill_Process(self,
		activity_name
		):
		self.shell.execCmd("adb shell am force-stop " + activity_name)

	def list_All_App(self,
		input_file,
		):
		if not os.path.exists(DATA_DIR + input_file):
			print "Error: Data file is not exist\n"
			exit(0)

		input_file = open(DATA_DIR + input_file, 'r')
		lines = input_file.readlines()

		for line in lines:
			arr = line.split(':')
			print arr[0] + '------->' + arr[1]
		print '\n \n'
	
	def parse_Package_List(self,
		input_file,
		):

		if not os.path.exists(DATA_DIR + input_file):
			print "Error: Data file is not exist\n"
			exit(0)

		input_file = open(DATA_DIR + input_file, 'r')
		lines = input_file.readlines()

		for line in lines:
			arr = line.split(':')
			self.app_dic[arr[0]] = arr[1]

def coreTestOptionParser (
	parser,	#OptionParser参数解析对象
	):
	usage = "usage: %prog [-d target]{-t times}"
	parser = OptionParser()
	parser.add_option('-f',  dest = "flyme",
					action="store_true",
					default=False,
					help = "Measure flyme built-in application.")

	parser.add_option('-t', dest = "third",
					action="store_true",
					default=False,
					help = "Measure third part application. ")

	parser.add_option('-l', '--list', dest = "list",
					action="store_true",
					default=False,
					help = "List all the available apps. ")

	parser.add_option('-c', '--num', dest = "num",
					default = 18,
					type = 'int',
					help = "Do [num] times measure, default is 18.")

	parser.add_option('-p', '--prd', dest = "prd",
					type = 'string',
					help = "Specify the measured build version.")

	parser.add_option('-b', '--build', dest = "build",
					type = 'string',
					help = "Specify the measured product(Used for hisory diagram).")

	(options, args) = parser.parse_args()
	coreTestOptionsHandler(options, args)

def coreTestOptionsHandler (
	options,	#命令选项解析对象
	args,	#参数
	):
	test = AppBootUpTime()

	if options.list == True:
		test.list_All_App('flyme_app_list.txt.bak')
		test.list_All_App('third_app_list.txt')
		exit(0)

	if(options.prd == None):
		print "Please specify the measured product. \n"
		print "Usage: ./app_bootup_time.py -p m80 \n"
		exit(0)

	if(options.build == None):
		print "Please specify the measured build version.\n"
		print "Usage: ./app_bootup_time.py -b 2016_03_04 \n"
		exit(0)

	if options.flyme == True:
		test.parse_Package_List('flyme_app_list.txt')
		test.do_Launch_App_Measure_Task(options.num, options.prd, options.build)

	if options.third == True:
		test.parse_Package_List('third_app_list.txt')
		test.do_Launch_App_Measure_Task(options.num, options.prd, options.build)

	if options.flyme == False and options.third == False:
		print "Please specify Measure flyme built-in or third part application.\n"
		print "Usage: ./app_bootup_time.py -f | -t \n"
		exit(1)