# VAST

VAST is a server-side application for submitting simple, data parallel, high throughput computing (HTC) workflows to BOINC, an open-source software platform for computing using volunteered resources, and Launcher, a utility that performs the workflows on clusters, massively parallel processor (MPP) systems, workgroups of computers, and personal machines.

## Connecting to VAST
After setting up an account on TODO, sign on to the server by sending a request to api.vast.utexas.edu

## Starting the server
download Mongodb
  start it using "sudo service mongod start" or "sudo service mongodb start"
navigate to the vast directory
  download the venv if the files included don't workflows
    type ". venv/bin/activate"
  type "export FLASK_APP=test/VAST.py"
  if wanting to debug, type "export FLASK_DEBUG=1"
  type "flask run"
