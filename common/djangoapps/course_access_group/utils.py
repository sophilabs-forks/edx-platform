from django.conf import settings
from simple_salesforce import Salesforce

def grab_salesforce_data():
	username = settings.APPSEMBLER_FEATURES['SALESFORCE_USERNAME']
	password = settings.APPSEMBLER_FEATURES['SALESFORCE_PASSWORD']
	token = settings.APPSEMBLER_FEATURES['SALESFORCE_TOKEN']

	sf = Salesforce(password=password, username=username, security_token=token)
	query_result = sf.query("SELECT Email_Domain__c FROM Account WHERE Type='Partner'")

	#returns list of valus from salesforce (up to 2000)
	#TODO: deal with entries > 2000
	#TODO: filter out uniques
	return query_result['records']
