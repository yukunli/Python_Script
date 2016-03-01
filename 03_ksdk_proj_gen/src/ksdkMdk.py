"""
File:  ksdkMdk.py
===================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Methods for MDK project creation for KSDK**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.6

UML
+++
.. uml:: {{/../../../src/ksdkIar.py

API
+++

"""

## USER MODULES
from ksdkTools import KsdkTools as kT
from ksdkProj import ksdkProjClass
import mdkFiles as mF

## PYTHON MODULES
import copy
import os
import xml.etree.ElementTree as ET

## Important ewp tags
CDEFINES = {'name': 'Define', 'state': []}
CDEFINES_USB = {'name': 'Define', 'state': ['_DEBUG=1']}
CINCLUDES = {'name': 'IncludePath', 'state': []}
ASMDEFINES = {'name': 'ADefines', 'state': ['DEBUG']}
ASMINCLUDES = {'name': 'AUserIncludes', 'state': []}
LINKOUT = {'name': 'OutputName', 'state': ''}
LINKDEFINES = {'name': 'Misc', 'state': ['__stack_size__=', '__heap_size__=']}
LINKDEFINES_USB = {'name': 'Misc', \
                  'state': ['__ram_vector_table__=1', '__stack_size__=', '__heap_size__=']}
LINKSCF = {'name': 'ScatterFile', 'state': []}
LINKLIBS = {'name': 'Misc', \
           'state': ['lib/ksdk_xxx_lib/mdk/ddd/debug/libksdk_xxx.lib']}
LINKLIBS_USB = {'name': 'Misc', \
               'state': ['usb/usb_core/device/build/mdk/usbd_sdk_yyy_zzz/debug/libusbd_zzz.lib', \
                         'usb/usb_core/device/build/mdk/usbd_sdk_yyy_zzz/debug/libusbd_zzz.lib', \
                         'lib/ksdk_xxx_lib/mdk/ddd/debug/libksdk_xxx.lib']}

PROJ_STARTUP =\
{'GroupName': 'startup',\
  'FileName': ['startup_xxx.s', \
               'system_xxx.c', \
               'system_xxx.h', \
               'startup.c', \
               'startup.h'],\
  'FileType': ['2', '1', '5', '1', '5'],\
  'FilePath': ['platform/devices/xxx/startup/arm/startup_xxx.s', \
               'platform/devices/xxx/startup/system_xxx.c', \
               'platform/devices/xxx/startup/system_xxx.h', \
               'platform/devices/startup.c', \
               'platform/devices/startup.h'],\
}

PROJ_UTILITIES =\
{'GroupName': 'utilities',\
  'FileName': ['fsl_misc_utilities.c', \
               'fsl_debug_console.c', \
               'fsl_debug_console.h', \
               'print_scan.c', \
               'print_scan.h'],\
  'FileType': ['1', '1', '5', '1', '5'],\
  'FilePath': ['platform/utilities/src/fsl_misc_utilities.c', \
               'platform/utilities/src/fsl_debug_console.c', \
               'platform/utilities/inc/fsl_debug_console.h', \
               'platform/utilities/src/print_scan.c', \
               'platform/utilities/src/print_scan.h'],\
}

PROJ_BOARD =\
{'GroupName': 'board',\
  'FileName': ['gpio_pins.c', \
               'gpio_pins.h', \
               'pin_mux.c', \
               'pin_mux.h',\
               'board.c', \
               'board.h', \
               'hardware_init.c'],\
  'FileType': ['1', '5', '1', '5', '1', '5', '1'],\
  'FilePath': ['../board/gpio_pins.c', \
               '../board/gpio_pins.h', \
               '../board/pin_mux.c', \
               '../board/pin_mux.h',\
               '../board/board.c', \
               '../board/board.h', \
               '../hardware_init.c']
}

PROJ_SOURCES =\
{'GroupName': 'sources',\
  'FileName': ['main.c', \
               'main.h'],\
  'FileType': ['1', '5'],\
  'FilePath': ['../main.c',\
               '../main.h']
}

PROJ_FREERTOS =\
{
    'GroupName': 'free-rtos',\
    'FileName': ['FreeRTOSConfig.h',\
                 'croutine.h',\
                 'event_groups.h',\
                 'FreeRTOS.h',\
                 'list.h',\
                 'mpu_wrappers.h',\
                 'portable.h',\
                 'projdefs.h',\
                 'queue.h',\
                 'semphr.h',\
                 'StackMacros.h',\
                 'task.h',\
                 'timers.h',\
                 'port.c',\
                 'portasm.s',\
                 'portmacro.h',\
                 'portTicks.h',\
                 'croutine.c',\
                 'event_groups.c',\
                 'heap_1.c',\
                 'heap_2.c',\
                 'heap_3.c',\
                 'heap_4.c',\
                 'list.c',\
                 'queue.c',\
                 'tasks.c',\
                 'timers.c'],
    'FileType': ['5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '1',\
                 '2',\
                 '5',\
                 '5',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1'],
    'FilePath': ['rtos/FreeRTOS/config/xxx/iar/FreeRTOSConfig.h',\
                 'rtos/FreeRTOS/include/croutine.h',\
                 'rtos/FreeRTOS/include/event_groups.h',\
                 'rtos/FreeRTOS/include/FreeRTOS.h',\
                 'rtos/FreeRTOS/include/list.h',\
                 'rtos/FreeRTOS/include/mpu_wrappers.h',\
                 'rtos/FreeRTOS/include/portable.h',\
                 'rtos/FreeRTOS/include/projdefs.h',\
                 'rtos/FreeRTOS/include/queue.h',\
                 'rtos/FreeRTOS/include/semphr.h',\
                 'rtos/FreeRTOS/include/StackMacros.h',\
                 'rtos/FreeRTOS/include/task.h',\
                 'rtos/FreeRTOS/include/timers.h',\
                 'rtos/FreeRTOS/port/mdk/port.c',\
                 'rtos/FreeRTOS/port/mdk/portasm.S',\
                 'rtos/FreeRTOS/port/mdk/portmacro.h',\
                 'rtos/FreeRTOS/port/mdk/portTicks.h',\
                 'rtos/FreeRTOS/src/croutine.c',\
                 'rtos/FreeRTOS/src/event_groups.c',\
                 'rtos/FreeRTOS/src/heap_1.c',\
                 'rtos/FreeRTOS/src/heap_2.c',\
                 'rtos/FreeRTOS/src/heap_3.c',\
                 'rtos/FreeRTOS/src/heap_4.c',\
                 'rtos/FreeRTOS/src/list.c',\
                 'rtos/FreeRTOS/src/queue.c',\
                 'rtos/FreeRTOS/src/tasks.c',\
                 'rtos/FreeRTOS/src/timers.c']
}

PROJ_MQX =\
{
    'GroupName': 'mqx',\
    'FileName': ['bsp.h',\
                 'bsp_config.h',\
                 'init_bsp.c',\
                 'mqx_main.c',\
                 'include/mqx.h',\
                 'lite_config.h',\
                 'mqx_cnfg.h',\
                 'small_ram_config.h',\
                 'verif_enabled_config.h',\
                 'mqx_sdk_config.h',\
                 'user_config.h'],
    'FileType': ['5',\
                 '5',\
                 '1',\
                 '1',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5',\
                 '5'],
    'FilePath': ['rtos/mqx/mqx/source/bsp/bsp.h',\
                 'rtos/mqx/mqx/source/bsp/bsp_config.h',\
                 'rtos/mqx/mqx/source/bsp/init_bsp.c',\
                 'rtos/mqx/mqx/source/bsp/mqx_main.c',\
                 'rtos/mqx/mqx/source/include/mqx.h',\
                 'rtos/mqx/config/common/lite_config.h',\
                 'rtos/mqx/config/common/mqx_cnfg.h',\
                 'rtos/mqx/config/common/small_ram_config.h',\
                 'rtos/mqx/config/common/verif_enabled_config.h',\
                 'rtos/mqx/config/mcu/xxx/mqx_sdk_config.h',\
                 'rtos/mqx/config/board/bbb/user_config.h']
}

PROJ_UCOSII =\
{
    'GroupName': 'ucosii',\
    'FileName': ['app_hooks.c',\
                 'os_core.c',\
                 'os_cpu.h',\
                 'os_cpu_a.s', \
                 'os_cpu_c.c', \
                 'os_dbg.c', \
                 'os_flag.c',\
                 'os_mbox.c', \
                 'os_mem.c', \
                 'os_mutex.c', \
                 'os_q.c', \
                 'os_sem.c', \
                 'os_task.c', \
                 'os_time.c', \
                 'os_tmr.c'],
    'FileType': ['1',\
                 '1',\
                 '5',\
                 '2', \
                 '1', \
                 '1', \
                 '1',\
                 '1', \
                 '1', \
                 '1', \
                 '1', \
                 '1', \
                 '1', \
                 '1', \
                 '1'],
    'FilePath': ['rtos/uCOSII/src/config/app_hooks.c',\
                 'rtos/uCOSII/src/uCOS-II/Source/os_core.c',\
                 'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/RealView/os_cpu.h',\
                 'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/RealView/os_cpu_a.s', \
                 'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/RealView/os_cpu_c.c', \
                 'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/RealView/os_dbg.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_flag.c',\
                 'rtos/uCOSII/src/uCOS-II/Source/os_mbox.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_mem.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_mutex.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_q.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_sem.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_task.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_time.c', \
                 'rtos/uCOSII/src/uCOS-II/Source/os_tmr.c']
}

PROJ_UCOSIII =\
{
    'GroupName': 'ucosiii',\
    'FileName': ['cpu_core.c',\
                 'cpu_a.s',\
                 'cpu_c.c',\
                 'os.h',\
                 'os_app_hooks.c',\
                 'os_cfg_app.c',\
                 'os_core.c',\
                 'os_cpu.h',\
                 'os_cpu_a.s',\
                 'os_cpu_c.c',\
                 'os_dbg.c',\
                 'os_flag.c',\
                 'os_init.c',\
                 'os_mem.c',\
                 'os_msg.c',\
                 'os_mutex.c',\
                 'os_pend_multi.c',\
                 'os_prio.c',\
                 'os_q.c',\
                 'os_sem.c',\
                 'os_stat.c',\
                 'os_task.c',\
                 'os_tick.c',\
                 'os_time.c',\
                 'os_tmr.c',\
                 'os_type.h',\
                 'os_var.c'],
    'FileType': ['1',\
                 '2',\
                 '1',\
                 '5',\
                 '1',\
                 '1',\
                 '1',\
                 '5',\
                 '2',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '1',\
                 '5',\
                 '1'],
    'FilePath': ['rtos/uCOSIII/src/uC-CPU/cpu_core.c',\
                 'rtos/uCOSIII/src/uC-CPU/ccc/RealView/cpu_a.s',\
                 'rtos/uCOSIII/src/uC-CPU/ccc/RealView/cpu_c.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os.h',\
                 'rtos/uCOSIII/src/config/os_app_hooks.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_cfg_app.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_core.c',\
                 'rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/RealView/os_cpu.h',\
                 'rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/RealView/os_cpu_a.s',\
                 'rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/RealView/os_cpu_c.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_dbg.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_flag.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_int.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_mem.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_msg.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_mutex.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_pend_multi.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_prio.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_q.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_sem.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_stat.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_task.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_tick.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_time.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_tmr.c',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_type.h',\
                 'rtos/uCOSIII/src/uCOS-III/Source/os_var.c']
}

WKSPACE_PROJECTS = \
{'PathAndName': ['lib/ksdk_xxx_lib/mdk/ddd/ksdk_xxx_lib.uvprojx',\
                 '.uvprojx'],\
'NodeIsActive': ['0', '1']
}


class KsdkMdk(object):
    """ Class for generating Keil MDK-ARM projects

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
        self.linkScf = copy.deepcopy(LINKSCF)
        self.asmDefines = copy.deepcopy(ASMDEFINES)
        self.asmIncludes = copy.deepcopy(ASMINCLUDES)

        self.projStartup = copy.deepcopy(PROJ_STARTUP)
        self.projUtilities = copy.deepcopy(PROJ_UTILITIES)
        self.projBoard = copy.deepcopy(PROJ_BOARD)
        self.projSources = copy.deepcopy(PROJ_SOURCES)

        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.projRtos = copy.deepcopy(PROJ_FREERTOS)
            elif ksdkProj.rtos == 'mqx':
                self.projRtos = copy.deepcopy(PROJ_MQX)
            elif ksdkProj.rtos == 'ucosii':
                self.projRtos = copy.deepcopy(PROJ_UCOSII)
            elif ksdkProj.rtos == 'ucosiii':
                self.projRtos = copy.deepcopy(PROJ_UCOSIII)

        self.wsProjects = copy.deepcopy(WKSPACE_PROJECTS)

        return

    def gen_proj(self, ksdkProj):
        """ Generate the uvprojx files for Keil project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        mdkPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/mdk'

        relPath = ''
        if self.isLinked:
            tempStr = kT.get_rel_path(mdkPath, ksdkProj.sdkPath) + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../'

        self.projRelPath = relPath

        ## Configure linker option
        self.linkScf['state'] = self.projRelPath + 'platform/devices/' +\
                                ksdkProj.device[1] + '/linker/arm/' +\
                                ksdkProj.device[0] + '_flash.scf'

        ## Set a define for the device
        self.cDefines['state'].append('CPU_' + ksdkProj.device[2])
        ##                Added to fix K80 application build issues                   ##
        #if (ksdkProj.device[1] == 'MK80F25615') or (ksdkProj.device[1] == 'MK82F25615'):
        #    self.cDefines['state'].append('USING_DIRECT_INTERFACE=1')
        ##                Added to fix UART smartcard application build issues        ##
        if ksdkProj.libList[0] != 'hal':
            for d in ksdkProj.drvList:
                if d[0] == 'smartcard':
                    if kT.get_smartcard_type(ksdkProj.sdkPath, ksdkProj.device[1]) == (1 << 8):
                        self.cDefines['state'].append('USING_DIRECT_INTERFACE=1')
                    elif kT.get_smartcard_type(ksdkProj.sdkPath, ksdkProj.device[1]) == 1:
                        self.cDefines['state'].append('USING_NCN8025_INTERFACE=1')
        ################################################################################
        if ksdkProj.useBSP:
            boardType = ksdkProj.board[0][:ksdkProj.board[0].find('_')]
            self.cDefines['state'].append(ksdkProj.board[0])
            if boardType == 'FRDM':
                self.cDefines['state'].append('FREEDOM')
            elif boardType == 'TWR':
                self.cDefines['state'].append('TOWER')
            elif boardType == 'USB':
                self.cDefines['state'].append('BOARD_USE_VIRTUALCOM')
                self.cDefines['state'].append('DONGLE')
            elif boardType == 'MRB':
                self.cDefines['state'].append('MRB_KW01')
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.cDefines['state'].append('FSL_RTOS_FREE_RTOS')
            elif ksdkProj.rtos == 'mqx':
                self.cDefines['state'].append('FSL_RTOS_MQX')
            elif ksdkProj.rtos == 'ucosii':
                self.cDefines['state'].append('FSL_RTOS_UCOSII')
            elif ksdkProj.rtos == 'ucosiii':
                self.cDefines['state'].append('FSL_RTOS_UCOSIII')

        ## Add C include paths necessary for project
        if ksdkProj.libList[0] != 'hal':
            self.cIncludes['state'].append(self.projRelPath + 'platform/osa/inc')
            self.cIncludes['state'].append(self.projRelPath + 'platform/utilities/inc')

        self.cIncludes['state'].append(self.projRelPath + 'platform/CMSIS/Include')
        self.cIncludes['state'].append(self.projRelPath + 'platform/devices')
        self.cIncludes['state'].append(self.projRelPath + 'platform/devices/' +\
                                                          ksdkProj.device[1] + '/include')
        self.cIncludes['state'].append(self.projRelPath + 'platform/devices/' +\
                                                          ksdkProj.device[1] + '/startup')
        self.cIncludes['state'].append(self.projRelPath + 'platform/hal/inc')

        if ksdkProj.libList[0] != 'hal':
            self.cIncludes['state'].append(self.projRelPath + 'platform/drivers/inc')

        self.cIncludes['state'].append(self.projRelPath + 'platform/system/inc')
        self.cIncludes['state'].append("../../")

        if ksdkProj.useBSP:
            self.cIncludes['state'].append("../board")

        ## Add device specific driver include paths
        if ksdkProj.libList[0] != 'hal':
            for d in ksdkProj.drvList:
                for p in d[1]:
                    if not self.projRelPath + p in self.cIncludes['state']:
                        self.cIncludes['state'].append(self.projRelPath + p)
        else:
            for d in ksdkProj.halList:
                for p in d[1]:
                    if not self.projRelPath + p in self.cIncludes['state']:
                        self.cIncludes['state'].append(self.projRelPath + p)

        # Add rtos paths
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/config/' + self.device[1][1:] + '/mdk')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/port/mdk')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/include')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/src')
                self.asmIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/config/' + self.device[1][1:] + '/mdk')
                #print self.asmIncludes
                #print self.asmIncludes['state']
                #print self.asmIncludes['state'][0]
            elif ksdkProj.rtos == 'mqx':
                archType = 'M4' if (self.device[4] == 'cm4') else 'M0'
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.mdk/debug')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.mdk/debug/config')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.mdk/debug/mqx')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.mdk/debug/mqx_stdlib')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/config/mcu/' + self.device[1])
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/config/board/' + ksdkProj.board[1])
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/bsp')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m/compiler/rv_mdk')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m/core/' + archType)
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m/cpu')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/include')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/config/common')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_dummy')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_mem')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_null')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_pipe')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_serial')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_tfs')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/nio/drivers/nio_tty')
            elif ksdkProj.rtos == 'ucosii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uCOS-II/Ports/' + archType + '/Generic/RealView')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uC-CPU/' + archType + '/RealView')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/config')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uCOS-II/Source')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uC-CPU')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uC-LIB')
            elif ksdkProj.rtos == 'ucosiii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uCOS-III/Ports/' + archType + '/Generic/RealView')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-CPU/' + archType + '/RealView')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/config')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uCOS-III/Source')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-CPU')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-LIB')

        # Add relative paths to files
        prePend = self.projRelPath + '{0}'
        self.projStartup['FileName'] = [f.replace('xxx', ksdkProj.device[1]) for f in self.projStartup['FileName']]
        self.projStartup['FilePath'] = [f.replace('xxx', ksdkProj.device[1]) for f in self.projStartup['FilePath']]
        self.projStartup['FilePath'] = [prePend.format(f) for f in self.projStartup['FilePath']]

        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                index = 0
                while index < len(self.projRtos['FilePath']):
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'xxx',\
                                                ksdkProj.device[1][1:])
                    self.projRtos['FilePath'][index] = self.projRelPath + self.projRtos['FilePath'][index]
                    index += 1
            elif ksdkProj.rtos == 'mqx':
                index = 0
                while index < len(self.projRtos['FilePath']):
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'xxx',\
                                                ksdkProj.device[1])
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'bbb',\
                                                ksdkProj.board[1])
                    self.projRtos['FilePath'][index] = self.projRelPath + self.projRtos['FilePath'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.projRtos['FilePath']):
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'ccc',\
                                                archType)
                    self.projRtos['FilePath'][index] = self.projRelPath + self.projRtos['FilePath'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosiii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.projRtos['FilePath']):
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'ccc',\
                                                archType)
                    self.projRtos['FilePath'][index] = self.projRelPath + self.projRtos['FilePath'][index]
                    index += 1

        kT.debug_log(self.projStartup['FileName'])
        kT.debug_log(self.projStartup['FilePath'])

        if ksdkProj.libList[0] != 'hal':
            self.projUtilities['FilePath'] = [prePend.format(f) for f in self.projUtilities['FilePath']]

        self.linkLibs['state'][0] = self.projRelPath +  self.linkLibs['state'][0]
        self.linkLibs['state'][0] = kT.string_replace(self.linkLibs['state'][0], \
                                                      'xxx', ksdkProj.libList[0])
        if ksdkProj.rtos != 'bm':
            self.linkLibs['state'][0] = kT.string_replace(self.linkLibs['state'][0], \
                                        'libksdk_' + ksdkProj.libList[0] + '.lib', \
                                        'libksdk_platform_' + ksdkProj.libList[0] + '.lib')
        self.linkLibs['state'][0] = kT.string_replace(self.linkLibs['state'][0], \
                                                      'ddd', ksdkProj.device[1][1:])

        if ksdkProj.rtos == 'mqx':
            mqxLib = self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.mdk/debug/mqx/lib_mqx.lib'
            self.linkLibs['state'].append(mqxLib)
            mqxStdLib = self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.mdk/debug/mqx_stdlib/lib_mqx_stdlib.lib'
            self.linkLibs['state'].append(mqxStdLib)

        projMem = self.get_memory_loc(ksdkProj)
        #print 'Memory loc/size: ' + str(projMem)

        peDebug = "PEMicro\\Pemicro_ArmCortexInterface.dll"
        cmDebug = "BIN\\CMSIS_AGDI.dll"

        tree = ET.ElementTree(ET.fromstring(mF.mdk_formatted_uvprojx))
        for elem in tree.iter(tag='TargetName'):
            if 'Debug' in elem.text:
                elem.text = self.name + ' Debug'
            else:
                elem.text = self.name + ' Release'
        for elem in tree.iter(tag='Device'):
            elem.text = self.device[0]
        for elem in tree.iter(tag='OutputName'):
            elem.text = self.name + '.out'
        for elem in tree.iter(tag='Driver'):
            elem.text = cmDebug if (self.device[4] == 'cm4') else peDebug
        for elem in tree.iter(tag='AdsCpuType'):
            elem.text = "\"Cortex-M4\"" if (self.device[4] == 'cm4') else "\"Cortex-M0+\""
        for elem in tree.iter(tag='RvdsVP'):
            elem.text = '2' if self.device[3] else '1'
        for elem in tree.iter(tag='Ir1Chk'):
            elem.text = '1'
        for elem in tree.iter(tag='Im1Chk'):
            elem.text = '1'
        for elem in tree.iter(tag='Im2Chk'):
            elem.text = '0' if (projMem[4] == '') else '1'
        for elem in tree.iter(tag='IRAM'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[2]
            for child in elem.findall('Size'):
                child.text = projMem[3]
        for elem in tree.iter(tag='IROM'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[0]
            for child in elem.findall('Size'):
                child.text = projMem[1]
        for elem in tree.iter(tag='OCR_RVCT4'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[0]
            for child in elem.findall('Size'):
                child.text = projMem[1]
        for elem in tree.iter(tag='OCR_RVCT9'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[2]
            for child in elem.findall('Size'):
                child.text = projMem[3]
        for elem in tree.iter(tag='OCR_RVCT10'):
            for child in elem.findall('StartAddress'):
                child.text = '0x0' if (projMem[4] == '') else projMem[4]
            for child in elem.findall('Size'):
                child.text = '0x0' if (projMem[5] == '') else projMem[5]
        for elem in tree.iter(tag='Cads'):
            for child in elem.findall('VariousControls'):
                for defs in child.findall('Define'):
                    temp = defs.text
                    for d in self.cDefines['state']:
                        temp += ', ' + d
                    defs.text = temp
                for incl in child.findall('IncludePath'):
                    temp = incl.text
                    for i in self.cIncludes['state']:
                        temp += '; ' + i
                    incl.text = temp
        for elem in tree.iter(tag='Aads'):
            if ksdkProj.rtos == 'freertos':
                for child in elem.findall('VariousControls'):
                    for incl in child.findall('IncludePath'):
                        incl.text = self.asmIncludes['state'][0]
        for elem in tree.iter(tag='ScatterFile'):
            elem.text = self.linkScf['state']
        for elem in tree.iter(tag='Misc'):
            temp = self.linkLibs['state'][0] + ' '
            if ksdkProj.rtos != 'bm':
                if ksdkProj.rtos == 'mqx':
                    temp += self.linkLibs['state'][1] + ' '
                    temp += self.linkLibs['state'][2] + ' '
                    temp += self.linkLibs['state'][1] + '(boot.o)' + ' '
                    temp += self.linkLibs['state'][1] + '(startup_*.o)' + ' '
                temp += ' --remove '
                temp += ' --predefine="-D__stack_size__=0x1000" '
                temp += ' --predefine="-D__heap_size__=0x1000" '
                temp += '--predefine="-D__ram_vector_table__=1" '
            elem.text = temp
        for elem in tree.iter(tag='Groups'):
            if ksdkProj.rtos != 'mqx':
                # Add startup files
                group = ET.SubElement(elem, 'Group')
                name = ET.SubElement(group, 'GroupName')
                name.text = self.projStartup['GroupName']
                files = ET.SubElement(group, 'Files')
                index = 0
                while index < len(self.projStartup['FileName']):
                    newFile = ET.SubElement(files, 'File')
                    fileName = ET.SubElement(newFile, 'FileName')
                    fileType = ET.SubElement(newFile, 'FileType')
                    filePath = ET.SubElement(newFile, 'FilePath')
                    fileName.text = self.projStartup['FileName'][index]
                    fileType.text = self.projStartup['FileType'][index]
                    filePath.text = self.projStartup['FilePath'][index]
                    index += 1
            # Add source files
            group = ET.SubElement(elem, 'Group')
            name = ET.SubElement(group, 'GroupName')
            name.text = self.projSources['GroupName']
            files = ET.SubElement(group, 'Files')
            index = 0
            while index < len(self.projSources['FileName']):
                newFile = ET.SubElement(files, 'File')
                fileName = ET.SubElement(newFile, 'FileName')
                fileType = ET.SubElement(newFile, 'FileType')
                filePath = ET.SubElement(newFile, 'FilePath')
                fileName.text = self.projSources['FileName'][index]
                fileType.text = self.projSources['FileType'][index]
                filePath.text = self.projSources['FilePath'][index]
                index += 1
            # Add board files if needed
            if ksdkProj.useBSP:
                group = ET.SubElement(elem, 'Group')
                name = ET.SubElement(group, 'GroupName')
                name.text = self.projBoard['GroupName']
                files = ET.SubElement(group, 'Files')
                index = 0
                while index < len(self.projBoard['FileName']):
                    newFile = ET.SubElement(files, 'File')
                    fileName = ET.SubElement(newFile, 'FileName')
                    fileType = ET.SubElement(newFile, 'FileType')
                    filePath = ET.SubElement(newFile, 'FilePath')
                    fileName.text = self.projBoard['FileName'][index]
                    fileType.text = self.projBoard['FileType'][index]
                    filePath.text = self.projBoard['FilePath'][index]
                    index += 1
            # Add utilities in needed
            if ksdkProj.libList[0] != 'hal':
                group = ET.SubElement(elem, 'Group')
                name = ET.SubElement(group, 'GroupName')
                name.text = self.projUtilities['GroupName']
                files = ET.SubElement(group, 'Files')
                index = 0
                while index < len(self.projUtilities['FileName']):
                    newFile = ET.SubElement(files, 'File')
                    fileName = ET.SubElement(newFile, 'FileName')
                    fileType = ET.SubElement(newFile, 'FileType')
                    filePath = ET.SubElement(newFile, 'FilePath')
                    fileName.text = self.projUtilities['FileName'][index]
                    fileType.text = self.projUtilities['FileType'][index]
                    filePath.text = self.projUtilities['FilePath'][index]
                    index += 1
            # Add RTOS files if needed
            if ksdkProj.rtos != 'bm':
                group = ET.SubElement(elem, 'Group')
                name = ET.SubElement(group, 'GroupName')
                name.text = self.projRtos['GroupName']
                files = ET.SubElement(group, 'Files')
                index = 0
                while index < len(self.projRtos['FileName']):
                    newFile = ET.SubElement(files, 'File')
                    fileName = ET.SubElement(newFile, 'FileName')
                    fileType = ET.SubElement(newFile, 'FileType')
                    filePath = ET.SubElement(newFile, 'FilePath')
                    fileName.text = self.projRtos['FileName'][index]
                    fileType.text = self.projRtos['FileType'][index]
                    filePath.text = self.projRtos['FilePath'][index]
                    index += 1

        root = tree.getroot()
        prettyRoot = kT.pretty_xml(root, "UTF-8")

        # Write data to file
        if not os.path.isdir(mdkPath):
            os.makedirs(mdkPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(mdkPath + '/' + self.name + '.uvprojx', "UTF-8")

        if 'MKL' in self.device[0]:
            setPath = mdkPath + '/pemicro_connection_settings.ini'
            setContent = mF.pemicro_connection_settings_ini
            setContent = kT.string_replace(setContent, 'dev_name', self.device[0][1:].replace('xxx', 'M'))
            with open(setPath, 'wb+') as f:
                f.write(setContent)
                f.close()

        return

    def gen_wkspace(self, ksdkProj):
        """ Generate the uvmpw files for Keil project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        mdkPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/mdk'

        relPath = ''
        if self.isLinked:
            tempStr = ksdkProj.sdkPath + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../'

        self.projRelPath = relPath

        self.wsProjects['PathAndName'][0] = self.projRelPath +  self.wsProjects['PathAndName'][0]
        self.wsProjects['PathAndName'][0] = kT.string_replace(self.wsProjects['PathAndName'][0], \
                                                      'xxx', ksdkProj.libList[0])
        if ksdkProj.rtos != 'bm':
            self.wsProjects['PathAndName'][0] = kT.string_replace(self.wsProjects['PathAndName'][0], \
                                        'libksdk_' + ksdkProj.libList[0] + '.lib', \
                                        'libksdk_platform_' + ksdkProj.libList[0] + '.lib')
        self.wsProjects['PathAndName'][0] = kT.string_replace(self.wsProjects['PathAndName'][0], \
                                                      'ddd', ksdkProj.device[1][1:])

        self.wsProjects['PathAndName'][1] = self.name + '.uvprojx'

        if ksdkProj.rtos == 'mqx':
            mqxLib = self.projRelPath + 'rtos/mqx/mqx/build/mdk/mqx_' + ksdkProj.board[1] + '/mqx_' + ksdkProj.board[1] + '.uvprojx'
            self.wsProjects['PathAndName'].insert(1, mqxLib)
            self.wsProjects['NodeIsActive'].insert(1, '0')
            mqxStdLib = self.projRelPath + 'rtos/mqx/mqx_stdlib/build/mdk/mqx_stdlib_' + ksdkProj.board[1] + '/mqx_stdlib_' + ksdkProj.board[1] + '.uvprojx'
            self.wsProjects['PathAndName'].insert(2, mqxStdLib)
            self.wsProjects['NodeIsActive'].insert(2, '0')

        tree = ET.ElementTree(ET.fromstring(mF.mdk_formatted_uvmpw))

        root = tree.getroot()
        index = 0
        while index < len(self.wsProjects['PathAndName']):
            project = ET.Element('project')
            root.append(project)
            pathName = ET.SubElement(project, 'PathAndName')
            pathName.text = self.wsProjects['PathAndName'][index]
            isActive = ET.SubElement(project, 'NodeIsActive')
            isActive.text = self.wsProjects['NodeIsActive'][index]
            index += 1

        #print 'Project count: ' + str(index)

        prettyRoot = kT.pretty_xml(root, "UTF-8")

        # Write data to file
        if not os.path.isdir(mdkPath):
            os.makedirs(mdkPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(mdkPath + '/' + self.name + '.uvmpw', "UTF-8")

        return


    def get_memory_loc(self, ksdkProj):
        """ Get memory local and return tuple of memory information from scatter file
        """

        scatPath = ksdkProj.sdkPath + '/platform/devices/' + self.device[1] + '/linker/arm/' + self.device[0] + '_flash.scf'

        textStart = ''
        textSize = ''
        dataStart1 = ''
        dataSize1 = ''
        dataStart2 = ''
        dataSize2 = ''

        with open(scatPath, 'rb') as f:
            for newLine in f:
                if '#define m_interrupts_start' in newLine:
                    temp = newLine.rfind('0x')
                    textStart = newLine[temp:(temp + 10)]
                if '#define m_text_size' in newLine:
                    #print newLine
                    temp = newLine.rfind('0x')
                    #print 'Text size line: ' + str(temp)
                    #print 'Text size: ' + newLine[temp:temp + 10]
                    tempInt = int(newLine[temp:temp + 10], 16)
                    #print 'Text size int: ' + str(tempInt)
                    tempInt += int("0x410", 16)
                    textSize = hex(tempInt)
                if '#define m_interrupts_ram_start' in newLine:
                    temp = newLine.rfind('0x')
                    dataStart1 = newLine[temp:(temp + 10)]
                if '#define m_data_2_start' in newLine:
                    temp = newLine.rfind('0x')
                    dataStart2 = newLine[temp:(temp + 10)]
                if '#define m_data_size' in newLine:
                    temp = newLine.rfind('0x')
                    dataSize1 = newLine[temp:(temp + 10)]
                if '#define m_data_2_size' in newLine:
                    temp = newLine.rfind('0x')
                    dataSize2 = newLine[temp:(temp + 10)]
            f.close()

        return (textStart, textSize, dataStart1, dataSize1, dataStart2, dataSize2)
