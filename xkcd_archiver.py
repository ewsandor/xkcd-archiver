#!/bin/python
# XKCD Comic Archiver
# xkcd_archiver.py
# Edward Sandor, January 2023 

import os
import sys, getopt
import datetime
from   urllib.parse import urlparse
import urllib.request, json 

version_str="0.0.1"
publish_year_str="January 2023"
author_str="Edward Sandor"

title_block_str="XKCD Archiver\n" \
                "Version " + version_str + "\n" \
                 + author_str + ", " + publish_year_str

def main(argv):

    #Init working variables
    i = 0
    output_dir = "xkcd_archive/"
    exclusion_list=[0, 404] # Comics are numbered from #1.  404 was never published (404 not found joke.).

    help_string=title_block_str + "\n\n" \
                "This script archives all xkcd comics directly from the website.\n\n" \
                "Arguments:\n" \
                "   -i <n>,    --initial_comic=<n>  Download all comics starting with #<n>.  If this argument is not provided, this script will start with comic #1.\n" \
                "   -d <path>, --directory=<path>   Output directory for comic archive." \

    #Parse command line arguments
    try:
        opts, args = getopt.getopt(argv,"hi:d:",["help", "initial_comic=", "directory="])
    except getopt.GetoptError as err:
        print(err)
        print("\n"+help_string)
        sys.exit(22)

    for opt, arg in opts:
       if opt in ('-i', "--initial_comic"): 
           i = int(arg)
       if opt in ('-d', "--directory"): 
           output_dir = arg
       elif opt in ('-h', "--help"): 
           print(help_string)
           sys.exit()

    #Validate Arguments
    if(os.path.exists(output_dir)==False):
        print("Output directory '" + output_dir + "' is inaccessible or does not exist.")
        sys.exit(2)

    #Take timestamp for session
    timestamp_str=str(datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())

    #Output archiving summary
    archive_summary_str=(title_block_str + "\n\n" \
                         "Archiving at " + timestamp_str + " starting with comic #" + str(i) +".  Excluding comics " + str(exclusion_list)+ ".\n" \
                         "Output directory: " + output_dir)
    print(archive_summary_str+"\n")
    with open(os.path.join(output_dir, "archive_summary.txt"), "w") as text_file:
        text_file.write(archive_summary_str)

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
