from lambdacloud import create_instance as create_ins
from lambdacloud import list_ssh_keys
from lambdacloud import list_instance_types
from lambdacloud import delete_instance as delete_ins
import time
import fire


def create_instance(instance_type=None, ssh_key_name=None, poll_time=20):
    # login(token=os.getenv('LAMBDA_CLOUD_TOKEN'))

    if ssh_key_name is None:
        ssh_keys = list_ssh_keys()
        print('Available ssh keys:')
        for idx, ssh_key in enumerate(ssh_keys, 1):
            print(idx, ssh_key)
        
        ssh_key_name = input(f'Select ssh key [1-{len(ssh_keys)}]: ')
        try:
            ssh_key_name = int(ssh_key_name)
        except:
            raise ValueError(f'Invalid ssh key selection: {ssh_key_name}')
        assert 1 <= ssh_key_name <= len(ssh_keys), f'Invalid ssh key selection, must be between 1 and {len(ssh_keys)}'
        ssh_key_name = ssh_keys[int(ssh_key_name)-1].name

    if instance_type is None:
        instance_types = list_instance_types()
        for idx, instance_type in enumerate(instance_types, 1):
            print(idx, instance_type)

        instance_type = input(f'Select instance type [1-{len(instance_types)}]: ')
        try:
            instance_type = int(instance_type)
        except:
            raise ValueError(f'Invalid instance type selection: {instance_type}')
        assert 1 <= instance_type <= len(instance_types), f'Invalid instance type selection, must be between 1 and {len(instance_types)}'
        instance_type = instance_types[int(instance_type)-1].name

    print(f'Creating instance of type {instance_type} with ssh key {ssh_key_name}')
    while True:
        try:
            instance_id = create_ins(instance_type, ssh_key_names=ssh_key_name)
            print(f'Instance created with id: {instance_id}')
            break
        except:
            print(f'No {instance_type} found...sleeping for {poll_time} seconds')
            time.sleep(poll_time)

delete_instance = delete_ins

if __name__ == "__main__":
    fire.Fire()
