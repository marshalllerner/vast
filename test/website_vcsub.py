#!/usr/bin/env python

import sys
import copy
import submit_api
import subprocess
import random
import uuid
import getpass
import hashlib

# hsub: Submission script for the Herd Volunteer Computing Project
# lwilson - TACC
# Usage: hsub <launcher_job_file>

def md5(fname):
  hash_md5 = hashlib.md5()
  with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

def BOINCupload(username, auth_code, jobFile, inputFiles=None):
    if inputFiles is None:
        inputFiles = []
    project_url = 'https://herd.tacc.utexas.edu/'
    project_auth = auth_code

    #
    # # Setup the batch
    # breq = submit_api.CREATE_BATCH_REQ()
    # breq.project = project_url
    # breq.authenticator = project_auth
    # breq.app_name = "herd"
    # breq.batch_name = "herd-{}-{}".format(username,uuid.uuid4())
    # breq.expire_time = 0
    # br = submit_api.create_batch(breq)
    # if br.tag == 'error':
    #   print 'ERROR: Unable to create batch: ', br.find('error_msg').text
    #
    # batch_id = int(br.find('batch_id').text)
    # print "hsub: Creating herd batch (id={}, name={})...".format(batch_id, breq.batch_name)
    # batch = submit_api.BATCH_DESC()
    # batch.project = project_url
    # batch.authenticator = project_auth
    # batch.app_name = "herd"
    # batch.batch_id = batch_id
    # batch.jobs = []
    #
    # # Setup the upload request object
    # ufr = submit_api.UPLOAD_FILES_REQ()
    # ufr.project = project_url
    # ufr.authenticator = project_auth
    # ufr.batch_id = batch_id
    # ufr.local_names = []
    # ufr.boinc_names = []
    #
    # #ufr.local_names.append('ZINC02884829-0000.pdbqt')
    # #ufr.boinc_names.append("{}_{}".format(md5('ZINC02884829-0000.pdbqt'),'ZINC02884829-0000.pdbqt'))
    #
    # #print ufr.to_xml()
    # #ufrr = submit_api.upload_files(ufr)
    # #if ufrr[0].tag == 'error':
    # #  print 'error: ', ufrr[0].find('error_msg').text
    #
    # #print 'success'
    #
    #
    #
    # # Iterate through the job file
    # job_file=open(jobFile, "r")
    # #launch_file=open(breq.batch_name, "w")
    #
    # for wu in inputFiles:
    #   job = submit_api.JOB_DESC()
    #   job.files = []
    #   file_ref = ""
    #   file_info = ""
    #   f = submit_api.FILE_DESC()
    #   f.mode = 'local_staged'
    #   #TODO: Get the full path here
    #   m5h = md5(wu)
    #   f.source = "{}_{}".format(m5h,wu.filename)
    #   job.files.append(copy.copy(f))
    #   ufr.local_names.append(wu.filename)
    #   ufr.boinc_names.append("{}_{}".format(m5h, wu.filename))
    #   file_info = file_info + """<file_info>
    # <sticky/>
    # <no_delete/>
    # </file_info>
    # """
    #   file_ref = file_ref + """<file_ref>
    # <open_name>{}</open_name>
    # </file_ref>
    # """.format(wu.filename)
    #
    #   job.rsc_fpops_est = 1e10
    #
    # #     #Identify input files
    # #     for a in wu_args[1:5]:
    # #       if a.startswith("--"):
    # #         #This is an argument flag, ignore
    # #         pass
    # #       else:
    # #         # Describe files for the job
    # #         f = submit_api.FILE_DESC()
    # #         f.mode = 'local_staged'
    # #         m5h = md5(a)
    # #         f.source = "{}_{}".format(m5h,a)
    # #         job.files.append(copy.copy(f))
    # #
    # #         # Establish file info for upload
    # #         ufr.local_names.append(a)
    # #         ufr.boinc_names.append("{}_{}".format(m5h,a))
    # #
    # #         # Add file_ref to input_template
    # #         file_info = file_info + """<file_info>
    # # </file_info>
    # # """
    # #         file_ref = file_ref + """
    # #         <file_ref>
    # #         <open_name>{}</open_name>
    # #         </file_ref>
    # # """.format(a)
    #
    #
    #   job.wu_template = """<input_template>
    #                       {}
    #                       <workunit>
    #                       {}
    #                       <command_line><![CDATA[{}]]></command_line>
    #                       <rsc_disk_bound>5000000000.00</rsc_disk_bound>
    #                       </workunit>
    #                       </input_template>""".format(file_info,file_ref,wu.rstrip())
    #
    #   job.result_template="""<output_template>
    #     <file_info>
    #       <name><OUTFILE_0/></name>
    #       <generated_locally/>
    #       <max_nbytes>50000000</max_nbytes>
    #       <url><UPLOAD_URL/></url>
    #     </file_info>
    #     <result>
    #       <file_name><OUTFILE_0/></file_name>
    #       <open_name>outfile.pdbqt</open_name>
    #     </result>
    #     </output_template>"""
    #   batch.jobs.append(copy.copy(job))
    # #  else:
    #     #Alternative case: simply dump the command into another file to be run by launcher
    # #    launch_file.write(wu)
    #
    # ufrr = submit_api.upload_files(ufr)
    # if ufrr[0].tag == 'error':
    #   print 'error: ', ufrr[0].find('error_msg').text
    #   return "There was an error: " + ufrr[0].find('error_msg').text
    #
    # r = submit_api.submit_batch(batch)
    # return r[0].tag, r[0].find('error_msg').text
