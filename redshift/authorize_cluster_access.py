import boto3
from botocore.exceptions import ClientError


def authorize_cluster_access(IpAddress='0.0.0.0/0'):
    """Enable access to Amazon Redshift clusters

    Defines a security group inbound rule for the default VPC. The rule
    enables access to Redshift clusters by IP addresses referenced in the
    IpAddress argument. To define the rule, EC2 permissions are required.

    :param IpAddress: string; IP addresses to authorize access to Redshift
    clusters. Default: '0.0.0.0/0' allows access from any computer, which is
    reasonable for demonstration purposes, but is not appropriate in a
    production environment.
    :return: True if cluster access is enabled, else False
    """

    ec2_client = boto3.client('ec2')

    # Redshift uses port 5439 by default. If Redshift was configured to use
    # a different port, specify the FromPort= and ToPort= arguments accordingly.
    try:
        ec2_client.authorize_security_group_ingress(GroupName='default',
                                                    IpProtocol='tcp',
                                                    FromPort=5439,
                                                    ToPort=5439,
                                                    CidrIp=IpAddress)
    except ClientError as e:
        print(f'ERROR: {e}')
        return False
    return True

def main():
    """Test authorize_cluster_access()"""
    if not authorize_cluster_access():
        print('FAIL: authorize_cluster_access()')
        exit(1)


if __name__ == '__main__':
    main()
