"""
File:  packPGKSDK.py
====================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Use this script to package the PGKSDK**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 1.0.0

"""

import sys
import os
import shutil
import subprocess
import platform
import zipfile

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from ksdkTools import KsdkTools as kT

VERSION_NUM = '1.0'

osName = platform.system()

if osName == 'Windows':
    specFile = 'build_app_windows.spec'
    buildP = subprocess.Popen(['pyinstaller ', specFile])
    buildP.wait()
    buildF = 'KSDK_Project_Generator.exe'
    srcFile = './dist/' + buildF
    dstDir = './dist/Windows/'
    dstFile = dstDir + buildF
    if not os.path.isdir(dstDir):
        os.makedirs(dstDir)
    shutil.copyfile(srcFile, dstFile)
    iconF = 'kds_icon.ico'
    iconDst = dstDir + iconF
    shutil.copyfile('../src/' + iconF, iconDst)
    pgZip = zipfile.ZipFile('KSDK_Project_Generator_' + VERSION_NUM + '_GA.zip', 'w')
    os.chdir('./dist/')
    for path, dirs, files in os.walk('./Windows/'):
        for f in files:
            fP = os.path.join(path, f)
            pgZip.write(fP)
#    shutil.copyfile('../../../PG_Shared_Build/KSDK_Project_Generator', './Linux/KSDK_Project_Generator')
#    for path, dirs, files in os.walk('./Linux/'):
#        for f in files:
#            fP = os.path.join(path, f)
#            pgZip.write(fP)
#    pgZip.write('LA_OPT_HOST_TOOL.htm')
#    kT.update_file('SW-Content.txt', 'BETA', VERSION_NUM)
    swContentFile = 'SW-Content-Register-KSDK_Project_Generator_' + VERSION_NUM + '.txt'
#    shutil.copyfile('SW-Content.txt', swContentFile)
#    pgZip.write(swContentFile)
    pgZip.close()
    os.chdir('../')

elif osName == 'Linux':
    specFile = 'build_app_linux.spec'
    buildP = subprocess.Popen(['pyinstaller', specFile])
    buildP.wait()
    buildF = 'KSDK_Project_Generator'
    srcFile = './dist/' + buildF
    dstDir = './dist/Linux/'
    dstFile = dstDir + buildF
    if not os.path.isdir(dstDir):
        os.makedirs(dstDir)
    shutil.copyfile(srcFile, dstFile)

elif osName == 'darwin14':
    specFile = 'build_app_mac.spec'
    buildP = subprocess.Popen(['pyinstaller ', specFile])
    buildP.wait()

