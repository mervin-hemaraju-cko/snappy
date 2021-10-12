import boto3
import snappy.utils.constants as Consts

class Instance:

    def __init__(self, json) -> None:

        # Declare empty values 
        self.name = None
        self.private_ip = None
        self.root_volume = None
        self.volumes = None

        # Retrieve instance name
        if "Tags" in json:

            for tag in json["Tags"]:

                if(tag["Key"].lower() == "name"):

                    self.name = tag["Value"]
        
        # Retrieve IP Address
        if "PrivateIpAddress" in json:

            self.private_ip = json["PrivateIpAddress"]


        # Retrieve volume IDs

        # Check if volumes exists before continuing
        if "BlockDeviceMappings" not in json:
            raise Exception(Consts.EXCEPTION_MESSAGE_VOLUMES_NOT_FOUND.format(self.private_ip))

        # Get the root volume device name
        if "RootDeviceName" in json:
            root_volume_device_name = json["RootDeviceName"]

            # Filter the root volume ID
            root_volume_data = next((filter(lambda t: t["DeviceName"] == root_volume_device_name, json["BlockDeviceMappings"])), None)
        
            if root_volume_data is not None:
                self.root_volume = root_volume_data["Ebs"]["VolumeId"]

        # Get all volume IDs
        self.volumes = [volume["Ebs"]["VolumeId"] for volume in json["BlockDeviceMappings"]]

    def snap_root(self, tags_specifications=None) -> str:
        
        # Check if root volume is present
        if self.root_volume is None:
            raise Exception(Consts.EXCEPTION_MESSAGE_ROOT_VOLUME_NOT_FOUND)

        # Create EC2 client 
        client = boto3.client('ec2')

        # Reformat tags scpefications
        if tags_specifications != None and tags_specifications != []:
            formated_tags_specs = [
                {
                    'ResourceType': 'snapshot',
                    'Tags': tags_specifications
                },
            ]
        else:
            formated_tags_specs = []

        # Create snapshot
        response = client.create_snapshot(
            Description=f'Snapshot for {self.private_ip}',
            VolumeId=self.root_volume,
            TagSpecifications=formated_tags_specs
        )
        
        # Return the snapshot ID
        return response["SnapshotId"]

    def snap_all(self, tags_specifications=None):

        # Create EC2 client 
        client = boto3.client('ec2')

        # Reformat tags scpefications
        if tags_specifications != None and tags_specifications != []:
            formated_tags_specs = [
                {
                    'ResourceType': 'snapshot',
                    'Tags': tags_specifications
                },
            ]
        else:
            formated_tags_specs = []

        # Create empty list of snapshot IDs
        snapshot_ids = []

        # Create snapshots
        for id in self.volumes:
            # Create snapshot
            response = client.create_snapshot(
                Description=f'Snapshot for {self.private_ip}',
                VolumeId=id,
                TagSpecifications=formated_tags_specs
            )

            # Append ID to list
            snapshot_ids.append(response["SnapshotId"])
        
        # Return the snapshot ID list
        return snapshot_ids


            




        