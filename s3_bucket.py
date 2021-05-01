import boto3

#파일 업로드 

# 업로드할 파일 이름
filename = "test.jpg"

# 업로드할 버킷
#bucketname = ""

def upload_file(filename):
    s3 = boto3.client('s3')
    s3.upload_file(filename, 'browser-test-bucket', filename) # 업로드할 파일, 버킷이름, 버킷에 저장될 장소와 이름



