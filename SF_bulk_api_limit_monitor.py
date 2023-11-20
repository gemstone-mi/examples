# Query Salesforce Bulk API for job status
# Search results for id where state != 'Completed' or 'Closed'
import requests
import datetime
import subprocess
import json
import sys
import os
from functions.datadog import dd_post_event
from functions.salesforce_api import sfgetapi

# API call to salesforce bulk api to get job status
results = sfgetapi('https://wexinc.my.salesforce.com/services/data/v57.0/limits')


# Uncomment this section to display the values
#print(json_output["DailyBulkApiBatches"]['Max'])
#print(json_output["DailyBulkApiBatches"]['Remaining'])


# Calculate the percent of the Bulk API Limit remaining
daily_max = results["DailyBulkApiBatches"]['Max']
remaining = results["DailyBulkApiBatches"]['Remaining']
diff = daily_max - remaining

percent_remaining = (remaining / daily_max) * 100
print('Of the Daily Bulk API Max, only ' + f'{percent_remaining:.2f}' + '% remains')

#If the precent remaining is lower than 70% send a warning event to DataDog
if percent_remaining < 70:
    #if the percent remaining is lower than 20% send an error to DataDog
    if percent_remaining < 20:
        dd_post_event('Daily Bulk API Limit', 'Bulk API Limit is ' + f'{percent_remaining:.2f}' + '%', 'Salesforce', 'error', 'Production')
    dd_post_event('Daily Bulk API Limit', 'Bulk API Limit is ' + f'{percent_remaining:.2f}' + '%', 'Salesforce', 'warning', 'Production')       







