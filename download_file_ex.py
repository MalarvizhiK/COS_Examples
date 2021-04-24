from ibm_botocore.client import Config
import ibm_boto3


def main(**kwargs):
    """
    The method that is invoked, when run with CLI arguments

    :param kwargs:
    :return: void
    """
    cos = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='',
    ibm_service_instance_id='',
    ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
    config=Config(signature_version='oauth'),
    endpoint_url='https://s3.us-south.cloud-object-storage.appdomain.cloud')
    try:
       res=cos.download_file(Bucket='test-27-apr', Key='test.txt', Filename='download.txt')
    except Exception as e:
        print(Exception, e)
    else:
        print('File Downloaded')

if __name__ == '__main__':
    main()
