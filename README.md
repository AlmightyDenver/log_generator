# log_generator


## Description

### Purpose
I made this programme because I needed sample log when testing data collection.

### The Details
Optionally, can select log file type,  time field location, time field format, and the log directory. (See Usage below)

"<Date>_Log_Generator.<log_format>" The log file is created in this format. 1 log occurs every second. If you want to modify file name, generation cycle, you need to edit code.

 There is a 5% chance of generation log of more than 10,000 characters.

                                                                                                                                                                                                                                ## Envir
python 3

## Prerequisite

Faker=13.3.4
numpy=1.19.5
dicttoxml==1.7.4



### Files
log_Gen.py : Generating Programme
Generated Log Sample : Sample Log fiels

  
  
## Usage

set log file directory
  `python logGen.py -p <my/log/path>`

set log format
  `python logGen.py -l <csv|xml|txt|json>`

set time field format
1 - %Y-%m-%d %H:%M, 2 - %Y/%m/%d %H:%M:%S
	`python logGen.py -tf <1|2>`

set time field order
	`python Log Gen.py -t <0|1|...|7>``

