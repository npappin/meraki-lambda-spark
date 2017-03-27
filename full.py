#!/usr/bin/python2.7

import argparse, boto3, json

parser = argparse.ArgumentParser()
parser.add_argument('string', type=str)

args = parser.parse_args()

s3 = boto3.client('s3')

def getEmail(objectID):
  print objectID

def lambda_handler(objectID):
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'])
  try:
    response = s3.get_object(Bucket=bucket, Key=key)
    print("CONTENT TYPE: " + response['ContentType'])
    print("Received event: " + json.dumps(response, indent=2))
    return response['ContentType']
  except Exception as e:
    print(e)
    print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
    raise e

def main(objectID):
  print objectID
  lambda_handler(objectID)
  print "stuff"

if __name__ == "__main__":
  print "hello"
  main(args.string)
