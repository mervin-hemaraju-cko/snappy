import boto3
from snappy.instance import Instance

class Snappy():

    def __init__(self, instances):

        # Create an empty list of instances
        self.instances = []

        # Create the boto3 EC2 client
        client = boto3.client('ec2')

        # Describe all instances
        response = client.describe_instances(
            Filters=[{
                'Name': 'private-ip-address',
                'Values': instances,
            }]
        )

        # Filter and append Instances
        for r in response['Reservations']:

            for i in r['Instances']:

                self.instances.append(Instance(i))