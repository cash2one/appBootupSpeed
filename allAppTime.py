#! /usr/bin/python
#-*- coding:utf-8 -*-

import sys
import string
import os
import xlsxwriter

class AllAppTime(object):
	
	def __init__(self,
		excel_name,
		product,
		version,
		):
		workbook = xlsxwriter.Workbook(excel_name)
		self.workbook = workbook
		self.product_name =  product
		self.build_version = version

	def add_chart(self,
		line_size,
		):
		chart = self.workbook.add_chart({'type' : 'column'})
		chart.set_title ({'name': 'Results of App BootUp Time'})
		chart.set_x_axis({'name': 'App Name'})
		chart.set_y_axis({'name': 'Time (ms)'})
		chart.add_series({
			#'name':          '',
			'categories': '=Sheet1!$A$2:$A$' + str(line_size),
			'values':        '=Sheet1!$B$2:$B$' + str(line_size),
			})
		self.worksheet.insert_chart('D13', chart)

	def parse(self,
		input_file,
		):

		count = 1
		sheet_sn = self.workbook.add_worksheet()
		self.worksheet = sheet_sn
		headings = ['App', 'Time']
		bold = self.workbook.add_format({'bold': True})
		self.worksheet.write_row('A1', headings, bold)
		
		input_file = open(input_file, 'r')
		lines = input_file.readlines()
		
		for line in lines:
			arr = []
			arr = line.split(':')
			self.worksheet.write(count, 0, arr[0])
			self.worksheet.write(count, 1, int(arr[1].strip()))
			count += 1
	
		self.add_chart(count)

	def allParse(self):
		self.parse(self.product_name + '/' + self.build_version + '_data.txt')
		self.finish()
		print 'Success create a xls file: %s-%s.xlsx' %(self.product_name.rstrip('/'), self.build_version)

	def finish(self):
		self.workbook.close()

if __name__ == '__main__':
	te = AllAppTime('tempdata.xlsx', 'm80', '2016_03_03')
	te.allParse()
