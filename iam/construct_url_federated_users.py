import urllib.parse
import json
import requests
import boto3

# Create an STS client
sts_client = boto3.client('sts')

# Assume a role defined on an external account. The role specifies the
# permissions that are allowed on the account.
# Replace EXTERNAL_ACCOUNT_NUMBER with the account number of the external
# account.
# Replace ROLE_NAME with the name of the role defined on the external account.
# Optional, but recommended: Specify a unique ExternalId= string assigned by
# the external account.
response = sts_client.assume_role(RoleArn='arn:aws:iam::EXTERNAL_ACCOUNT_NUMBER:role/ROLE_NAME',
                                  RoleSessionName='AssumeRoleSession1')

# Reference the temporary credentials section of the response
tempCredentials = response['Credentials']

# Construct the required JSON structure using the temporary credentials
session_json = '{'
session_json += '"sessionId":"' + tempCredentials['AccessKeyId'] + '",'
session_json += '"sessionKey":"' + tempCredentials['SecretAccessKey'] + '",'
session_json += '"sessionToken":"' + tempCredentials['SessionToken'] + '"'
session_json += '}'

# Make request to AWS federation endpoint to get sign-in token.
# Construct the parameter string with the sign-in action request,
# a 12-hour session duration, and the JSON document with temporary
# credentials.
request_parameters = '?Action=getSigninToken'
request_parameters += '&SessionDuration=43200'
request_parameters += '&Session=' + urllib.parse.quote_plus(session_json)
request_url = 'https://signin.aws.amazon.com/federation' + request_parameters
response = requests.get(request_url)
# Returns a JSON document with a single element named SigninToken.
signin_token = json.loads(response.text)

# Create URL where the sign-in token is used to sign into the AWS Console
request_parameters = '?Action=login'
request_parameters += '&Issuer=Example.org'
request_parameters += '&Destination=' + urllib.parse.quote_plus('https://console.aws.amazon.com/')
request_parameters += '&SigninToken=' + signin_token['SigninToken']
request_url = 'https://signin.aws.amazon.com/federation' + request_parameters

# Send final URL to stdout
print(request_url)