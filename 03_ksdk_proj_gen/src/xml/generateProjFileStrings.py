"""
File:  generateXmlString.py
===================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Converts project xml files to strings and saves to .py file**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.5

UML
+++
.. uml:: {{/../../../src/xml/generateXmlString.py

API
+++

"""

import os
import time
import getpass

### Atollic files

fileList = [f for f in os.listdir('./atl') if os.path.isfile(os.path.join('./atl', f))]

print fileList

headerString = "\"\"\"\n"\
"File:  atlFiles.py\n"\
"==================\n"\
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
".. versionadded:: 0.0.6\n"\
"\n"\
"\"\"\"\n\n"

with open('../atlFiles.py', "wb") as f:
    f.write(headerString)
    ## Populate file content strings
    index = 0
    while index < len(fileList):
        t = open('./atl/' + fileList[index], 'rb').read()
        f.write(fileList[index] + ' = \\\n')
        f.write('\"\"\"' + t + '\"\"\"\n\n')
        index += 1
    f.close()

### IAR files

fileList = [f for f in os.listdir('./iar') if os.path.isfile(os.path.join('./iar', f))]

print fileList

headerString = "\"\"\"\n"\
"File:  iarFiles.py\n"\
"==================\n"\
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
".. versionadded:: 0.0.6\n"\
"\n"\
"\"\"\"\n\n"

with open('../iarFiles.py', "wb") as f:
    f.write(headerString)
    ## Populate file content strings
    index = 0
    while index < len(fileList):
        t = open('./iar/' + fileList[index], 'rb').read()
        f.write(fileList[index] + ' = \\\n')
        f.write('\"\"\"' + t + '\"\"\"\n\n')
        index += 1
    f.close()

### KDS files

fileList = [f for f in os.listdir('./kds') if os.path.isfile(os.path.join('./kds', f))]

print fileList

headerString = "\"\"\"\n"\
"File:  kdsFiles.py\n"\
"==================\n"\
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
".. versionadded:: 0.0.6\n"\
"\n"\
"\"\"\"\n\n"

with open('../kdsFiles.py', "wb") as f:
    f.write(headerString)
    ## Populate file content strings
    index = 0
    while index < len(fileList):
        t = open('./kds/' + fileList[index], 'rb').read()
        f.write(fileList[index] + ' = \\\n')
        f.write('\"\"\"' + t + '\"\"\"\n\n')
        index += 1
    f.close()

### MDK files

fileList = [f for f in os.listdir('./mdk') if os.path.isfile(os.path.join('./mdk', f))]

print fileList

headerString = "\"\"\"\n"\
"File:  mdkFiles.py\n"\
"==================\n"\
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
".. versionadded:: 0.0.6\n"\
"\n"\
"\"\"\"\n\n"

with open('../mdkFiles.py', "wb") as f:
    f.write(headerString)
    ## Populate file content strings
    index = 0
    while index < len(fileList):
        t = open('./mdk/' + fileList[index], 'rb').read()
        f.write(fileList[index] + ' = \\\n')
        f.write('\"\"\"' + t + '\"\"\"\n\n')
        index += 1
    f.close()

### GCC files

fileList = [f for f in os.listdir('./armgcc') if os.path.isfile(os.path.join('./armgcc', f))]

print fileList

headerString = "\"\"\"\n"\
"File:  armgccFiles.py\n"\
"==================\n"\
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
".. versionadded:: 0.0.6\n"\
"\n"\
"\"\"\"\n\n"

with open('../armgccFiles.py', "wb") as f:
    f.write(headerString)
    ## Populate file content strings
    index = 0
    while index < len(fileList):
        t = open('./armgcc/' + fileList[index], 'rb').read()
        f.write(fileList[index] + ' = \\\n')
        f.write('\"\"\"' + t + '\"\"\"\n\n')
        index += 1
    f.close()
