For SDK KEx packages test steps:

1. Download all KEx SDK 2.0 packages to a parent folder.
2. Open the command window, execute command: python batch_pkg.py -p [All_KEx_packages_parent_path] -z > key.log 2>&1
3. Double check the XXXX_failure.log and key.log, and all projects that the tool supported will be generated in KEx packages.


usage: batch_pkg.py [-h] -p PARENT_PATH [-ng] [-z] [-f] [-u]

Process the command for batch test

optional arguments:
  -h, --help      show this help message and exit
  -p PARENT_PATH  Specify the parent path of whole KEx packages
  -ng             not re-generate all projects again
  -z              Unzip all KEx packages if they have not been unzipped
  -f              Unzip all KEx packages even they have been unzipped
  -u              Upload to test git for auto compile test, note that it
                  requires another scripts for uploading