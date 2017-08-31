#!/usr/bin/env python

import os
import sys
import subprocess
from subprocess import CalledProcessError
import commands
import shutil
import submit_api
import random
import uuid
import getpass
import hashlib

class CommandNotFoundException(Exception): #if the command is not found
  pass
#checks if the user inputted a job file or too many files
if len(sys.argv) < 2 or len(sys.argv) > 2:
  print "Usage: getInputFiles <job_file>"
  raise EnvironmentError("Too many or not enough variables. Exiting")
  exit(1)



# Used to see if a job can be offloaded to BOINC by looking at the command
# (e.g. "echo" from "echo 'Hello World'", "./start_launcher_BOINC" from
# "./start_launcher_BOINC <Job_File>"). The offloadable jobs are static
# executables that are in ELF format and dynamic executables that only contain
# standard libraries (/lib, /lib64, and/or /usr)
#
# param fileName - a string containing a single command line job (e.g. "echo 'Hello World'")
#
# returns true or false depending on if the job can be offloaded to BOINC, and
# raises an error if there is no command on the specific inputted line
def can_offload(fileName):
  try:
    good_path = subprocess.check_output(["which", fileName])[:-1]
    if "ELF" in subprocess.check_output(["file", good_path]):
      #os.access(fileName, os.X_OK)
      try:
        libs = subprocess.check_output(["ldd", good_path])
      except subprocess.CalledProcessError:
        return True
      libArr = libs.split("\n")
      for lineNum in range(1, len(libArr) - 1):
        if any(possibilities in libArr[lineNum] for possibilities in ("/lib/", "/lib64/", "/usr/")):
          continue
      #    raise DynamicNonStandardException("%s contains more than just standard libraries %s" %(fileName, libArr[lineNum]))
      #   I wasn't sure if there should be an error thrown or it should just return false.
        return False
      shutil.copy2(good_path, newpath)
      return True
    else:
      return False
  except subprocess.CalledProcessError:
    raise CommandNotFoundException("Command was not found")


newpath = './inputFiles'
if not os.path.exists(newpath):
    os.makedirs(newpath)
#Iterate through the job file
print("The program will now determine which files can be offloaded to VAST" +
      "and add its input files to the folder ./inputFiles ")
print
file_object = open(sys.argv[1])
for line in file_object.readlines():
  try:
    wu_args=line.split(" ")
    if can_offload(wu_args[0].rstrip()) and len(wu_args) > 1:
        for a in wu_args[1:]: #TODO: how many arguments should be the maximum?
            if a.startswith("--"):
                #This is an argument flag, ignore
                pass
            else:
                try:
                    good_path = subprocess.check_output(["which", a.rstrip()])[:-1]
                    if os.path.isfile(good_path):
                        shutil.copy2(good_path, newpath)
                except CalledProcessError:
                    continue
  except IndexError:
    print("There was a line with no command. Skipping this line.")
  except CommandNotFoundException:
    print("The line `{}` contained an error with the command. Skipping this line.".format(line[:-1]))
