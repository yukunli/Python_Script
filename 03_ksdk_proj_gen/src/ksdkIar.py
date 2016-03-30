"""
File:  ksdkIar.py
===================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Methods for IAR project creation for KSDK**

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
import iarFiles as iF

## PYTHON MODULES
import copy
import os
import xml.etree.ElementTree as ET

## Important ewp tags
CDEFINES = {'name': 'CCDefines', 'state': []}
CDEFINES_USB = {'name': 'CCDefines', 'state': ['_DEBUG=1']}
CINCLUDES = {'name': 'CCIncludePath2', 'state': []}
ASMDEFINES = {'name': 'ADefines', 'state': ['DEBUG']}
ASMINCLUDES = {'name': 'AUserIncludes', 'state': []}
LINKOUT = {'name': 'IlinkOutputFile', 'state': '.out'}
LINKDEFINES = {'name': 'IlinkConfigDefines', 'state': ['__stack_size__=', '__heap_size__=']}
LINKDEFINES_USB = {'name': 'IlinkConfigDefines', \
                  'state': ['__ram_vector_table__=1', '__stack_size__=', '__heap_size__=']}
LINKICF = {'name': 'IlinkIcfFile', 'state': ['.icf']}
LINKLIBS = {'name': 'IlinkAdditionalLibs', \
           'state': ['lib/ksdk_xxx_lib/iar/ddd/debug/libksdk_xxx.a']}
LINKLIBS_USB = {'name': 'IlinkAdditionalLibs', \
               'state': ['lib/ksdk_xxx_lib/iar/ddd/debug/libksdk_xxx.a', \
                         'usb/usb_core/device/build/iar/usbd_sdk_yyy_zzz/debug/libusbd_zzz.a', \
                         'usb/usb_core/device/build/iar/usbh_sdk_yyy_zzz/debug/libusbh_zzz.a']}

EWP_STARTUP =\
{'name': 'startup',\
 'file': ['platform/devices/xxx/startup/iar/startup_xxx.s', \
          'platform/devices/xxx/startup/system_xxx.c', \
          'platform/devices/xxx/startup/system_xxx.h', \
          'platform/devices/startup.c', \
          'platform/devices/startup.h']
}

EWP_UTILITIES =\
{'name': 'utilities',\
 'file': ['platform/utilities/src/fsl_debug_console.c', \
          'platform/utilities/inc/fsl_debug_console.h', \
          'platform/utilities/src/print_scan.c', \
          'platform/utilities/inc/print_scan.h']
}

EWP_BOARD =\
{'name': 'board',\
 'file': ['$PROJ_DIR$/../board/gpio_pins.c', \
          '$PROJ_DIR$/../board/gpio_pins.h', \
          '$PROJ_DIR$/../board/pin_mux.c', \
          '$PROJ_DIR$/../board/pin_mux.h',\
          '$PROJ_DIR$/../board/board.c', \
          '$PROJ_DIR$/../board/board.h', \
          '$PROJ_DIR$/../hardware_init.c']
}

EWP_SOURCES =\
{'name': 'sources',\
 'file': ['$PROJ_DIR$/../main.c', \
          '$PROJ_DIR$/../main.h']
}

EWP_FREERTOS =\
{
    'name': 'free-rtos',\
    'file': ['rtos/FreeRTOS/config/xxx/iar/FreeRTOSConfig.h',\
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
             'rtos/FreeRTOS/port/iar/port.c',\
             'rtos/FreeRTOS/port/iar/portasm.s',\
             'rtos/FreeRTOS/port/iar/portmacro.h',\
             'rtos/FreeRTOS/port/iar/portTicks.h',\
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

EWP_MQX =\
{
    'name': 'mqx',\
    'file': ['rtos/mqx/mqx/source/bsp/bsp.h',\
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

EWP_UCOSII =\
{
    'name': 'ucosii',\
    'file': ['rtos/uCOSII/src/config/app_hooks.c',\
             'rtos/uCOSII/src/uCOS-II/Source/os_core.c',\
             'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/IAR/os_cpu.h',\
             'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/IAR/os_cpu_a.asm', \
             'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/IAR/os_cpu_c.c', \
             'rtos/uCOSII/src/uCOS-II/Ports/ccc/Generic/IAR/os_dbg.c', \
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

EWP_UCOSIII =\
{
    'name': 'ucosiii',\
    'file': ['rtos/uCOSIII/src/uC-CPU/cpu_core.c',\
             'rtos/uCOSIII/src/uC-CPU/ccc/IAR/cpu_a.asm',\
             'rtos/uCOSIII/src/uC-CPU/ccc/IAR/cpu_c.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os.h',\
             'rtos/uCOSIII/src/config/os_app_hooks.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_cfg_app.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_core.c',\
             'rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/IAR/os_cpu.h',\
             'rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/IAR/os_cpu_a.asm',\
             'rtos/uCOSIII/src/uCOS-III/Ports/ccc/Generic/IAR/os_cpu_c.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_dbg.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_flag.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_int.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_mem.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_msg.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_mutex.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_pend_multi.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_prio.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_q.c',
             'rtos/uCOSIII/src/uCOS-III/Source/os_sem.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_stat.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_task.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_tick.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_time.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_tmr.c',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_type.h',\
             'rtos/uCOSIII/src/uCOS-III/Source/os_var.c']
}

EWW_BATCH_ALL =\
{
    'name': 'all',
    'member': [{'project': '', 'configuration': 'Release'},\
               {'project': '', 'configuration': 'Debug'}]
}

EWW_BATCH_DBG =\
{
    'name': 'Debug',
    'member': [{'project': '', 'configuration': 'Debug'}]
}

EWW_BATCH_RLS =\
{
    'name': 'Release',
    'member': [{'project': '', 'configuration': 'Release'}]
}

EWW_PROJECTS = {'path': []}

class KsdkIar(object):
    """ Class for generating IAR EWARM projects

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
        self.asmDefines = copy.deepcopy(ASMDEFINES)
        self.asmIncludes = copy.deepcopy(ASMINCLUDES)
        self.linkOut = copy.deepcopy(LINKOUT)
        self.linkIcf = copy.deepcopy(LINKICF)

        self.ewpStartup = copy.deepcopy(EWP_STARTUP)
        self.ewpUtilities = copy.deepcopy(EWP_UTILITIES)
        self.ewpBoard = copy.deepcopy(EWP_BOARD)
        self.ewpSources = copy.deepcopy(EWP_SOURCES)

        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.ewpRtos = copy.deepcopy(EWP_FREERTOS)
            elif ksdkProj.rtos == 'mqx':
                self.ewpRtos = copy.deepcopy(EWP_MQX)
            elif ksdkProj.rtos == 'ucosii':
                self.ewpRtos = copy.deepcopy(EWP_UCOSII)
            elif ksdkProj.rtos == 'ucosiii':
                self.ewpRtos = copy.deepcopy(EWP_UCOSIII)

        # Copy dictionaries for .eww batch buildss
        self.wsBatchAll = copy.deepcopy(EWW_BATCH_ALL)
        self.wsBatchDbg = copy.deepcopy(EWW_BATCH_DBG)
        self.wsBatchRls = copy.deepcopy(EWW_BATCH_RLS)

        # Copy project path dictionary
        self.projPaths = copy.deepcopy(EWW_PROJECTS)

        #self.parent = "C:\\Users\\b45635\\PGKSDK\\IAR"
        #self.name = 'Test'
        return

    def gen_ewp(self, ksdkProj):
        """ Generate the ewp files for IAR project

        :param ksdkProj: Instance of a KSDK project
        """

        iarPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/iar'
        if self.isLinked:
            self.projRelPath = '$PROJ_DIR$/' + kT.get_rel_path(iarPath, ksdkProj.sdkPath) + '/'
        else:
            self.projRelPath = '$PROJ_DIR$/../'

        # Populate ksdkProj specifics to dictionaries

        ## Set name of out file
        self.linkOut['state'] = self.name + '.out'

        ## Configure linker option
        self.linkIcf['state'] = self.projRelPath + 'platform/devices/' +\
                                ksdkProj.device[1] + '/linker/iar/' +\
                                ksdkProj.device[0] + '_flash.icf'

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
        self.cIncludes['state'].append("$PROJ_DIR$/../../..")

        if ksdkProj.useBSP:
            self.cIncludes['state'].append("$PROJ_DIR$/../board")

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
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/config/' + self.device[1][1:] + '/iar')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/port/iar')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/include')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/src')
                self.asmIncludes['state'].append(self.projRelPath + 'rtos/FreeRTOS/config/' + self.device[1][1:] + '/iar')
                #print self.asmIncludes
                #print self.asmIncludes['state']
                #print self.asmIncludes['state'][0]
            elif ksdkProj.rtos == 'mqx':
                archType = 'M4' if (self.device[4] == 'cm4') else 'M0'
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.iar/debug')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.iar/debug/config')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.iar/debug/mqx')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.iar/debug/mqx_stdlib')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/config/mcu/' + self.device[1])
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/config/board/' + ksdkProj.board[1])
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/bsp')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/mqx/mqx/source/psp/cortex_m/compiler/iar')
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
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uCOS-II/Ports/' + archType + '/Generic/IAR')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uC-CPU/' + archType + '/IAR')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/config')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uCOS-II/Source')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uC-CPU')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSII/src/uC-LIB')
            elif ksdkProj.rtos == 'ucosiii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uCOS-III/Ports/' + archType + '/Generic/IAR')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-CPU/' + archType + '/IAR')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/config')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uCOS-III/Source')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-CPU')
                self.cIncludes['state'].append(self.projRelPath + 'rtos/uCOSIII/src/uC-LIB')

        # Add relative paths to files
        index = 0
        while index < len(self.ewpStartup['file']):
            self.ewpStartup['file'][index] = kT.string_replace(self.ewpStartup['file'][index],\
                                                               'xxx', \
                                                               ksdkProj.device[1])
            self.ewpStartup['file'][index] = self.projRelPath + self.ewpStartup['file'][index]
            index += 1

        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                index = 0
                while index < len(self.ewpRtos['file']):
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'xxx',\
                                                ksdkProj.device[1][1:])
                    self.ewpRtos['file'][index] = self.projRelPath + self.ewpRtos['file'][index]
                    index += 1
            elif ksdkProj.rtos == 'mqx':
                index = 0
                while index < len(self.ewpRtos['file']):
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'xxx',\
                                                ksdkProj.device[1])
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'bbb',\
                                                ksdkProj.board[1])
                    self.ewpRtos['file'][index] = self.projRelPath + self.ewpRtos['file'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.ewpRtos['file']):
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'ccc',\
                                                archType)
                    self.ewpRtos['file'][index] = self.projRelPath + self.ewpRtos['file'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosiii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.ewpRtos['file']):
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'ccc',\
                                                archType)
                    self.ewpRtos['file'][index] = self.projRelPath + self.ewpRtos['file'][index]
                    index += 1

        kT.debug_log(self.ewpStartup['file'])

        if ksdkProj.libList[0] != 'hal':
            index = 0
            while index < len(self.ewpUtilities['file']):
                self.ewpUtilities['file'][index] = self.projRelPath + self.ewpUtilities['file'][index]
                index += 1

        self.linkLibs['state'][0] = self.projRelPath +  self.linkLibs['state'][0]
        self.linkLibs['state'][0] = kT.string_replace(self.linkLibs['state'][0], 
                                                      'xxx', ksdkProj.libList[0])
        if ksdkProj.rtos != 'bm':
            self.linkLibs['state'][0] = kT.string_replace(self.linkLibs['state'][0], \
                                        'libksdk_' + ksdkProj.libList[0] + '.a', \
                                        'libksdk_platform_' + ksdkProj.libList[0] + '.a')
        self.linkLibs['state'][0] = kT.string_replace(self.linkLibs['state'][0], 
                                                      'ddd', ksdkProj.device[1][1:])

        if ksdkProj.rtos == 'mqx':
            mqxLib = self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.iar/debug/mqx/lib_mqx.a'
            self.linkLibs['state'].append(mqxLib)
            mqxStdLib = self.projRelPath + 'rtos/mqx/lib/' + ksdkProj.board[1] + '.iar/debug/mqx_stdlib/lib_mqx_stdlib.a'
            self.linkLibs['state'].append(mqxStdLib)


        #    l = kT.string_replace(l, 'zzz', ksdkProj.rtos)
        #    kT.debug_log(l)
        #    if self.projType == 'usb':
        #        l = kT.string_replace(l, 'yyy', ksdkProj.board[1])
        #    b = l

        kT.debug_log(self.linkLibs['state'])

        # Configure linker stack and heap
        if self.projType == 'usb':
            if ksdkProj.rtos == 'bm':
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['state'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['state'][1] = '__stack_size__=0x1000'
            else:
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['state'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['state'][1] = '__stack_size__=0x1000'

        if ksdkProj.rtos == 'mqx':
            self.linkDefines['state'][0] = '__stack_size__=0x400'
            self.linkDefines['state'][1] = '__heap_size__=0x400'
            self.linkDefines['state'].append('__ram_vector_table__=1')
        elif ksdkProj.rtos == 'freertos':
            self.linkDefines['state'][0] = '__stack_size__=0x1000'
            self.linkDefines['state'][1] = '__heap_size__=0x1000'
            self.linkDefines['state'].append('__ram_vector_table__=1')
        elif ksdkProj.rtos == 'ucosii':
            self.linkDefines['state'][0] = '__stack_size__=0x1000'
            self.linkDefines['state'][1] = '__heap_size__=0x1000'
            self.linkDefines['state'].append('__ram_vector_table__=1')
        elif ksdkProj.rtos == 'ucosiii':
            self.linkDefines['state'][0] = '__stack_size__=0x1000'
            self.linkDefines['state'][1] = '__heap_size__=0x1000'
            self.linkDefines['state'].append('__ram_vector_table__=1')

        tree = ET.ElementTree(ET.fromstring(iF.iar_formatted_ewp))

        for elem in tree.iter(tag='option'):
            for child in elem.findall('name'):
                if child.text == 'OGChipSelectEditMenu':
                    projDev = ET.Element('state')
                    projDev.text = ksdkProj.device[0] + '\tFreescale ' + ksdkProj.device[0]
                    elem.append(projDev)
                if child.text == 'FPU':
                    projFPU = ET.Element('state')
                    projFPU.text = '5' if self.device[3] else '0'
                    elem.append(projFPU)
                if child.text == 'GFPUCoreSlave':
                    projFPU = ET.Element('state')
                    projFPU.text = '39' if self.device[3] else '35'
                    elem.append(projFPU)
                if child.text == 'GBECoreSlave':
                    projBE = ET.Element('state')
                    projBE.text = '39' if self.device[3] else '35'
                    elem.append(projBE)
                if child.text == 'CCDefines':
                    for d in self.cDefines['state']:
                        projCDef = ET.Element('state')
                        projCDef.text = d
                        elem.append(projCDef)
                if child.text == 'IlinkConfigDefines':
                    if ksdkProj.rtos != 'bm':
                        for d in self.linkDefines['state']:
                            projLDef = ET.Element('state')
                            projLDef.text = d
                            elem.append(projLDef)
                if child.text == 'IlinkOverrideProgramEntryLabel':
                    if ksdkProj.rtos == 'mqx':
                        for s in elem.findall('state'):
                            s.text = '1'
                            #print s.text
                if child.text == 'IlinkProgramEntryLabel':
                    if ksdkProj.rtos == 'mqx':
                        for s in elem.findall('state'):
                            s.text = 'Reset_Handler'
                            #print s.text
                if child.text == 'IlinkOutputFile':
                    projOut = ET.Element('state')
                    projOut.text = self.linkOut['state']
                    elem.append(projOut)
                if child.text == 'IlinkIcfFile':
                    projIcf = ET.Element('state')
                    projIcf.text = self.linkIcf['state']
                    elem.append(projIcf)
                if child.text == 'IlinkAdditionalLibs':
                    for l in self.linkLibs['state']:
                        projLib = ET.Element('state')
                        projLib.text = l
                        elem.append(projLib)
                if child.text == 'CCIncludePath2':
                    for i in self.cIncludes['state']:
                        projInc = ET.Element('state')
                        projInc.text = i
                        elem.append(projInc)
                if child.text == 'AUserIncludes':
                    #print "ASM Inlcudes"
                    if ksdkProj.rtos == 'freertos':
                        asmInc = ET.Element('state')
                        asmInc.text = self.asmIncludes['state'][0]
                        elem.append(asmInc)

        # Add file groups to ewp file
        root = tree.getroot()
        if ksdkProj.rtos != 'mqx':
            startGrp = ET.SubElement(root, 'group')
            startName = ET.SubElement(startGrp, 'name')
            startName.text = self.ewpStartup['name']
            for f in self.ewpStartup['file']:
                startFile = ET.SubElement(startGrp, 'file')
                startFName = ET.SubElement(startFile, 'name')
                startFName.text = f
        sourceGrp = ET.SubElement(root, 'group')
        sourceName = ET.SubElement(sourceGrp, 'name')
        sourceName.text = self.ewpSources['name']
        for f in self.ewpSources['file']:
            sourceFile = ET.SubElement(sourceGrp, 'file')
            sourceFName = ET.SubElement(sourceFile, 'name')
            sourceFName.text = f
        if ksdkProj.useBSP:
            boardGrp = ET.SubElement(root, 'group')
            boardName = ET.SubElement(boardGrp, 'name')
            boardName.text = self.ewpBoard['name']
            for f in self.ewpBoard['file']:
                boardFile = ET.SubElement(boardGrp, 'file')
                boardFName = ET.SubElement(boardFile, 'name')
                boardFName.text = f
        if ksdkProj.libList[0] != 'hal':
            utilsGrp = ET.SubElement(root, 'group')
            utilsName = ET.SubElement(utilsGrp, 'name')
            utilsName.text = self.ewpUtilities['name']
            for f in self.ewpUtilities['file']:
                utilsFile = ET.SubElement(utilsGrp, 'file')
                utilsFName = ET.SubElement(utilsFile, 'name')
                utilsFName.text = f
        if ksdkProj.rtos != 'bm':
            rtosGrp = ET.SubElement(root, 'group')
            rtosName = ET.SubElement(rtosGrp, 'name')
            rtosName.text = self.ewpRtos['name']
            for f in self.ewpRtos['file']:
                rtosFile = ET.SubElement(rtosGrp, 'file')
                rtosFName = ET.SubElement(rtosFile, 'name')
                rtosFName.text = f

        prettyRoot = kT.pretty_xml(root, "iso-8859-1")

        # Write data to file
        if not os.path.isdir(iarPath):
            os.makedirs(iarPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(iarPath + '/' + self.name + '.ewp', "iso-8859-1")

        # Gen ewd while we are here
        tree = ET.ElementTree(ET.fromstring(iF.iar_formatted_ewd))

        for elem in tree.iter(tag='option'):
            for child in elem.findall('name'):
                if child.text == 'OCDynDriverList':
                    for state in elem.findall('state'):
                        state.text = 'CMSISDAP_ID' if (self.device[4] == 'cm4') else 'PEMICRO_ID'
                if child.text == 'CMSISDAPResetList':
                    for state in elem.findall('state'):
                        state.text = '5' if (self.device[4] == 'cm4') else '10'
                if child.text == 'CMSISDAPInterfaceRadio':
                    for state in elem.findall('state'):
                        state.text = '1' if (self.device[4] == 'cm4') else '0'
                if child.text == 'CMSISDAPSelectedCPUBehaviour':
                    for state in elem.findall('state'):
                        state.text = '' if (self.device[4] == 'cm4') else '0'

        tree.write(iarPath + '/' + self.name + '.ewd', "iso-8859-1")

        return

    def gen_eww(self, ksdkProj):
        """ Generate the eww files for IAR project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        iarPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/iar'
        if self.isLinked:
            self.wsRelPath = '$WS_DIR$/' + kT.get_rel_path(iarPath, ksdkProj.sdkPath) + '/'
        else:
            self.wsRelPath = '$WS_DIR$/../'

        # Get project library names
        ## hal or platform library
        if ksdkProj.rtos == 'bm':
            sdkLibName = 'ksdk_' + ksdkProj.libList[0] + '_lib'
            sdkLibPath = 'lib/ksdk_' + ksdkProj.libList[0] + '_lib/iar/' + ksdkProj.device[1][1:] + '/ksdk_' + ksdkProj.libList[0] + '_lib'
        else:
            sdkLibName = 'ksdk_' + ksdkProj.rtos + '_lib'
            sdkLibPath = 'lib/ksdk_' + ksdkProj.rtos + '_lib/iar/' + ksdkProj.device[1][1:] + '/ksdk_' + ksdkProj.rtos + '_lib'

        if ksdkProj.rtos == 'mqx':
            mqxLibName = 'mqx_' + ksdkProj.board[1]
            mqxLibPath = 'rtos/mqx/mqx/build/iar/' + mqxLibName + '/' + mqxLibName + '.ewp'
            mqxStdLibName = 'mqx_stdlib_' + ksdkProj.board[1]
            mqxStdLibPath = 'rtos/mqx/mqx_stdlib/build/iar/' + mqxStdLibName + '/' + mqxStdLibName + '.ewp'

        # Populate dictionaries with ksdkProj info
        ## All
        self.wsBatchAll['member'][0]['project'] = self.name
        self.wsBatchAll['member'][1]['project'] = self.name
        self.wsBatchAll['member'].append({'project': sdkLibName, \
                                     'configuration': 'Release'})
        self.wsBatchAll['member'].append({'project': sdkLibName, \
                                     'configuration': 'Debug'})
        ## Release
        self.wsBatchRls['member'][0]['project'] = self.name
        self.wsBatchRls['member'].append({'project': sdkLibName, \
                                     'configuration': 'Release'})
        ## Debug
        self.wsBatchDbg['member'][0]['project'] = self.name
        self.wsBatchDbg['member'].append({'project': sdkLibName, \
                                     'configuration': 'Debug'})

        if ksdkProj.rtos == 'mqx':
            self.wsBatchAll['member'].append({'project': mqxLibName, \
                                              'configuration': 'Debug'})
            self.wsBatchAll['member'].append({'project': mqxLibName, \
                                              'configuration': 'Release'})
            self.wsBatchDbg['member'].append({'project': mqxLibName, \
                                              'configuration': 'Debug'})
            self.wsBatchRls['member'].append({'project': mqxLibName, \
                                              'configuration': 'Release'})
            self.wsBatchAll['member'].append({'project': mqxStdLibName, \
                                              'configuration': 'Debug'})
            self.wsBatchAll['member'].append({'project': mqxStdLibName, \
                                              'configuration': 'Release'})
            self.wsBatchDbg['member'].append({'project': mqxStdLibName, \
                                              'configuration': 'Debug'})
            self.wsBatchRls['member'].append({'project': mqxStdLibName, \
                                              'configuration': 'Release'})

        # Create tree
        tree = ET.ElementTree()

        # Set root
        root = ET.Element('workspace')

        # Create subelements for batch builds
        batch = ET.SubElement(root, 'batchBuild')

        ## All
        batchDefAll = ET.SubElement(batch, 'batchDefinition')
        batchName = ET.SubElement(batchDefAll, 'name')
        batchName.text = self.wsBatchAll['name']
        for m in self.wsBatchAll['member']:
            batchMember = ET.SubElement(batchDefAll, 'member')
            batchProj = ET.SubElement(batchMember, 'project')
            batchProj.text = m['project']
            batchConfig = ET.SubElement(batchMember, 'configuration')
            batchConfig.text = m['configuration']

        ## Release
        batchDefRls = ET.SubElement(batch, 'batchDefinition')
        batchName = ET.SubElement(batchDefRls, 'name')
        batchName.text = self.wsBatchRls['name']
        for m in self.wsBatchRls['member']:
            batchMember = ET.SubElement(batchDefRls, 'member')
            batchProj = ET.SubElement(batchMember, 'project')
            batchProj.text = m['project']
            batchConfig = ET.SubElement(batchMember, 'configuration')
            batchConfig.text = m['configuration']

        ## Debug
        batchDefDbg = ET.SubElement(batch, 'batchDefinition')
        batchName = ET.SubElement(batchDefDbg, 'name')
        batchName.text = self.wsBatchDbg['name']
        for m in self.wsBatchDbg['member']:
            batchMember = ET.SubElement(batchDefDbg, 'member')
            batchProj = ET.SubElement(batchMember, 'project')
            batchProj.text = m['project']
            batchConfig = ET.SubElement(batchMember, 'configuration')
            batchConfig.text = m['configuration']

        # Edit dictionary to add ksdkProj info
        self.projPaths['path'].append('$WS_DIR$/' + self.name + '.ewp')
        self.projPaths['path'].append(self.wsRelPath + sdkLibPath + '.ewp')

        if ksdkProj.rtos == 'mqx':
            self.projPaths['path'].append(self.wsRelPath + mqxLibPath)
            self.projPaths['path'].append(self.wsRelPath + mqxStdLibPath)

        # Populate project paths
        for p in self.projPaths['path']:
            proj = ET.SubElement(root, 'project')
            projPath = ET.SubElement(proj, 'path')
            projPath.text = p

        # Format data to make it more readable
        prettyRoot = kT.pretty_xml(root, "iso-8859-1")

        #print prettyRoot

        # Write data to file
        if not os.path.isdir(iarPath):
            os.mkdir(iarPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(iarPath + '/' + self.name + '.eww', "iso-8859-1")

        return
