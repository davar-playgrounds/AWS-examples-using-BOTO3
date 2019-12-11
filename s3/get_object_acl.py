import logging
import boto3
from botocore.exceptions import ClientError


def get_object_acl(bucket_name, object_name):
    """Retrieve the access control list of an Amazon S3 object.

    :param bucket_name: string
    :param object_name: string
    :return: Dictionary defining the object's access control policy consisting
     of owner and grants. If error, return None.
    """

    # Retrieve the bucket ACL
    s3 = boto3.client('s3')
    try:
        response = s3.get_object_acl(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        logging.error(e)
        return None

    # Return both the Owner and Grants keys
    # The Owner and Grants settings together form the Access Control Policy.
    # The Grants alone form the Access Control List.
    return {'Owner': response['Owner'], 'Grants': response['Grants']}


def main():
    """Exercise get_object_acl()"""

    # Assign these values before running the program
    test_bucket_name = 'BUCKET_NAME'
    test_object_name = 'OBJECT_NAME'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Retrieve the object's current access control list
    acl = get_object_acl(test_bucket_name, test_object_name)
    if acl is None:
        exit(-1)

    # Output the object ACL grantees and permissions
    for grantee in acl['Grants']:
        # The grantee type determines the grantee_identifier
        grantee_type = grantee['Grantee']['Type']
        if grantee_type == 'CanonicalUser':
            grantee_identifier = grantee['Grantee']['DisplayName']
        elif grantee_type == 'AmazonCustomerByEmail':
            grantee_identifier = grantee['Grantee']['EmailAddress']
        elif grantee_type == 'Group':
            grantee_identifier = grantee['Grantee']['URI']
        else:
            grantee_identifier = 'Unknown'
        logging.info(f'Grantee: {grantee_identifier}, '
                     f'Permissions: {grantee["Permission"]}')


if __name__ == '__main__':
    main()
