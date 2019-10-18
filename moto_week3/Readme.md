Aim of this project is to create tests for mocking AWS Services.

I have tried to mock EC2, S3 and working on mocking DynamoDB functions via Moto.
I have currently used the decorator form, and I'm trying to use the context manager form while mocking my DynamoDB functions.

Prerequisites: Moto, Boto3 and Python

Steps to Execute:

1. Go to the setup file and update endpoints of the services (currently not live yet, since DynamoDB test isn't configured)
2. Run the setup file and all the test will run one after the other.

Workaround:
Run the test file for particular service till the tests pass/fail for that particular service.

