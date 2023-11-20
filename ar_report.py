# run a soql query against salesforce using the salesforce cli tool and write the results in a csv file
# usage: soql.py <query>
# example: soql.py "select id, name from account limit 10"
# prompt for Salseforce Org



import sys
import os
import subprocess
import csv
import json
import requests
import datetime

org = "Production"

#prompt for the month and day to start the report
month = input("Enter the month to start the report (mm): ")
day = input("Enter the day to start the report (dd): ")





# get query from command line
query = "SELECT CreatedBy.Name, Parent.Account_Name_Text__c, Parent.Name, Parent.Approved_Credit_Limit__c FROM Application_Request__History WHERE (CreatedBy.Name = 'Garnet Merrill' OR CreatedBy.Name = 'Enio Ribeiro' OR CreatedBy.Name = 'Jeremy Olson' OR CreatedBy.Name = 'Frederick Straub' OR CreatedBy.Name = 'Nick Edwards' ) AND CreatedDate >= 2023-" + month + "-" + day + "T00:00:00Z"

# run soql query using salesforce cli tool
# note: the --json flag is not available in all versions of the cli tool
# so you may need to upgrade to the latest version
# https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_install_cli.htm
# filter uniqe results and write to csv file and count the number of records returned and total the credit limit
#cmd = 'sf  data query -o ' + org + ' -q "' + query + '" --json | jq -r ".result.records | .[] | [.CreatedBy.Name, .Parent.Account_Name_Text__c, .Parent.Name, .Parent.Approved_Credit_Limit__c] | @csv" | sort --unique > ar_report.csv'

# filter uniqe results and write to csv file and count the number of records returned and total the credit limit
cmd = 'sf  data query -o ' + org + ' -q "' + query + '" --json | jq -r ".result.records | .[] | [.CreatedBy.Name, .Parent.Account_Name_Text__c, .Parent.Name, .Parent.Approved_Credit_Limit__c] | @csv" | sort --unique > ar_report.csv'

#print(cmd)
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

# count the number of records returned and total the credit limit as currency
with open('ar_report.csv', 'r') as f:
    reader = csv.reader(f)
    count = 0
    total = 0
    for row in reader:
        count += 1
        total += float(row[3])
     #   print(row[2] + ' ' + row[3] + ' ' + ' Total Credit Limit: ' + str('${:,.2f}'.format(total)))

    print('-----Summary-----')
    print('Total # of ARs: ' + str(count))   
    print('Total Credit Limit: ' + str('${:,.2f}'.format(total)))

















    
    







    






















