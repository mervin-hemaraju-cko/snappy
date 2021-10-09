import boto3

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
            raise Exception(f"The instance {self.private_ip} does not have any volumes.")

        # Get the root volume device name
        root_volume_device_name = json["RootDeviceName"]

        # Filter the root volume ID
        root_volume_data = next((filter(lambda t: t["DeviceName"] == root_volume_device_name, json["BlockDeviceMappings"])), None)
        
        if root_volume_data is not None:
            self.root_volume = root_volume_data["Ebs"]["VolumeId"]

        # Get all volume IDs
        self.volumes = [volume["Ebs"]["VolumeId"] for volume in json["BlockDeviceMappings"]]

    def snap_root(self):
        pass

    def snap_all(self):
        pass




        