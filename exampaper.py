# A python program created to batch download past exam papers from the DCU repository
# Run environment:
# Ubuntu 18.04
# Visual Studio Code
# Python 3.6.9

import requests, csv, json, io, sys, os, shutil, argparse, urllib.request

def progress(count, total, status=''):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def stringtofloat(stringwithfloat):
    try:
        return float(stringwithfloat)
    except ValueError:
        return 0.0

parser = argparse.ArgumentParser(description='Download Batch DCU Exam papers')
parser.add_argument("-m", required=True, help="Input Your Modules Seperated by a comma")
parser.add_argument("-r", help="Boolean statement if you want to include repeat exams. Default: Yes", default="Yes")
parser.add_argument("-d", help="Directory You Want to Download Files to", default="./exampapers/")
parser.add_argument("-y", help="Specify the year you want to go back to", default="0")
parser.add_argument("-v", help="Verbose, if you want to include debug messages. Default: False", default="no")

try:
    options = parser.parse_args()
    module_arr = options.m
    repeat_boolean_string = options.r
    dir = options.d
    year = float(options.y)
    debug = options.v
except:
    parser.print_help()
    sys.exit(0)

if str.lower(repeat_boolean_string) == "y" or str.lower(repeat_boolean_string) == "yes" or str.lower(repeat_boolean_string) == "t" or str.lower(repeat_boolean_string) == "true" or str.lower(repeat_boolean_string) == "on":
    repeat_bool = True
else:
    repeat_bool = False

if str.lower(debug) == "y" or str.lower(debug) == "yes" or str.lower(debug) == "t" or str.lower(debug) == "true" or str.lower(debug) == "on":
    debug = True
else:
    debug = False

if os.path.isdir(dir):
    print("Folder Found Deleting previous folder")
    try:
        shutil.rmtree(dir)
    except:
        print('Error while deleting directory')

if debug == True:
    print("m argument is " + module_arr)

module_list = module_arr.split(",")


if debug == True:
    for x in module_list:
        print(x)

response = requests.get('https://docs.google.com/spreadsheet/ccc?key=1CFYESIf92lMHY4K-cQne0xvD-gb1CMsz8I0NiXGQN8g&output=csv')
assert response.status_code == 200, 'Wrong status code'

temp_data = response.text
temp_data = temp_data.replace("\"<a href=\'https://drive.google.com/file/d/", "").replace("/view?usp=sharing'target=\"\"_blank\"\">Click here to open</a>\"", "")

# data[row][column]
# column equals 0 = Module Code
# column equals 1 = Year
# column equals 2 = Google Drive Key 

data=list(csv.reader(io.StringIO(temp_data)))

length_of_list = len(data)

counter = 0

for z in module_list:
    for i in range(0, length_of_list):
        if repeat_bool == True:
            if stringtofloat(data[i][1]) >= year:
                if z in str(data[i][0]):   
                    if debug == True:
                        print(data[i][0] + "  " + data[i][1]+ "  " + data[i][2])
                    counter = counter + 1
        else:
            if stringtofloat(data[i][1]) >= year:
                if str(data[i][0]) == z:
                    if debug == True:
                        print(data[i][0] + "  " + data[i][1]+ "  " + data[i][2])
                    counter = counter + 1


if debug == True:
    print("Counter Value = " + str(counter))
counter2 = 0

if counter == 0:
    print("Could not find any exam papers, make sure you have entered your Module Code correctly")
    sys.exit(0)

for z in module_list:
    for i in range(0, length_of_list):
        if repeat_bool == True:
            if stringtofloat(data[i][1]) >= year:
                if z in str(data[i][0]):
                    if os.path.isdir(dir+data[i][0]) == False:
                        try:
                            os.makedirs(dir+data[i][0])
                        except OSError:
                            print ("Creation of the directory %s failed" % dir+data[i][0])
                    
                    counter2 = counter2 + 1
                    progress(counter2, counter, "Downloading Exam Papers")
                    sys.stdout.flush()

                    
                    URL = "https://drive.google.com/uc?export=download&id="+data[i][2]
                    try:
                        urllib.request.urlretrieve(URL, dir+data[i][0]+"/"+data[i][0]+"_"+data[i][1]+".pdf")
                    except URLERROR:
                        print("Failed to Download " + data[i][0] + "_" + data[i][1] + ".pdf")

        else:
            if str(data[i][0]) == z:
                if stringtofloat(data[i][1]) >= year:
                    if os.path.isdir(dir+data[i][0]) == False:
                        try:
                            os.makedirs(dir+data[i][0])
                        except OSError:
                            print ("Creation of the directory %s failed" % dir+data[i][0])
                    
                    counter2 = counter2 + 1
                    progress(counter2, counter, "Downloading Exam Papers")
                    sys.stdout.flush()

                    
                    URL = "https://drive.google.com/uc?export=download&id="+data[i][2]
                    try:
                        urllib.request.urlretrieve(URL, dir+data[i][0]+"/"+data[i][0]+"_"+data[i][1]+".pdf")
                    except URLERROR:
                        print("Failed to Download " + data[i][0] + "_" + data[i][1] + ".pdf")

                # else:
                #     print("directory already exists lol")



