#! /usr/bin/python
#-*- coding:utf-8 -*-

from optparse import OptionParser
import os
import sys
import string
from oneAppTime import OneAppTime
from allAppTime import AllAppTime

def listAllApp(
	input_file_name,
	):
	if not os.path.exists('database/' + input_file_name):
		print "Error: Data file is not exist\n"
		exit(0)

	input_file = open('database/' + input_file_name, 'r')
	lines = input_file.readlines()
	arr = []
	print input_file_name
	for line in lines:
		arr.append(line.split(':')[0])
	print '%s \n' %arr

def listAllData(
	product
	):
	if not os.path.exists(os.path.dirname(product+'/')):
		print "Error: %s data file is not exist!\n" %product
		exit(1)
	for filename in os.listdir(os.path.dirname(product+'/')):
		if filename.endswith(".txt"):
			print filename

def coreShowOptionsHandler (
	options,	#命令选项解析对象
	args,		#参数
	):
	
	if options.zhow == True:
		listAllApp('flyme_app_list.txt')
		listAllApp('third_app_list.txt')
		exit(0)
	
	if(options.list != None):
		listAllData(options.list)
		exit(0)
		
	if(options.product == None):
		print "Please specify the measured product. \n"
		print "Usage: ./app_bootup_time.py -p m80 \n"
		exit(0)
	if(options.date != None and options.app != None):
		print "Error: please specify one mode"
		exit(0)
	elif(options.date != None and options.app == None):
		show = AllAppTime(options.product+'-'+options.date+'.xlsx', options.product, options.date)
		show.allParse()
		exit(0)
	elif(options.date == None and options.app != None):
		show = OneAppTime(options.product+'-'+options.app+'.xlsx', options.app, options.product)
		show.allParse()
		exit(0)
	else:
		print '''
			Usage: 
			1.  ./bootuptest.py show -p m80 -a [app_name]
					Show all app_name :  ./bootuptest.py show -z
			2.  ./bootuptest.py show -p m80 -d [date]
					Show all date data :  ./bootuptest.py show -l m80
		''' 
		exit(0)

def coreShowOptionParser (
	parser,	#OptionParser参数解析对象
	):

	parser.add_option('-z', '--zhow', dest = "zhow",
					action="store_true",
					default=False,
					help = "Show all app name.\n")

	parser.add_option('-d', '--date', dest = "date",
					type = 'string',
					help = "Show diagram for specific date.\n")
	
	parser.add_option('-p', '--product', dest = "product",
					type = 'string',
					help = "Specify the showed product.\n")
	
	parser.add_option('-a', '--app', dest = "app",
					type = 'string',
					help = "Show diagram for specific app.\n")

	parser.add_option('-l', '--list', dest = "list",
					type = 'string',
					help = "Show all data for specific product.\n")

	(options, args) = parser.parse_args()
	coreShowOptionsHandler(options, args)
