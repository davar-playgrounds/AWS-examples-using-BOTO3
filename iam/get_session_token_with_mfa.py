import boto3

# Prompt for an MFA time-based one-time password (TOTP)
mfa_TOTP = input('Enter the MFA code: ')

# Create an STS client
sts_client = boto3.client('sts')

# Get temporary credentials for an AWS account or IAM user.
# Replace MFA_DEVICE with the virtual MFA device ID for the user. Alternatively, set the
# SerialNumber string to the serial number of the MFA hardware device, such as
# SerialNumber='GAHT12345678'.
response = sts_client.get_session_token(DurationSeconds=3600,   # Credentials valid for one hour
                                        SerialNumber='arn:aws:iam::MFA_DEVICE:mfa/user',
                                        TokenCode=mfa_TOTP)

# Reference the temporary credentials section of the response
tempCredentials = response['Credentials']

# Use the temporary credentials to create an S3 client that can access the
# external account.
s3_client = boto3.client('s3',
                         aws_access_key_id=tempCredentials['AccessKeyId'],
                         aws_secret_access_key=tempCredentials['SecretAccessKey'],
                         aws_session_token=tempCredentials['SessionToken'])

# Replace BUCKET_NAME with a bucket that exists on the external account
bucket_name = 'BUCKET_NAME'
# List the objects in the external account's bucket. The user's
# permissions must allow this type of S3 access.
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
except Exception as e:
    print(f'ERROR: Could not find bucket {bucket_name}')
else:
    print(f'Objects in {bucket_name}')
    for obj in response['Contents']:
        print(f'   {obj["Key"]}')