import sys
import psutil
import json
import subprocess
import pprint


def get_partitions_info(partition_name):

    if partition_name is None:
        return json.dumps({"error": "Partition not found"}, indent=4)

    disk_partitions = psutil.disk_partitions()

    # Find the specific partition by name
    partition = next((p for p in disk_partitions if p.device == partition_name), None)
    partition_info = {}

    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        partition_info["total_size_bytes"]=partition_usage.total
        partition_info["used_size_bytes"]=partition_usage.used
        partition_info["free_size_bytes"]=partition_usage.free
        partition_info["total_size_gigabytes"]=round(partition_usage.total / (1024 ** 3),2)
        partition_info["used_size_gigabytes"]=round(partition_usage.used / (1024 ** 3),2)
        partition_info["free_size_gigabytes"]=round(partition_usage.free / (1024 ** 3),2)
    except PermissionError:
        print("PermissionError: Access denied")

    if partition:
        partition_info["device"]=partition.device
        partition_info["mountpoint"]=partition.mountpoint
        partition_info["fstype"]=partition.fstype
        partition_info["opts"]=partition.opts
        return json.dumps(partition_info, indent=4)
    else:
        return json.dumps({"error": "Partition not found"}, indent=4)

def get_disk_info_for_path(file_path):
    command = f"df -P {file_path}"
    df_output = subprocess.check_output(command, shell=True).decode("utf-8")
    
    # Split the output into lines and extract the filesystem/disk name
    lines = df_output.split('\n')
    if len(lines) > 1:  # Ensure there's at least one line of output
        # The disk/partition name is in the second column of the first line
        disk_name = lines[1].split()[0]
        return disk_name

    return None  

partition_name = get_disk_info_for_path("/home/joseamair/Desktop/code/projects/disk_test_utility/utils")
print(partition_name)
disk_info = get_partitions_info(partition_name=partition_name)
print(disk_info)