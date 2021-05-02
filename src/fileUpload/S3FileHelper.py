import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

class S3FileHelper():
    def __init__(self):
        load_dotenv()
        self.accessKey = os.getenv("AWS_S3_ACCRESS_KEY")
        self.secretKey = os.getenv("AWS_S3_SECRET_KEY")
        self.bucketName = os.getenv("AWS_S3_KAKAO_WORK_BUCKET_NAME")
    
    def uploadFile(self, localFilePath, s3Key):
        key = 'kakaowork/{}'.format(s3Key)
        s3Client = boto3.client(
            's3',
            region_name='ap-northeast-2',
            aws_access_key_id=self.accessKey,
            aws_secret_access_key=self.secretKey
            )
        
        try:
            with open(localFilePath, 'rb') as data:
                s3Client.upload_file(data.name, self.bucketName, key)
        except ClientError as e:
            return False
        finally:
            self.__closeClientConnection(s3Client)  
        return True

    def getSignedUrl(self, s3Key):
        key = 'kakaowork/{}'.format(s3Key)
        s3Client = boto3.client(
            's3',
            region_name='ap-northeast-2',
            aws_access_key_id=self.accessKey,
            aws_secret_access_key=self.secretKey
            )

        response = None
        try:
            # expire 3600 sec
            response = s3Client.generate_presigned_url(
                'get_object',
                Params ={
                    'Bucket': self.bucketName,
                    'Key': key
                })
        except ClientError as e:
            return response
        finally:
            self.__closeClientConnection(s3Client)      
        return response

    def __closeClientConnection(self, client):
        session = client._endpoint.http_session
        managers = [session._manager, *session._proxy_managers.values()]
        for manager in managers:
            manager.clear()


            