#!/bin/bash

NS='\e[0m' # NO STYLE
blue='\e[0;34m'
red='\e[0;91m'
green='\e[92m'
bold='\e[1m'


#UNCOMMENT NEXT 4 LINES FOR STANDALONE SCRIPT.
#echo -e "${blue}${bold}Please enter the immediate sub-directory of your zip-files:${NS}"
#read zips_dir
#echo ""
#cd "$zips_dir"


echo ""
echo -e "${blue}${bold}running unzip.sh.....${NS}"
echo ""
cd "$1" #change working directory to first argument provided to the script.

# add a unique id to every folder extracted
# in case some students named theyr zip folders by the same name.
# this also shows the order in which folders are extracted.
declare -i uniqueId=1

for file in *.zip;
  do
        if [ "$file" == "*.zip" ]
        then #exit if there are no zip files in the directory.
          echo -e "${red}No .zip files in directory.\nAborting.${NS}"
          exit 0
        else
          dir=$(basename "$uniqueId$file" .zip) # remove the .zip from the filename
          mkdir "$dir"
          cd "$dir" && unzip ../"$file" && rm ../"$file" # unzip and remove file if successful
          cd ..
          ((uniqueId++))
        fi
  done

echo -e "${green}Done.${NS}"
