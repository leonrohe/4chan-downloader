import os
import time
import requests
from bs4 import BeautifulSoup

url = input("Enter the URL of the 4chan thread. \n")

## get response from url
r = requests.get(url)

## create soup out of html text
soup = BeautifulSoup(r.text, "html.parser")

## get current working directory
cwd = os.getcwd()

folder_title = ""

## find thread subject, if exists
thread_subject = soup.find(class_="subject").text

## set name of folder to create
if thread_subject != "":
    folder_title = thread_subject
else:
    folder_title = str(int(time.time()))
    print("<WARNING> Could not parse Thread Subject. Temporary folder name was given")

## create folder path
dir = os.path.join(cwd, folder_title)

## create folder
try:
    os.mkdir(dir)
except:
    print("<WARNING> Could not create folder: " + dir + " .Maybe it already exists?")

## get all media from thread
media_all = soup.find_all(class_="fileThumb")
file_count = len(media_all)

print("Found " + str(file_count) + " downloadable media files. Starting to download ...")

## loop through all media files and save them to folder
z = 0
for media in media_all:

    print("Progress: " + str(z) + "/" + str(file_count), end='\r')

    link = "https:" + media.get("href")
    filetype = os.path.splitext(link)[1]

    f = open(dir + "/" + str(z)+filetype, "wb")
    rr = requests.get(link)
    f.write(rr.content)
    f.close()
    z = z + 1