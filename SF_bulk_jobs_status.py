# Query Salesforce Bulk API for job status
# Search results for id where state != 'Completed' or 'Closed'
import requests
import datetime
import subprocess
import csv
import json
import sys
import os
from functions.datadog import dd_post_event
from functions.salesforce_api import sfgetapi

# API call to salesforce bulk api to get job status
#url = 'https://wexinc.my.salesforce.com/services/data/v57.0/jobs/query'
results = sfgetapi('https://wexinc.my.salesforce.com/services/data/v57.0/jobs/query')

#Parse the json output to get the job id and status
#json_output = r.json()

#loop through the json output and print the job id and status
print("---Salesforce Jobs----")
for job in results["records"]:     
      if job['state'] != "Closed":
        print (job['id'] + ' ' + job['operation'] + ' ' + job['object'] + ' ' + job['state'] + '\n')
        dd_post_event('Running Jobs', job['id'] + ' ' + job['operation'] + ' ' + job['object'] + ' ' + job['state'], 'Salesforce', 'info', 'Production')

#  Uncomment this section to turn on monitoring for Talend jobs   
###
#print("\n---Talend Jobs----")
#for job in results["records"]: 
#      if "externalIdFieldName" in job:
#        if job['externalIdFieldName'] == "Talend_External_ID__c":
#          print (job['id'] + ' ' + job['operation'] + ' ' + job['object'] + ' ' + job['externalIdFieldName'] + ' ' + job['state'] + '\n')
#          dd_post_event('Talend Jobs',job['id'] + ' ' + job['operation'] + ' ' + job['object'] + ' ' + job['externalIdFieldName'] + ' ' + job['state'],'salesforce','info','prod')
###

print("\n---Jobs w/ Failed Records----")
for job in results["records"]: 
      if "numberRecordsFailed" in job:
        print (job['id'] + ' ' + job['operation'] + ' ' + job['object'] + ' ' + job['numberRecordsFailed'] + ' ' + job['state'] + '\n')
        dd_post_event('Failed Job', job['id'] + ' ' + job['operation'] + ' ' + job['object'] + ' ' + job['numberRecordsFailed'] + ' ' + job['state'], 'Salesforce', 'error', 'Production')









