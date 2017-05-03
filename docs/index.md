---
layout: default
---

# What is it?

This project is a sample of how to use AWS to a create a workflow that will add parsed email text to Cisco Spark.

# How does it work?

![MLS Workflow](mls-workflow.png)

Using the email alerting features of the Cisco Meraki Dashboard a message is sent into AWS Simple Email Service. This service recieves the email and uploads it to S3. After the upload is complete Lambda is called with the object passed into the function. This is where lambda.py takes over and parses the email. Once parsing is complete the lambda function performs an API call to Spark and posts the message.

# What's next?

As always there is lots left to complete, but if you want something specifically post a bug or send a PR.
