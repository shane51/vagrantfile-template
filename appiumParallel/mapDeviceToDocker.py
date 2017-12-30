import subprocess
import re
import os
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

appium_image_name = "appium/appium-python"

test_code_repo_name = "LucaTester"
host_home_path = os.environ['HOME']
host_adb_key_path = "" + host_home_path + "/.android"
test_code_src_path = "" + host_home_path + "/" + test_code_repo_name + "/"
test_code_dest_path = "/opt/"
cmd_to_run = ["python", test_code_dest_path + test_code_repo_name + "/" + "main.py"]

outputs = subprocess.check_output("lsusb")


def device_map(lsusboutputs):
    usbinfo_array = lsusboutputs.split('\n')
    device_list = {}
    if not usbinfo_array:
        print("No usb find. Please check your usb settings!")
        return {}

    for usbinfo in usbinfo_array:
        if not usbinfo.count('root hub') + usbinfo.count('VMware'):
            temp = re.match(r'Bus (\d*) Device (\d*): \w* (\w*):(\w*)', usbinfo)

            if temp:
                usb_location = '/dev/bus/usb/' + temp.group(1) + '/' + temp.group(2) + ':/dev/bus/usb/001/001'
                usb_id = temp.group(3) + temp.group(4) + temp.group(1) + temp.group(2)
                device_list[usb_id] = usb_location

    return device_list


def docker_clear_all_device_container(device_list):
    for key in device_list:
        container_name = key
        cmd = ["docker", "rm", "-f", container_name]
        status_code = subprocess.call(cmd)
        if status_code == 0:
            print("rm docker: " + container_name + " successfully")
        else:
            print("rm docker: " + container_name + " failed. Status code: " + str(status_code))
            device_list.pop(key)
    return device_list


def docker_run_parallel_with_binding_device(device_list, adb_key_path):
    if not device_list:
        print("docker run error! No devices find. Please check your device is connected!")
        return {}
    cmd = ["sudo", "adb", "kill-server"]
    shutdown_adb = subprocess.check_call(cmd)

    if shutdown_adb:
        print("stop host adb failed. No devices can be accessed by docker. code: " + str(shutdown_adb))
        return {}

    print("stop host adb successfully")

    docker_clear_all_device_container(device_list)

    for key in device_list:
        container_name = key
        device_mapping = device_list[key]
        cmd = ["docker", "run", "-d", "--name", container_name, "-v",
               adb_key_path + ":/root/.android", "--device=" + device_mapping,
               appium_image_name]
        status_code = subprocess.call(cmd)
        if status_code == 0:
            print("Start docker: " + container_name + " successfully")
        else:
            print("Start docker: " + container_name + " failed. Status code: " + str(status_code))
            device_list.pop(key)

    return device_list


def docker_cp_test_code_into_container_parallel(device_list, src_path, dest_path):
    if not device_list:
        print("docker cp error! No devices find. Please check your device is connected!")
        return {}

    for key in device_list:
        container_name = key
        cmd = ["docker", "cp", src_path, container_name + ":" + dest_path]
        status_code = subprocess.call(cmd)
        if status_code == 0:
            print(" Copy test code into " + container_name + " successfully")
        else:
            print(" Copy test code into " + container_name + " failed. Status code: " + str(status_code))
            device_list.pop(key)

    return device_list


def docker_run_test_in_container_foreground(device, script):
    if not device:
        print("docker exec error! No devices find. Please check your device is connected!")
        return {}

    container_name = device[0]

    cmd = ["docker", "exec", container_name] + script

    status_code = subprocess.call(cmd)
    if status_code == 0:
        print(" run test in " + container_name + " successfully")
        return 0
    else:
        print(" run test in " + container_name + " failed. Status code: " + str(status_code))
        return 1


devices = device_map(outputs)
print("Find devices: " + str(devices))
devices = docker_run_parallel_with_binding_device(devices, host_adb_key_path)
devices = docker_cp_test_code_into_container_parallel(devices, test_code_src_path, test_code_dest_path)
print("Devices to run" + str(devices.keys()))

if devices:
    pool = ThreadPool(len(devices))

    results = pool.map(partial(docker_run_test_in_container_foreground, script=cmd_to_run), devices.items())

    pool.close()
    pool.join()

    print(results)
