#!/bin/python3

import subprocess

packages_to_skip = [
    'cyclonedds', 'fastcdr', 'fastrtps', 'foonathan_memory_vendor', 
    'google_benchmark_vendor', 'gmock_vendor', 'gtest_vendor', 
    'iceoryx_binding_c', 'iceoryx_hoofs', 'iceoryx_posh', 
    'osrf_testing_tools_cpp', 'urdfdom', 'urdfdom_headers']

installed_pkg_list = open('/opt/ros/humble/installed_packages.list', 'r').read().split('\n')
installed_pkg_list.remove('')

with open('/opt/ros/humble/packages_to_install.rosinstall') as input_file:
    with open('/opt/ros/humble/packages_to_install.filtered.rosinstall', 'w') as output_file:
        while True:
            header = input_file.readline()
            local_name = input_file.readline()
            uri = input_file.readline()
            version = input_file.readline()
            if not header or not local_name or not uri or not version:
                break
            package_name = version.split('/')[2]
            if package_name in installed_pkg_list:
                continue
            if package_name in packages_to_skip:
                continue
            output_file.write(header)
            output_file.write(local_name)
            output_file.write(uri)
            output_file.write(version)
        output_file.write('\n')
