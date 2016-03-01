"""
File:  imageMaker.py
====================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Use this script to generate image dictionary for KSDK Project Generator tool**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.5

"""

import base64
import os
import time
import getpass

boardImageList = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]

#print boardImageList
#TODO: Outside of this file, in this directory add 1.3.0 .gif images for 1.3.0 boards

headerString = "\"\"\"\n"\
"File:  ksdkImg.py\n"\
"=================\n"\
"Copyright (c) " + time.strftime("%Y") + " Freescale Semiconductor\n"\
"\n"\
"Brief\n"\
"+++++\n"\
"**Dictionary of image files**\n"\
"\n"\
".. codeauthor:: " + getpass.getuser() + "<getpass.getuser()@freescale.com>\n"\
"\n"\
".. sectionauthor:: " + getpass.getuser() + "<getpass.getuser()@freescale.com>\n"\
"\n"\
".. versionadded:: 0.0.5\n"\
"\n"\
"\"\"\"\n\n"

with open('../ksdkImg.py', "wb") as f:
    f.write(headerString)
    f.write('boardImages = { \\\n')
    ## Populate the image dictionary with the images
    index = 0
    while index < len(boardImageList):
        testImage = base64.encodestring(open('./' + boardImageList[index], 'rb').read())
        f.write('\'' + boardImageList[index] + '\': \"\"\"\n')
        f.write(testImage)
        if index == (len(boardImageList) - 1):
            f.write('\"\"\"}')
        else:
            f.write('\"\"\", \\\n')
        index += 1
    f.close()
