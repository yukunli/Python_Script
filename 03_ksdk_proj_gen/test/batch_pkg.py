"""
File:  batch_pkg.py
=================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Batch script to call all unzipped SDK 2.0 KEx packages**

.. codeauthor:: Bill.Yuan <Bill.Yuan@nxp.com>

.. sectionauthor:: Bill.Yuan <Bill.Yuan@nxp.com>

.. versionadded:: 0.0.1
.. versionadded:: 0.0.2

++++
.. 0.0.1 Support ER test for SDK 2.0 KEx packages
.. 0.0.2 Support RC1 test for SDK 2.0 KEx packages, support 3 folders levels scanning
+++

"""
import os
import sys
import re
import argparse


DEBUG = False

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
UPLOAD_SCRIPTS_PATH = 'D:\\Users\\b46681\\EclipseWorkspace\\UploadPackages\\src'

SDK_package_list = []
SDK_zip_pakcage_list = []
SEARCH_FOLDER_MAX_LEVER = 3


def search_SDK_zip_packages(root_folder, level):
    if level > SEARCH_FOLDER_MAX_LEVER: return
    for item in os.listdir(root_folder):
        ab_path = os.path.join(root_folder, item)
        if os.path.isfile(ab_path):
            if ab_path.endswith('.zip') or ab_path.endswith('.tar.gz'):
                SDK_zip_pakcage_list.append(ab_path)
        elif os.path.isdir(ab_path):
            search_SDK_zip_packages(ab_path, level + 1)


def unzip_SDK_packages(root_folder, force_replace):
    # print how many SDK packages will be unzipped
    print 'The following packages will be unzipped for testing:\n'
    count = 0
    for package_path in SDK_zip_pakcage_list:
        count = count + 1
        print str(count) + ' ' + package_path

    # start unzip
    for package_path in SDK_zip_pakcage_list:
        parent_folder_path = os.path.split(package_path)[0]
        folder_name = os.path.splitext(package_path)[0]

        target_folder = os.path.join(parent_folder_path, folder_name)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        else:
            if not force_replace:
                print 'Skip unzip because it has been unzipped: ' + target_folder
                continue

        print 'unzipping ' + folder_name + ' in path: ' + parent_folder_path
        cmd = ''
        if package_path.endswith('.zip'):
            cmd = 'unzip -o ' + package_path + ' -d ' + target_folder
        elif package_path.endswith('.tar.gz'):
            cmd = 'tar -zxvf ' + package_path + ' -C ' + target_folder

        try:
            if DEBUG: print 'execute the command: ' + cmd
            os.system(cmd)
        except Exception, e:
            print 'Fatal to call os.system() for command: ' + cmd


def search_SDK_packages(root_folder, level):
    if level > SEARCH_FOLDER_MAX_LEVER: return

    for SDK_root in os.listdir(root_folder):
        ab_path = os.path.join(root_folder, SDK_root)
        if os.path.isdir(ab_path):

            is_SDK_package = False
            for SDK_root_file in os.listdir(ab_path):
                if SDK_root_file == 'ksdk_manifest.xml':
                    SDK_package_list.append(ab_path)
                    if DEBUG: print "Found SDK package: " + SDK_root
                    is_SDK_package = True
                    break

            if not is_SDK_package:
                search_SDK_packages(ab_path, level + 1)


def execute_batch_test():
    # print how many SDK packages will be executed
    print 'The following packages will be executed auto test:\n'
    count = 0
    for package_path in SDK_package_list:
        count = count + 1
        print str(count) + ' ' + package_path

    os.chdir(CURRENT_PATH)
    for package_path in SDK_package_list:
        cmd = 'python test_sdk.py ' + package_path
        try:
            if DEBUG: print 'execute the command: ' + cmd
            os.system(cmd)
        except Exception, e:
            print 'Fatal to call os.system() for command: ' + cmd


def execute_projects_uploading(root_folder):
    os.chdir(UPLOAD_SCRIPTS_PATH)

    cmd = 'python auto_push_usr_apps_batch.py ' + root_folder
    try:
        if DEBUG: print 'execute the command: ' + cmd
        os.system(cmd)
    except Exception, e:
        print 'Fatal to call os.system() for command: ' + cmd


if __name__ == '__main__':

    # parser the arguments
    parser = argparse.ArgumentParser(description='Process the command for batch test')
    parser.add_argument('-p', action='store', required=True, dest='parent_path', \
                        help='Specify the parent path of whole KEx packages')
    parser.add_argument('-ng', action='store_true', default=False, dest='not_generate', \
                        help='not re-generate all projects again')
    parser.add_argument('-z', action='store_true', default=False, dest='unzip_packages', \
                        help='Unzip all KEx packages if they have not been unzipped')
    parser.add_argument('-f', action='store_true', default=False, dest='force_replace', \
                        help='Unzip all KEx packages even they have been unzipped')
    parser.add_argument('-u', action='store_true', default=False, dest='upload_test_git', \
                        help='Upload to test git for auto compile test, note that it requires another scripts for uploading')
    arguments = parser.parse_args()


    # check parent folder first
    if os.path.isdir(arguments.parent_path) != True:
        print arguments.parent_path + " is not a directory!"
        exit()

    if os.path.exists(arguments.parent_path) != True:
        print arguments.parent_path + " does not exist!"
        exit()


    # unzip all packages if user requires
    if arguments.unzip_packages:
        search_SDK_zip_packages(arguments.parent_path, 1)
        unzip_SDK_packages(arguments.parent_path, arguments.force_replace)


    # search and get all SDK packages need to be tested
    if not arguments.not_generate:
        search_SDK_packages(arguments.parent_path, 1)
        execute_batch_test()


    # upload all generated projects to auto build system
    # note that, it requires others scripts for uploading
    if arguments.upload_test_git:
        execute_projects_uploading(arguments.parent_path)
