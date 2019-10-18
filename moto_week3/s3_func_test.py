import boto3
import io
import sys
import unittest
from moto import mock_s3
from s3_functions import main, get_client, list_s3_buckets, list_s3_objects, read_s3_object


class S3Tests(unittest.TestCase):
    def setUp(self):
        #sets up the local moto s3 service for mocking.
        self.bucket = 'buck02jay'
        self.key = 'upload.txt'
        self.value = 'RA1511001010001'

    @mock_s3
    def _moto_setup(self):
        
        """
        simulation of s3 file upload
        """
        s3_client = get_client()
        s3.create_bucket(Bucket=self.bucket)
        s3.put_object(Bucket=self.bucket, Key=self.key, Body = self.value)
        pass

    @mock_s3
    def test_get_client(self):
        s3 = get_client()
        #success
        self.assertEqual(s3._endpoint.host, "https://s3.ap-south-1.amazonaws.com")


    @mock_s3
    def test_list_s3_buckets(self):
        self.__moto_setup()
        buckets = [b for b in list_s3_buckets()]
        print(buckets)
        #success
        self.assertTrue(self.bucket in buckets)


    @mock_s3
    def test_list_s3_objects(self):
        self.__moto_setup()
        keys = [b for b in list_s3_objects(self.bucket)]
        # success
        self.assertIn(self.key, keys)


    @mock_s3
    def test_read_s3_object(self):
        self.__moto_setup()
        data = [str(d, encoding = "utf-8") for d in read_s3_object(self.bucket,self.key)]
        #doesn't read data as specified due to bytes like object.
        self.assertTrue(self.value == data)


    @mock_s3
    def test_main(self):
        self.__moto_setup()
        sys.stdout = my_std_out = io.StringIO()
        main()
        content = my_std_out.getvalue()
        #error above, couldn't fix.
        self.assertTrue('[{}]'.format(self.bucket)in content)
        self.assertTrue(r'[{}]'.format(self.key) in content)
        self.assertTrue(r'{}'.format(self.value) in content)




