import subprocess
import re
import os

outputs = subprocess.check_output("lsusb")


def device_map(lsusboutputs):
    usbinfo_array = lsusboutputs.split('\n')
    device_list = {}
    if not usbinfo_array:
        print("No usb find. Please check the your usb settings!")
        return {}

    for usbinfo in usbinfo_array:
        if not usbinfo.count('root hub'):
            temp = re.match(r'Bus (\d*) Device (\d*): \w* (\w*):(\w*)', usbinfo)

            if temp:
                usb_location = '/dev/bus/usb/' + temp.group(1) + '/' + temp.group(2) + ':/dev/bus/usb/001/001'
                usb_id = temp.group(3) + temp.group(4)
                device_list[usb_id] = usb_location

    return device_list


def docker_clear_all_device_container(device_list):
    for key in device_list:
        container_name = key
        status_code = subprocess.call(["docker", "rm", "-f", container_name])
        if status_code == 0:
            print("rm docker: " + container_name + " successfully")
        else:
            print("rm docker: " + container_name + " failed. Status code: " + str(status_code))
            device_list.pop(key)
    return device_list


def docker_run_parallel_with_binding_device(device_list):
    home_path = os.environ['HOME']
    appium_image_name = "appium/appium-python"

    shutdown_adb = subprocess.check_call(["sudo", "adb", "kill-server"])

    if shutdown_adb:
        print("stop host adb failed. No devices can be accessed by docker. code: " + str(shutdown_adb))
        return {}

    print("stop host adb successfully")

    docker_clear_all_device_container(device_list)

    for key in device_list:
        container_name = key
        device_mapping = device_list[key]
        status_code = subprocess.call(["docker", "run", "-d", "--name", container_name, "-v",
                                       home_path + "/.android:/root/.android", "--device=" + device_mapping,
                                       appium_image_name])
        if status_code == 0:
            print("Start docker: " + container_name + " successfully")
        else:
            print("Start docker: " + container_name + " failed. Status code: " + str(status_code))
            device_list.pop(key)

    return device_list


devices = device_map(outputs)
print(devices)
docker_run_parallel_with_binding_device(devices)
