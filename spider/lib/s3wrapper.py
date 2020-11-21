import boto3 


class S3Wrapper(object):

    def __init__(self, access_key, secret_key):
        self.__s3_resource = boto3.resource( 
            's3', 
            aws_access_key_id = access_key, 
            aws_secret_access_key = secret_key, 
        ) 

    def upload(self, bucket_name, local_path, upload_path):
        data = open(local_path, 'rb') 
        self.__s3_resource.Bucket(bucket_name).put_object(Body=data, Key=upload_path) 
        self.__s3_resource.Bucket(bucket_name)
        print("Upload Success")
    
    def download(self, bucket_name, download_prefix, file_name):
        self.__s3_resource.Bucket(bucket_name).download_file(download_prefix, file_name)
        self.__s3_resource.Bucket(bucket_name)
        print("Download Success")

