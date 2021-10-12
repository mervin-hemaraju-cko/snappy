###############################################################
############## All constants values resides here ##############
###############################################################


#################################################
############## TEMPLATES & FILTERS ##############
#################################################
def template_snapshot_output(snapshot_id, for_instance, volume_id):
    return {
        "SnapshotID": snapshot_id,
        "InstanceName": for_instance,
        "VolumeID": volume_id,
    }

def filter_boto3_instance_retrieval(instances):
    return [{
                'Name': 'private-ip-address',
                'Values': instances,
            }]
    
######################################
############## MESSAGES ##############
######################################
MESSAGE_DESCRIPTION_SNAPSHOT = 'Snapshot for {}'


########################################
############## EXCEPTIONS ##############
########################################
EXCEPTION_MESSAGE_VOLUMES_NOT_FOUND = "The instance {} does not have any volumes."
EXCEPTION_MESSAGE_ROOT_VOLUME_NOT_FOUND = "This instance does not have a root volume"
EXCEPTION_MESSAGE_INSTANCES_RETRIEVAL_FAILED = "The following instances could not be retrieved: {}"