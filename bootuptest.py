#! /usr/bin/python
#-*- coding:utf-8 -*-

import sys
from optparse import OptionParser
from testParser import coreTestOptionParser
from showParser import coreShowOptionParser

parser = OptionParser()

#解析参数
def parseArgs ():
	if len(sys.argv) == 1:
		print '''
	Please select at least one subsytem.
			
	'runtest' or 'show'?
		'''
		exit(1)

	arg1 = sys.argv[1]
        if arg1 == 'runtest':
                coreTestOptionParser(parser)
        elif arg1 == 'show':
                coreShowOptionParser(parser)
        else:
                print "\nUnkonwn subsystem '%s' found，please correct it. \n" % arg1

        return

if __name__ == '__main__':
        parseArgs()