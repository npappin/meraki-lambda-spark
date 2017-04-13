import os, json, boto3, urllib, urllib2
import email

s3 = boto3.client('s3')

def getEmail(event):
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'])
  #print "%s,%s" % (bucket, key)
  try:
    response = s3.get_object(Bucket=bucket, Key=key)
    #print("CONTENT TYPE: " + response['ContentType'])
    #print("Received event: ")
    #print(response.viewkeys())
    #print "Body:"
    emailText = response['Body'].read()
    #print emailText
    return emailText
  except Exception as e:
    print(e)
    print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
    raise e

def parseEmail(rawEmail):
  parsingEmail = email.message_from_string(rawEmail)
  parsedEmail = {}
  parsedEmail['Subject'] = parsingEmail['Subject']
  walkedEmail = parsingEmail.walk()
  for part in walkedEmail:
    if part.get_content_type() == 'text/plain':
      parsedEmail['Text'] = part.get_payload()
  needToLoop = True
#  while needToLoop == True:
#    print "run once"
#    needToLoop = False
  plainText = parsedEmail['Text']
  plainText = plainText.splitlines()
  plainText = plainText[2:]
  plainText = plainText[:-6]
  plainText.insert(0,parsedEmail['Subject'])
  plainText = '/n'.join(map(str,plainText))
  parsedEmail['Parsed'] = plainText
#  for line in plainText:
#    print(line)
  return parsedEmail
  
def postToSpark(dictToPost):
  apiKey = os.environ.get('SparkApiKey')
  url = "https://api.ciscospark.com/v1/messages"
  data = '''{
    "roomId" : "Y2lzY29zcGFyazovL3VzL1JPT00vNGVlMDYxYzAtMTMwZC0xMWU3LTk3NzYtODkyNDJkMDcxNjcx",
    "text" : "%s"
    }''' % dictToPost['Parsed']
  headers = {
    'authorization': "Bearer %s" % apiKey,
    'content-type': "application/json",
    'cache-control': "no-cache",
  }
  #print headers
  req = urllib2.Request(url,data,headers)
  content = urllib2.urlopen(req).read()
  #print content
  return 0

def lambda_handler(event, context):
  # TODO implement
  #print "Received event: %s" % (json.dumps(event, indent=2))
  #print os.environ.get('SparkApiKey')
  emailText = getEmail(event)
  #print emailText
  parsedEmail = parseEmail(emailText)
  print(parsedEmail)
  
  postToSpark(parsedEmail)
  #return "fuck"
  return 0
