# appBootupSpeed
This is a app bootup speed auto test tool.

### Prepare:
1. Install Python
Download link:https://www.python.org/downloads/release/python-2710/

2. Install xlsxwriter
xlsxwriter Home Page:http://xlsxwriter.readthedocs.org/getting_started.html
use command line: pip install XlsxWriter

### How To Use:
Run as command line: 
python ./bootuptest.py runtest | show
runtest:
Usage: bootuptest.py [options]

Options:
  -h, --help            show this help message and exit
  -f                    Measure flyme built-in application.
  -t                    Measure third part application.
  -l, --list            List all the available apps.
  -c NUM, --num=NUM     Do [num] times measure, default is 18.
  -p PRD, --prd=PRD     Specify the measured build version.
  -b BUILD, --build=BUILD
                        Specify the measured product(Used for hisory diagram).

show:
Usage: bootuptest.py [options]

Options:
  -h, --help            show this help message and exit
  -z, --zhow            Show all app name.
  -d DATE, --date=DATE  Show diagram for specific date.
  -p PRODUCT, --product=PRODUCT
                        Specify the showed product.
  -a APP, --app=APP     Show diagram for specific app.
  -l LIST, --list=LIST  Show all data for specific product.
