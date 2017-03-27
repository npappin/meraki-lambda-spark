import json, boto3, urllib, urllib2

s3 = boto3.client('s3')

def getEmail(event):
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'])
  print "%s,%s" % (bucket, key)
  try:
    response = s3.get_object(Bucket=bucket, Key=key)
    print("CONTENT TYPE: " + response['ContentType'])
    print("Received event: ")
    print(response.viewkeys())
    print "Body:"
    print(response['Body'].read())
    return response['ContentType']
  except Exception as e:
    print(e)
    print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
    raise e

def parseEmail():
  pass
  
def postToSpark():
  url = "https://api.ciscospark.com/v1/messages"
  data = "{\r\n  \"roomId\" : \"Y2lzY29zcGFyazovL3VzL1JPT00vYjM0MzBmYzAtYzI4ZS0xMWU2LTkwZTYtZWJmZjkzMDZkYjdi\",\r\n  \"text\" : \"This is a plain\\ntext message\"\r\n}"
  headers = {
    'authorization': "Bearer OGVjNjg0OGMtNjg1Zi00ZDllLTg1ZjctNmNiZjM1MTAzNjE2MjFjNTA0NDQtNjU4",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "f55b2a37-25cf-daa0-7443-dadd509dabb3"
  }
  req = urllib2.Request(url,data,headers)
  content = urllib2.urlopen(req).read()
  print content
  return 0

def lambda_handler(event, context):
  # TODO implement
  print "Received event: %s" % (json.dumps(event, indent=2))
  emailText = getEmail(event)
  print emailText
  #parsedEmailText = parseEmail(emailText)
  postToSpark()
  #return "fuck"
