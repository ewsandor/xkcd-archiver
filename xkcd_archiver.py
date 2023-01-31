#!/bin/python
# XKCD Comic Archiver
# xkcd_archiver.py
# Edward Sandor, January 2023 

import os
import sys, getopt
from   urllib.parse import urlparse
import urllib.request, json 

def main(argv):

    #Init working variables
    i = 0
    output_dir = "xkcd_archive/"
    exclusion_list=[0, 404]

    help_string="XKCD Archiver\n" \
                "This script archives all xkcd comics directly from the website.\n\n" \
                "Arguments:\n" \
                "   -i <n>,    --initial_comic=<n>  Download all comics starting with #<n>.  If this argument is not provided, this script will start with comic #1.\n" \
                "   -d <path>, --directory=<path>   Output directory for comic archive." \

    #Parse command line arguments
    try:
        opts, args = getopt.getopt(argv,"hi:d:",["help", "initial_comic=", "directory="])
    except getopt.GetoptError:
        print("Unrecognized Input!\n")
        print(help_string)
        sys.exit(22)

    for opt, arg in opts:
       if opt in ('-i', "--initial_comic="): 
           i = int(arg)
       if opt in ('-d', "--directory="): 
           output_dir = arg
       elif opt in ('-h', "--help"): 
           print(help_string)
           sys.exit()

    if(os.path.exists(output_dir)==False):
        print("Output directory '" + output_dir + "' is inaccessible or does not exist.")
        sys.exit(2)

    #Archive all xkcd comics starting at i until error (e.g. 404)
    while(True):
        if(i not in exclusion_list):
            with urllib.request.urlopen("https://xkcd.com/"+str(i)+"/info.0.json") as url:
                print("Archiving comic #"+str(i))
                data = json.load(url)
                with open(os.path.join(output_dir,"{:05d}".format(i)+"_info.0.json"), 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print("Image path "+data["img"])
                #print(data)
                parsed_url = urlparse(data["img"])
                if(len(os.path.basename(parsed_url.path)) > 0):
                    urllib.request.urlretrieve(data["img"], os.path.join(output_dir,"{:05d}".format(i)+"_comic_"+os.path.basename(parsed_url.path)))
        else:
            print("Skipping comic #"+str(i))
        i=i+1

if __name__ == "__main__":
   main(sys.argv[1:])
