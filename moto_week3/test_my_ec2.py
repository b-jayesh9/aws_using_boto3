import sys
import io
import unittest
from moto import mock_ec2
from moto import mock_ec2_deprecated
from my_ec2 import get_client, list_ec2_instances, main
import xmlrunner


class Ec2TestCase(unittest.TestCase):

    @mock_ec2
    @mock_ec2_deprecated
    # used mock ec2 deprecated here coz of deprecation warning while using the ImageID
    def _moto_setup(self):
        """
        Run Instance
        """
        ec2 = get_client()

        reservation = ec2.run_instances(ImageId='something', MinCount=1, MaxCount=1)
        self.instance_id = reservation['Instances'][0]['InstanceId']

    @mock_ec2
    def test_get_client(self):
        """
        check that out get_client function has a valid endpoint
        """
        ec2 = get_client()
        self.assertEqual(ec2._endpoint.host, 'https://ec2.ap-south-1.amazonaws.com')

    @mock_ec2
    def test_list_ec2_instances(self):
        """
        check that our bucket shows as expected
        """
        instances = [e for e in list_ec2_instances()]
        self.assertEqual([], instances)

    @mock_ec2
    def test_main(self):
        """
        verifies the execution of the main function
        """
        # setup ec2 environment
        self._moto_setup()

        # capture stdout for processing
        sys.stdout = my_std_out = io.StringIO()

        # run main function
        main()

        content = my_std_out.getvalue()
        self.assertEqual(self.instance_id, content.strip())


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
