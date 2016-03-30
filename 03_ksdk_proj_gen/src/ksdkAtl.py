"""
File:  ksdkAtl.py
===================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Methods for ATL project creation for KSDK**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.6

UML
+++
.. uml:: {{/../../../src/ksdkAtl.py

API
+++

"""


## USER MODULES
from ksdkTools import KsdkTools as kT
from ksdkProj import ksdkProjClass
import atlFiles as aF

## PYTHON MODULES
import copy
import os
import xml.etree.ElementTree as ET


## Important ewp tags
CDEFINES = {'valueType': 'definedSymbols', 'listOptionValue': []}
CDEFINES_USB = {'valueType': 'definedSymbols', 'listOptionValue': ['_DEBUG=1']}
CINCLUDES = {'valueType': 'includePath', 'listOptionValue': []}

ASMDEFINES = {'valueType': 'definedSymbols', 'listOptionValue': ['DEBUG']}
ASMINCLUDES = {'valueType': 'includePath', 'listOptionValue': []}

LINKOUT = {'name': 'IlinkOutputFile', 'state': '.out'}
LINKDEFINES = {'name': 'IlinkConfigDefines', 'state': ['__stack_size__=', '__heap_size__=']}
LINKDEFINES_USB = {'name': 'IlinkConfigDefines', \
                  'state': ['__ram_vector_table__=1', '__stack_size__=', '__heap_size__=']}


LINKLD = {'valueType': 'stringList', 'listOptionValue': []}
LINKLIBS = {'valueType': 'userObjs', \
           'libName': ['ksdk_xxx'], \
           'libPath': ['lib/ksdk_xxx_lib/atl/ddd/debug']}
LINKLIBS_USB = {'valueType': 'userObjs', \
               'listOptionValue': ['lib/ksdk_xxx_lib/atl/ddd/debug/libksdk_xxx.a', \
                         'usb/usb_core/device/build/atl/usbd_sdk_yyy_zzz/debug/libusbd_zzz.a', \
                         'usb/usb_core/device/build/atl/usbh_sdk_yyy_zzz/debug/libusbh_zzz.a']}

WS_PROJECTS = {'name': '', \
               'path': '', \
               'open': 'true', \
       'activeconfig': ['debug', 'release'], \
    'buildreferences': [{'config': 'debug', 'text': 'false'}, {'config': 'release', 'text': 'false'}]}

PROJ_STARTUP =\
[\
 {'name': 'startup', 'type': '2', 'locationURI': 'virtual:/virtual'},\
 {'name': 'startup/startup_xxx.s', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/devices/xxx/startup/gcc/startup_xxx.S'}, \
 {'name': 'startup/system_xxx.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/devices/xxx/startup/system_xxx.c'}, \
 {'name': 'startup/system_xxx.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/devices/xxx/startup/system_xxx.h'}, \
 {'name': 'startup/startup.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/devices/startup.c'}, \
 {'name': 'startup/startup.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/devices/startup.h'}, \
]

PROJ_UTILITIES =\
[\
 {'name': 'utilities', 'type': '2', 'locationURI': 'virtual:/virtual'},\
 {'name': 'utilities/fsl_debug_console.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/utilities/src/fsl_debug_console.c'}, \
 {'name': 'utilities/fsl_debug_console.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/utilities/inc/fsl_debug_console.h'}, \
 {'name': 'utilities/print_scan.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/utilities/src/print_scan.c'}, \
 {'name': 'utilities/print_scan.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/platform/utilities/src/print_scan.h'}, \
]

PROJ_BOARD =\
[\
 {'name': 'board', 'type': '2', 'locationURI': 'virtual:/virtual'},\
 {'name': 'board/gpio_pins.c', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/board/gpio_pins.c'}, \
 {'name': 'board/gpio_pins.h', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/board/gpio_pins.h'}, \
 {'name': 'board/pin_mux.c', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/board/pin_mux.c'}, \
 {'name': 'board/pin_mux.h', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/board/pin_mux.h'}, \
 {'name': 'board/board.c', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/board/board.c'}, \
 {'name': 'board/board.h', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/board/board.h'}, \
 {'name': 'board/hardware_init.c', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/hardware_init.c'}, \
]

PROJ_SOURCES =\
[\
 {'name': 'sources', 'type': '2', 'locationURI': 'virtual:/virtual'},\
 {'name': 'sources/main.c', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/main.c'}, \
 {'name': 'sources/main.h', 'type': '1', 'locationURI': 'PARENT-1-PROJECT_LOC/main.h'}, \
]

PROJ_FREERTOS =\
[\
    {'name': 'free-rtos', 'type': '2', 'locationURI': 'virtual:/virtual'},\
    {'name': 'free-rtos/FreeRTOSConfig.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/config/xxx/gcc/FreeRTOSConfig.h'},\
    {'name': 'free-rtos/croutine.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/croutine.h'},\
    {'name': 'free-rtos/event_groups.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/event_groups.h'},\
    {'name': 'free-rtos/FreeRTOS.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/FreeRTOS.h'},\
    {'name': 'free-rtos/list.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/list.h'},\
    {'name': 'free-rtos/mpu_wrappers.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/mpu_wrappers.h'},\
    {'name': 'free-rtos/portable.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/portable.h'},\
    {'name': 'free-rtos/projdefs.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/projdefs.h'},\
    {'name': 'free-rtos/queue.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/queue.h'},\
    {'name': 'free-rtos/semphr.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/semphr.h'},\
    {'name': 'free-rtos/StackMacros.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/StackMacros.h'},\
    {'name': 'free-rtos/task.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/task.h'},\
    {'name': 'free-rtos/timers.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/include/timers.h'},\
    {'name': 'free-rtos/port.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/port/gcc/port.c'},\
    {'name': 'free-rtos/portasm.s', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/port/gcc/portasm.s'},\
    {'name': 'free-rtos/portmacro.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/port/gcc/portmacro.h'},\
    {'name': 'free-rtos/portTicks.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/port/gcc/portTicks.h'},\
    {'name': 'free-rtos/croutine.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/croutine.c'},\
    {'name': 'free-rtos/event_groups.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/event_groups.c'},\
    {'name': 'free-rtos/heap_1.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/heap_1.c'},\
    {'name': 'free-rtos/heap_2.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/heap_2.c'},\
    {'name': 'free-rtos/heap_3.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/heap_3.c'},\
    {'name': 'free-rtos/heap_4.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/heap_4.c'},\
    {'name': 'free-rtos/list.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/list.c'},\
    {'name': 'free-rtos/queue.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/queue.c'},\
    {'name': 'free-rtos/tasks.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/tasks.c'},\
    {'name': 'free-rtos/timers.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/FreeRTOS/src/timers.c'}\
]


PROJ_MQX =\
[\
    {'name': 'mqx', 'type': '2', 'locationURI': 'virtual:/virtual'},\
    {'name': 'mqx/bsp.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/mqx/source/bsp/bsp.h'},\
    {'name': 'mqx/bsp_config.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/mqx/source/bsp/bsp_config.h'},\
    {'name': 'mqx/init_bsp.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/mqx/source/bsp/init_bsp.c'},\
    {'name': 'mqx/mqx_main.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/mqx/source/bsp/mqx_main.c'},\
    {'name': 'mqx/mqx.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/mqx/source/include/mqx.h'},\
    {'name': 'mqx/lite_config.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/config/common/lite_config.h'},\
    {'name': 'mqx/mqx_cnfg.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/config/common/mqx_cnfg.h'},\
    {'name': 'mqx/small_ram_config.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/config/common/small_ram_config.h'},\
    {'name': 'mqx/verif_enabled_config.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/config/common/verif_enabled_config.h'},\
    {'name': 'mqx/mqx_sdk_config.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/config/mcu/xxx/mqx_sdk_config.h'},\
    {'name': 'mqx/user_config.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/mqx/config/board/bbb/user_config.h'}\
]

PROJ_UCOSII =\
[\
    {'name': 'ucosii', 'type': '2', 'locationURI': 'virtual:/virtual'},\
    {'name': 'ucosii/app_hooks.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/config/app_hooks.c'},\
    {'name': 'ucosii/os_core.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_core.c'},\
    {'name': 'ucosii/os_cpu.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/GNU/os_cpu.h'},\
    {'name': 'ucosii/os_cpu_a.S', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/GNU/os_cpu_a.S'}, \
    {'name': 'ucosii/os_cpu_c.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/GNU/os_cpu_c.c'}, \
    {'name': 'ucosii/os_dbg.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/GNU/os_dbg.c'}, \
    {'name': 'ucosii/os_flag.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_flag.c'},\
    {'name': 'ucosii/os_mbox.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_mbox.c'}, \
    {'name': 'ucosii/os_mem.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_mem.c'}, \
    {'name': 'ucosii/os_mutex.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_mutex.c'}, \
    {'name': 'ucosii/os_q.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_q.c'}, \
    {'name': 'ucosii/os_sem.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_sem.c'}, \
    {'name': 'ucosii/os_task.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_task.c'}, \
    {'name': 'ucosii/os_time.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_time.c'}, \
    {'name': 'ucosii/os_tmr.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSII/src/uCOS-II/Source/os_tmr.c'}\
]

PROJ_UCOSIII =\
[\
    {'name': 'ucosiii', 'type': '2', 'locationURI': 'virtual:/virtual'},\
    {'name': 'ucosiii/cpu_core.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uC-CPU/cpu_core.c'},\
    {'name': 'ucosiii/cpu_a.S', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uC-CPU/ccc/GNU/cpu_a.S'},\
    {'name': 'ucosiii/cpu_c.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uC-CPU/ccc/GNU/cpu_c.c'},\
    {'name': 'ucosiii/os.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os.h'},\
    {'name': 'ucosiii/os_app_hooks.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/config/os_app_hooks.c'},\
    {'name': 'ucosiii/os_cfg_app.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_cfg_app.c'},\
    {'name': 'ucosiii/os_core.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_core.c'},\
    {'name': 'ucosiii/os_cpu.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/GNU/os_cpu.h'},\
    {'name': 'ucosiii/os_cpu_a.S', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/GNU/os_cpu_a.S'},\
    {'name': 'ucosiii/os_cpu_c.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/GNU/os_cpu_c.c'},\
    {'name': 'ucosiii/os_dbg.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_dbg.c'},\
    {'name': 'ucosiii/os_flag.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_flag.c'},\
    {'name': 'ucosiii/os_int.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_int.c'},\
    {'name': 'ucosiii/os_mem.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_mem.c'},\
    {'name': 'ucosiii/os_msg.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_msg.c'},\
    {'name': 'ucosiii/os_mutex.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_mutex.c'},\
    {'name': 'ucosiii/os_pend_multi.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_pend_multi.c'},\
    {'name': 'ucosiii/os_prio.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_prio.c'},\
    {'name': 'ucosiii/os_q.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_q.c'},
    {'name': 'ucosiii/os_sem.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_sem.c'},\
    {'name': 'ucosiii/os_stat.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_stat.c'},\
    {'name': 'ucosiii/os_task.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_task.c'},\
    {'name': 'ucosiii/os_tick.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_tick.c'},\
    {'name': 'ucosiii/os_time.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_time.c'},\
    {'name': 'ucosiii/os_tmr.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_tmr.c'},\
    {'name': 'ucosiii/os_type.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_type.h'},\
    {'name': 'ucosiii/os_var.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/rtos/uCOSIII/src/uCOS-III/Source/os_var.c'}\
]

class KsdkAtl(object):
    """ Class for generating ATL projects

        .. todo:: Edit class to make it a child of ksdkProjClass
    """
    def __init__(self, ksdkProj):
        """ Init class

        :param ksdkProj: Instance of a KSDK project
        """

        self.parent = ksdkProj.workSpace
        self.userName = ksdkProj.userName
        self.date = ksdkProj.date
        self.name = ksdkProj.name
        self.isLinked = ksdkProj.isLinked
        self.device = ksdkProj.device

        self.projRelPath = ''
        self.wsRelPath = ''

        ## Determine if this is a USB or standard project
        self.projType = 'usb' if ksdkProj.useUSB else 'std'

        # Create local copies of the tag dictionaries
        if self.projType == 'std':
            self.cDefines = copy.deepcopy(CDEFINES)
            self.linkDefines = copy.deepcopy(LINKDEFINES)
            self.linkLibs = copy.deepcopy(LINKLIBS)
        else:
            self.cDefines = copy.deepcopy(CDEFINES_USB)
            self.linkDefines = copy.deepcopy(LINKDEFINES_USB)
            self.linkLibs = copy.deepcopy(LINKLIBS_USB)

        self.cIncludes = copy.deepcopy(CINCLUDES)
        self.linkOut = copy.deepcopy(LINKOUT)
        self.linkLd = copy.deepcopy(LINKLD)

        self.asmDefines = copy.deepcopy(ASMDEFINES)
        self.asmIncludes = copy.deepcopy(ASMINCLUDES)

        self.projStartup = copy.deepcopy(PROJ_STARTUP)
        self.projSources = copy.deepcopy(PROJ_SOURCES)
        self.projUtilities = copy.deepcopy(PROJ_UTILITIES)
        self.projBoard = copy.deepcopy(PROJ_BOARD)

        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.projRtos = copy.deepcopy(PROJ_FREERTOS)
            elif ksdkProj.rtos == 'mqx':
                self.projRtos = copy.deepcopy(PROJ_MQX)
            elif ksdkProj.rtos == 'ucosii':
                self.projRtos = copy.deepcopy(PROJ_UCOSII)
            elif ksdkProj.rtos == 'ucosiii':
                self.projRtos = copy.deepcopy(PROJ_UCOSIII)

        #self.parent = "C:\\Users\\b45635\\PGKSDK\\IAR"
        #self.name = 'Test'
        return

    def gen_cproject(self, ksdkProj):
        """ Generate the cproject file for KDS project

        :param ksdkProj: Instance of a KSDK project
        """

        kdsPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl'
        relPath = ''
        if self.isLinked:
            tempStr = kT.get_rel_path(kdsPath, ksdkProj.sdkPath) + '/../'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../../'
        
        self.projRelPath = relPath


        # Populate ksdkProj specifics to dictionaries

        ## Configure linker option
        self.linkLd['listOptionValue'].append(self.projRelPath + 'platform/devices/' +\
                                              ksdkProj.device[1] + '/linker/gcc/' +\
                                              ksdkProj.device[0] + '_flash.ld')


        ## Set a define for the device
        self.cDefines['listOptionValue'].append('CPU_' + ksdkProj.device[2])
        ##                Added to fix K80 application build issues                   ##
        #if (ksdkProj.device[1] == 'MK80F25615') or (ksdkProj.device[1] == 'MK82F25615'):
        #    self.cDefines['listOptionValue'].append('USING_DIRECT_INTERFACE=1')
        ##                Added to fix UART smartcard application build issues        ##
        if ksdkProj.libList[0] != 'hal':
            for d in ksdkProj.drvList:
                if d[0] == 'smartcard':
                    if kT.get_smartcard_type(ksdkProj.sdkPath, ksdkProj.device[1]) == (1 << 8):
                        self.cDefines['listOptionValue'].append('USING_DIRECT_INTERFACE=1')
                    elif kT.get_smartcard_type(ksdkProj.sdkPath, ksdkProj.device[1]) == 1:
                        self.cDefines['listOptionValue'].append('USING_NCN8025_INTERFACE=1')
        ################################################################################
        if ksdkProj.useBSP:
            boardType = ksdkProj.board[0][:ksdkProj.board[0].find('_')]
            self.cDefines['listOptionValue'].append(ksdkProj.board[0])
            if boardType == 'FRDM':
                self.cDefines['listOptionValue'].append('FREEDOM')
            elif boardType == 'TWR':
                self.cDefines['listOptionValue'].append('TOWER')
            elif boardType == 'USB':
                self.cDefines['listOptionValue'].append('BOARD_USE_VIRTUALCOM')
                self.cDefines['listOptionValue'].append('DONGLE')
            elif boardType == 'MRB':
                self.cDefines['listOptionValue'].append('MRB_KW01')
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.cDefines['listOptionValue'].append('FSL_RTOS_FREE_RTOS')
            elif ksdkProj.rtos == 'mqx':
                self.cDefines['listOptionValue'].append('FSL_RTOS_MQX')
            elif ksdkProj.rtos == 'ucosii':
                self.cDefines['listOptionValue'].append('FSL_RTOS_UCOSII')
            elif ksdkProj.rtos == 'ucosiii':
                self.cDefines['listOptionValue'].append('FSL_RTOS_UCOSIII')

        ## Add C include paths necessary for project
        if ksdkProj.libList[0] != 'hal':
            self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/osa/inc')
            self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/utilities/inc')

        self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/CMSIS/Include')
        self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/devices')
        self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/devices/' +\
                                                          ksdkProj.device[1] + '/include')
        self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/devices/' +\
                                                          ksdkProj.device[1] + '/startup')
        self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/hal/inc')

        if ksdkProj.libList[0] != 'hal':
            self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/drivers/inc')

        self.cIncludes['listOptionValue'].append(self.projRelPath + 'platform/system/inc')
        self.cIncludes['listOptionValue'].append("../../")

        if ksdkProj.useBSP:
            self.cIncludes['listOptionValue'].append("../../board")

        ## Add device specific driver include paths
        if ksdkProj.libList[0] != 'hal':
            for d in ksdkProj.drvList:
                for p in d[1]:
                    if not self.projRelPath + p in self.cIncludes['listOptionValue']:
                        self.cIncludes['listOptionValue'].append(self.projRelPath + p)
        else:
            for d in ksdkProj.halList:
                for p in d[1]:
                    if not self.projRelPath + p in self.cIncludes['listOptionValue']:
                        self.cIncludes['listOptionValue'].append(self.projRelPath + p)

        # Add rtos paths
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/FreeRTOS/config/' + self.device[1][1:] + '/gcc')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/FreeRTOS/port/gcc')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/FreeRTOS/include')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/FreeRTOS/src')
                self.asmIncludes['listOptionValue'].append(self.projRelPath + 'rtos/FreeRTOS/config/' + self.device[1][1:] + '/gcc')
                #print self.asmIncludes
                #print self.asmIncludes['listOptionValue']
                #print self.asmIncludes['listOptionValue'][0]
            elif ksdkProj.rtos == 'mqx':
                archType = 'M4' if (self.device[4] == 'cm4') else 'M0'
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.atl/debug')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.atl/debug/config')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.atl/debug/mqx')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.atl/debug/mqx_stdlib')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/config/mcu/' + self.device[1])
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/config/board/' + ksdkProj.board[1])
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/bsp')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m/compiler/gcc_arm')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m/core/' + archType)
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m/cpu')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/include')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/config/common')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_dummy')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_mem')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_null')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_pipe')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_serial')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_tfs')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_tty')
            elif ksdkProj.rtos == 'ucosii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSII/src/uCOS-II/Ports/' + archType + '/Generic/GNU')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSII/src/uC-CPU/' + archType + '/GNU')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSII/src/config')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSII/src/uCOS-II/Source')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSII/src/uC-CPU')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSII/src/uC-LIB')
            elif ksdkProj.rtos == 'ucosiii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSIII/src/uCOS-III/Ports/' + archType + '/Generic/GNU')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-CPU/' + archType + '/GNU')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSIII/src/config')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSIII/src/uCOS-III/Source')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-CPU')
                self.cIncludes['listOptionValue'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-LIB')

        if ksdkProj.rtos == 'bm':
            self.linkLibs['libName'][0] = kT.string_replace(self.linkLibs['libName'][0],\
                                                            'xxx', ksdkProj.libList[0])
        else:
            self.linkLibs['libName'][0] = 'ksdk_platform_' + ksdkProj.libList[0]
        self.linkLibs['libName'].append('m')

        self.linkLibs['libPath'][0] = self.projRelPath +  self.linkLibs['libPath'][0]
        self.linkLibs['libPath'][0] = kT.string_replace(self.linkLibs['libPath'][0],\
                                                        'xxx', ksdkProj.libList[0])
        if ksdkProj.rtos != 'bm':
            self.linkLibs['libPath'][0] = kT.string_replace(self.linkLibs['libPath'][0], \
                                        'libksdk_' + ksdkProj.libList[0] + '.a', \
                                        'libksdk_platform_' + ksdkProj.libList[0] + '.a')
        self.linkLibs['libPath'][0] = kT.string_replace(self.linkLibs['libPath'][0], \
                                                      'ddd', ksdkProj.device[1][1:])

        if ksdkProj.rtos == 'mqx':
            mqxLib = '_mqx'
            self.linkLibs['libName'].append(mqxLib)
            mqxPath = self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.atl/debug/mqx'
            self.linkLibs['libPath'].append(mqxPath)
            mqxStdLib = '_mqx_stdlib'
            self.linkLibs['libName'].append(mqxStdLib)
            mqxStdPath = self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.atl/debug/mqx_stdlib'
            self.linkLibs['libPath'].append(mqxStdPath)


        #    l = kT.string_replace(l, 'zzz', ksdkProj.rtos)
        #    kT.debug_log(l)
        #    if self.projType == 'usb':
        #        l = kT.string_replace(l, 'yyy', ksdkProj.board[1])
        #    b = l

        kT.debug_log(self.linkLibs['libName'])
        kT.debug_log(self.linkLibs['libPath'])

        # Configure linker stack and heap
        if self.projType == 'usb':
            if ksdkProj.rtos == 'bm':
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x1000'
            else:
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x1000'

        tree = ET.ElementTree(ET.fromstring(aF.formatted_cproject))
        root = tree.getroot()

        for child in root.findall('storageModule'):
            for config in child.findall('cconfiguration'):
                for module in config.findall('storageModule'):
                    if module.get('moduleId') == "cdtBuildSystem":
                        for configure in module.findall('configuration'):
                            buildVer = configure.get('name')
                            for folder in configure.findall('folderInfo'):
                                for toolC in folder.findall('toolChain'):
                                    #for option in toolC.findall('option'):
                                    #    if option.get('superClass') == "com.atollic.truestudio.as.general.otherflags":
                                    #        option.set('value', " -mcpu=cortex-" + ksdkProj.device[4][1:])
                                    #    if option.get('superClass') == "com.atollic.truestudio.gcc.misc.otherflags":
                                    #        option.set('value', " -mcpu=cortex-" + ksdkProj.device[4][1:])
                                    #    if option.get('superClass') == "com.atollic.truestudio.common_options.target.fpu":
                                    #        optionVal = "hard" if ksdkProj.device[3] else "soft"
                                    #        print optionVal
                                    #        option.set('value', "com.atollic.truestudio.common_options.target.fpu." + optionVal)
                                    for tool in toolC.findall('tool'):
                                        #Add assembler options
                                        if tool.get('name') == "Assembler":
                                            for label in tool.findall('option'):
                                                if label.get('superClass') == "com.atollic.truestudio.common_options.target.fpu":
                                                    optionVal = "hard" if ksdkProj.device[3] else "soft"
                                                    #print optionVal
                                                    label.set('value', "com.atollic.truestudio.common_options.target.fpu." + optionVal)
                                                if label.get('superClass') == "com.atollic.truestudio.as.general.otherflags":
                                                    label.set('value', " -mcpu=cortex-" + ksdkProj.device[4][1:])
                                                if label.get('superClass') == "com.atollic.truestudio.as.general.incpath":
                                                    if ksdkProj.rtos == 'freertos':
                                                        for a in self.asmIncludes['listOptionValue']:
                                                            path = ET.Element('listOptionValue', {'builtIn': 'false', 'value': a})
                                                            label.append(path)
                                        #Add compiler options
                                        if tool.get('name') == "C Compiler":
                                            for label in tool.findall('option'):
                                                #Add include paths
                                                if label.get('superClass') == "com.atollic.truestudio.gcc.directories.select":
                                                    #Add New Include paths
                                                    for i in self.cIncludes['listOptionValue']:
                                                        path = ET.Element('listOptionValue', {'builtIn': 'false', 'value': i})
                                                        label.append(path)
                                                #Add compiler defines
                                                if label.get('superClass') == "com.atollic.truestudio.gcc.symbols.defined":
                                                    # Add new project defines
                                                    for d in self.cDefines['listOptionValue']:
                                                        define = ET.Element('listOptionValue', {'builtIn': 'false', 'value': d})
                                                        label.append(define)
                                                if label.get('superClass') == "com.atollic.truestudio.common_options.target.fpu":
                                                    optionVal = "hard" if ksdkProj.device[3] else "soft"
                                                    #print optionVal
                                                    label.set('value', "com.atollic.truestudio.common_options.target.fpu." + optionVal)
                                                if label.get('superClass') == "com.atollic.truestudio.gcc.misc.otherflags":
                                                    label.set('value', " -mcpu=cortex-" + ksdkProj.device[4][1:])
                                        #Add linker options
                                        if tool.get('name') == "C Linker":
                                            for label in tool.findall('option'):
                                                #Add linker script
                                                if label.get('superClass') == "com.atollic.truestudio.ld.general.scriptfile":
                                                    for l in self.linkLd['listOptionValue']:
                                                        label.set('value', l)
                                                    #Add other objects (.a files such as libksdk_platform.a)
                                                if label.get('superClass') == "com.atollic.truestudio.ld.libraries.list":
                                                    for l in self.linkLibs['libName']:
                                                        lib = ET.Element('listOptionValue', {'builtIn': 'false', 'value': l})
                                                        label.append(lib)
                                                if label.get('superClass') == "com.atollic.truestudio.ld.libraries.searchpath":
                                                    #Add necessary linker objects
                                                    if buildVer == 'debug':
                                                        for l in self.linkLibs['libPath']:
                                                            lib = ET.Element('listOptionValue', {'builtIn': 'false', 'value': l})
                                                            label.append(lib)
                                                    else:
                                                        for l in self.linkLibs['libPath']:
                                                            temp = kT.string_replace(l, 'debug', 'release')
                                                            lib = ET.Element('listOptionValue', {'builtIn': 'false', 'value': temp})
                                                            label.append(lib)
                                                if label.get('superClass') == "com.atollic.truestudio.ld.misc.linkerflags":
                                                    temp = label.get('value')
                                                    if ksdkProj.device[4][1:] != 'm4':
                                                        temp = kT.string_replace(temp, 'm4', ksdkProj.device[4][1:])
                                                    if ksdkProj.rtos != 'bm':
                                                        temp += ' -Xlinker --defsym=__ram_vector_table__=1'
                                                        if ksdkProj.rtos == 'mqx':
                                                            temp += ' -Xlinker --undefined=__isr_vector'
                                                    label.set('value', temp)

        prettyRoot = kT.pretty_xml(root, "UTF-8")

        # Write data to file
        if not os.path.isdir(kdsPath):
            os.makedirs(kdsPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(kdsPath + '/.cproject', "UTF-8")

        kT.cdt_fix_post_xml(kdsPath)

        return

    def gen_project(self, ksdkProj):
        """ Generate the eww files for KDS project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        atlPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl'

        relPath = ''
        if self.isLinked:
            tempStr = kT.get_rel_path(atlPath, ksdkProj.sdkPath) + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../'

        tree = ET.ElementTree(ET.fromstring(aF.formatted_project))
        root = tree.getroot()
        for child in root:
            if child.tag == 'name':
                child.text = str(self.name + '_' + ksdkProj.device[2])
            if child.tag == 'linkedResources':
                #Add linked resources
                if ksdkProj.useBSP == True:
                    #Add board file links
                    for b in self.projBoard:
                        link = ET.Element('link')
                        child.append(link)
                        linkName = ET.Element('name')
                        linkName.text = b['name']
                        link.append(linkName)
                        linkType = ET.Element('type')
                        linkType.text = b['type']
                        link.append(linkType)
                        linkURI = ET.Element('locationURI')
                        linkURI.text = b['locationURI']
                        link.append(linkURI)

                if ksdkProj.libList[0] != 'hal':
                    #Add utilities folder link
                    for u in self.projUtilities:
                        link = ET.Element('link')
                        child.append(link)
                        linkName = ET.Element('name')
                        linkName.text = u['name']
                        link.append(linkName)
                        linkType = ET.Element('type')
                        linkType.text = u['type']
                        link.append(linkType)
                        linkURI = ET.Element('locationURI')
                        if ksdkProj.isLinked:
                            linkURI.text = u['locationURI']
                        else:
                            tempURI = kT.string_replace(u['locationURI'], 'PROJECT_KSDK', 'PARENT-1-PROJECT_LOC')
                            linkURI.text = tempURI
                        link.append(linkURI)

                if ksdkProj.rtos != 'mqx':
                    for s in self.projStartup:
                        link = ET.Element('link')
                        child.append(link)
                        linkName = ET.Element('name')
                        tempName = kT.string_replace(s['name'], 'xxx', ksdkProj.device[1])
                        linkName.text = tempName
                        link.append(linkName)
                        linkType = ET.Element('type')
                        linkType.text = s['type']
                        link.append(linkType)
                        linkURI = ET.Element('locationURI')
                        tempURI = kT.string_replace(s['locationURI'], 'xxx', ksdkProj.device[1])
                        if ksdkProj.isLinked == False:
                            tempURI = kT.string_replace(tempURI, 'PROJECT_KSDK', 'PARENT-1-PROJECT_LOC')
                        #print tempURI
                        linkURI.text = tempURI
                        link.append(linkURI)

                if ksdkProj.rtos != 'bm':
                    for r in self.projRtos:
                        link = ET.Element('link')
                        child.append(link)
                        linkName = ET.Element('name')
                        linkName.text = r['name']
                        link.append(linkName)
                        linkType = ET.Element('type')
                        linkType.text = r['type']
                        link.append(linkType)
                        linkURI = ET.Element('locationURI')
                        if ksdkProj.rtos == 'freertos':
                            tempURI = kT.string_replace(r['locationURI'], 'xxx', ksdkProj.device[1][1:])
                        elif ksdkProj.rtos == 'mqx':
                            tempURI = kT.string_replace(r['locationURI'], 'xxx', ksdkProj.device[1])
                            tempURI = kT.string_replace(r['locationURI'], 'bbb', ksdkProj.board[1])
                        elif ksdkProj.rtos == 'ucosii':
                            archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                            tempURI = kT.string_replace(r['locationURI'], 'ccc', archType)
                        elif ksdkProj.rtos == 'ucosiii':
                            archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                            tempURI = kT.string_replace(r['locationURI'], 'ccc', archType)
                        if ksdkProj.isLinked == False:
                            tempURI = kT.string_replace(tempURI, 'PROJECT_KSDK', 'PARENT-1-PROJECT_LOC')
                        #print tempURI
                        linkURI.text = tempURI
                        link.append(linkURI)

                for c in self.projSources:
                    link = ET.Element('link')
                    child.append(link)
                    linkName = ET.Element('name')
                    linkName.text = c['name']
                    link.append(linkName)
                    linkType = ET.Element('type')
                    linkType.text = c['type']
                    link.append(linkType)
                    linkURI = ET.Element('locationURI')
                    linkURI.text = c['locationURI']
                    link.append(linkURI)

        # Add variable to project for KSDK path
        if ksdkProj.isLinked:
            projVarList = ET.SubElement(root, 'variableList')
            root.append(projVarList)
            projVar = ET.Element('variable')
            projVarList.append(projVar)
            varName = ET.Element('name')
            varName.text = "PROJECT_KSDK"
            projVar.append(varName)
            varVal = ET.Element('value')
            if ksdkProj.osType == 'Windows':
                varVal.text = "file:/" + kT.string_replace(ksdkProj.sdkPath, '\\', '/')
            else:
                varVal.text = "file:" + ksdkProj.sdkPath
            projVar.append(varVal)

        # Format data to make it more readable
        prettyRoot = kT.pretty_xml(root, "UTF-8")

        #print prettyRoot

        # Write data to file
        if not os.path.isdir(atlPath):
            os.mkdir(atlPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(atlPath + '/.project', "UTF-8")

        return

    def gen_debug(self, ksdkProj):
        """ Generate debug launch files
        """

        # Get relative path
        atlPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl'

        tree = ET.ElementTree(ET.fromstring(aF.project_board_debug_jlink_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' debug jlink.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'jlinkDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(aF.project_board_release_jlink_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' release jlink.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'jlinkDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(aF.project_board_debug_pne_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' debug pne.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'pneDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(aF.project_board_release_pne_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' release pne.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'pneDEVICE', self.device[0])

        return

    def gen_settings(self, ksdkProj):
        """ Generate settings files for ATL project
        """

        atlPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl/.settings'

        # Write data to file
        if not os.path.isdir(atlPath):
            os.mkdir(atlPath)

        tree = ET.ElementTree(ET.fromstring(aF.language_settings_xml))
        launchPath = atlPath + '/language.settings.xml'
        tree.write(launchPath, "UTF-8")

        setPath = atlPath + '/com.atollic.truestudio.debug.hardware_device.prefs'
        setContent = aF.com_atollic_truestudio_debug_hardware_device_prefs
        setContent = kT.string_replace(setContent, 'settingDevice', self.device[0])
        with open(setPath, 'wb+') as f:
            f.write(setContent)
            f.close()

        return

