from functions.salesforce_api import sfauth
from simple_salesforce import Salesforce


#separator = " "
#SF_USER = os.getenv('SF_USER')
#PASS= os.getenv('PASS')
#TOKEN = os.getenv('TOKEN')

#Print Secrets

#print (separator.join(PASS))
#print (separator.join(TOKEN))
#print(separator.join(SF_USER))
      
#Set the URL
#sf = Salesforce(instance_url='https://gemstone-dev-ed.my.salesforce.com/', session_id='')

#Authenticate
#sf = Salesforce(username=SF_USER, password=PASS, security_token=TOKEN)

sf=sfauth()
#Create a Contact
sf.Contact.create({'LastName':'Bunny','Email':'BBunny@gemstone.com'})
