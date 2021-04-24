import ibm_boto3
from ibm_botocore.client import Config, ClientError

def get_buckets(cos):
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        print("------------------------------")
        for bucket in buckets:
            print("Bucket Name: {0}".format(bucket.name))
            try:
                get_bucket_contents(cos, bucket.name)
            except Exception as e:
                print('Get bucket content failed')
                print(Exception, e)
        print("------------------------------")    
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))
        
        
def get_bucket_contents(cos, bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        print("------------------------------")
        for file in files:
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        print("------------------------------")    
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))        


def main(**kwargs):
    """
    The method that is invoked, when run with CLI arguments

    :param kwargs:
    :return: void
    """
    cos = ibm_boto3.resource(service_name='s3',
    ibm_api_key_id='',
    ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
    ibm_service_instance_id='',
    config=Config(signature_version='oauth'), endpoint_url='https://s3.us-south.cloud-object-storage.appdomain.cloud')
    try:
        get_buckets(cos)
    except Exception as e:
        print('List buckets failed')
        print(Exception, e)        
                      

if __name__ == '__main__':
    main()
