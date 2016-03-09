#! /usr/bin/python
#-*- coding:utf-8 -*-

import sys
import string
import os
import xlsxwriter
from operator import itemgetter, attrgetter

class OneAppTime(object):

	def __init__(self,
		excel_name,
		app_name,
		product
		):
		workbook = xlsxwriter.Workbook(excel_name)
		self.workbook = workbook
		self.app_name = app_name
		self.product_name = product + '/'
		self.app_time_dic = {}

	def add_chart(self,
		line_size,
		):
		chart = self.workbook.add_chart({'type' : 'column'})
		chart.set_title({'name': 'Results of ' + self.app_name +' BootUp Time'})
		chart.set_x_axis({'name': 'App Name'})
		chart.set_y_axis({'name': 'Time (ms)'})
		chart.set_size({'width': 577, 'height': 287})    #设置图表大小
		chart.add_series({
			'name':          '=Sheet1!$A$1',
			'categories': '=Sheet1!$A$2:$A$' + str(line_size),
			'values':        '=Sheet1!$B$2:$B$' + str(line_size),
			})
		self.worksheet.insert_chart('D13', chart)

	def write_excel(self,
		):
		sheet_sn = self.workbook.add_worksheet()
		self.worksheet = sheet_sn
		headings = ['Version', 'Time']
		bold = self.workbook.add_format({'bold': True})
		self.worksheet.write_row('A1', headings, bold)

		count = 1
		for line in self.app_time_dic:
			self.worksheet.write(count, 0, line[0].strip())
			self.worksheet.write(count, 1, int(line[1].strip()))
			count += 1

		if(count-1 < 6):
			print "History data at least 6 times, now is %s" %(count-1)
			exit(1)
		self.add_chart(count)

	def parse(self,
		input_file_name,
		):

		input_file = open(self.product_name + input_file_name, 'r')
		lines = input_file.readlines()

		for line in lines:
			if self.app_name in line:
				arr = []
				arr = line.split(':')
				self.app_time_dic[input_file_name.rstrip('_data.txt')] = arr[1]

	def allParse(self):
		count = 1
		for filename in os.listdir(os.path.dirname(self.product_name)):
			if filename.endswith(".txt"):
				self.parse(filename)

		self.app_time_dic = sorted( self.app_time_dic.iteritems(), key=itemgetter(0), reverse=False ) #按照时间排序
		self.write_excel()
		self.finish()
		print 'Success create a xls file: %s-%s.xlsx' %(self.product_name.rstrip('/'), self.app_name)

	def finish(self):
		self.workbook.close()

if __name__ == '__main__':
	te = OneAppTime('tempdata.xlsx',  'Reader', 'm80')
	te.allParse()