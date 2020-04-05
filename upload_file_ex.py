from ibm_botocore.client import Config
import ibm_boto3


def main(**kwargs):
    """
    The method that is invoked, when run with CLI arguments

    :param kwargs:
    :return: void
    """
    cos = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='xx-xxx',
    ibm_service_instance_id='xx-xx-xx-xx-xxx',
    ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
    config=Config(signature_version='oauth'),
    endpoint_url='https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints')
    try:
        res=cos.upload_file(Filename='test.txt', Bucket='cloud-object-storage-8w-cos-standard-c5u',Key='test.txt')
    except Exception as e:
        print(Exception, e)
    else:
        print('File Uploaded')

if __name__ == '__main__':
    main()
