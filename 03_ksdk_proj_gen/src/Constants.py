'''
Created on Jan 7, 2016

@author: B49736
'''

#Elements from KSDK manifest
API_TAG_ELEMENT = 'api'
KSDK_TAG_ELEMENT = 'ksdk'
COMPILER_TAG_NAME = 'compiler'
COMPILERS_TAG_NAME = 'compilers'
BOARD_TAG_NAME = 'board'
BOARDS_TAG_NAME = 'boards'
DEVICES_TAG_NAME = 'devices'
DEVICE_TAG_NAME = 'device'
COMPONENTS_TAG_NAME = 'components'
COMPONET_TAG_NAME = 'component'
TOOLCHAINS_TAG_NAME = 'toolchains'
TOOLCHAIN_TAG_NAME = 'toolchain'
TOOLS_TAG_NAME = 'tools'
TOOL_TAG_NAME = 'tool'

#Attributes from KSDK manifest
API_VERSION_ATR = 'version'
FOR_ATR = 'for'
ID_ATR = 'id'
DEVICE_FULL_NAME_ATR = 'full_name'

#rtos type
RTOS_NONE = 'bm'
RTOS_FREERTOS = 'freertos'
RTOS_UCOSII = 'ucosii'
RTOS_UCOSIII = 'ucosiii'


#Folder names
CMSIS_FOLDER = 'CMSIS'
SOURCES_FOLDER = 'sources'
DRIVERS_FOLDER = 'drivers'
UTILITIES_FOLDER = 'utilities'

DEFAULT_VERSION = "1.0"

ADV_HELP = "Choose to create a 'New' project or 'Clone' an existing one.\n" + \
           "\n" + \
           "New:\n" + \
           "\t- Select the options you wish to use for your project.\n" + \
           "\t- Some selections will restrict your options to prevent adding\n" + \
           "\t  incompatible components.\n" + \
           "\t- A toolchain must be selected in order for a project to be\n" + \
           "\t  generated.\n" + \
           "\n" + \
           "Clone:\n" + \
           "\t- Cloned projects will retain their original names. They will\n" + \
           "\t  be placed into '/board/{selectedBoard}/user_apps' if\n" + \
           "\t  the 'Generate standalone project' checkbox is not checked.\n" + \
           "\n" + \
           "Advanced Generate:\n" + \
           "\t- Will generate a project based solely on the configuration in\n" + \
           "\t  this window.\n"

#placeholder for project name
PROJECT_NAME_PLACEHOLDER = 'project_name'

BOARD_C = """/* This is a template for board specific configuration */

#include <stdint.h>
#include "board.h"


/* Initialize debug console. */
void BOARD_InitDebugConsole(void){
    /* This is a template function */
}
"""
BOARD_H = """ /* This is a template file for board configuration */

#ifndef _BOARD_H_
#define _BOARD_H_

/*******************************************************************************
 * Definitions
 ******************************************************************************/

/* The board name */
#define BOARD_NAME "###-not-specified-###"


/*******************************************************************************
 * API
 ******************************************************************************/

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/* Initialize debug console. */
void BOARD_InitDebugConsole(void);

#if defined(__cplusplus)
}
#endif /* __cplusplus */

#endif /* _BOARD_H_ */
"""

CLOCK_CONFIG_C = """/* This is a template for clock configuration */


/*******************************************************************************
 * Definitions
 ******************************************************************************/

/*******************************************************************************
 * Variables
 ******************************************************************************/

/*******************************************************************************
 * Code
 ******************************************************************************/
 
 void BOARD_BootClockRUN(void) {
    /* This is a template function */
 }
"""
 
CLOCK_CONFIG_H = """/* This is a template for clock configuration */

#ifndef _CLOCK_CONFIG_H_
#define _CLOCK_CONFIG_H_

/*******************************************************************************
 * DEFINITION
 ******************************************************************************/

/*******************************************************************************
 * API
 ******************************************************************************/

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

void BOARD_BootClockRUN(void);

#if defined(__cplusplus)
}
#endif /* __cplusplus */

#endif /* _CLOCK_CONFIG_H_ */
"""

PIN_MUX_C = """/* This is a template file for pins configuration */

#include "fsl_device_registers.h"

/*******************************************************************************
 * Code
 ******************************************************************************/
/*!
 * @brief Initialize all pins used in this example
 */
void BOARD_InitPins(void)
{
  /* This is a template function for pins configuration. Intentionally empty */
}
"""

PIN_MUX_H = """/* This is a template file for pins configuration */

#ifndef _PIN_MUX_H_
#define _PIN_MUX_H_

#include <stdbool.h>

/*******************************************************************************
 * API
 ******************************************************************************/

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus*/

/*!
 * @brief Initialize all pins used in this example
 */
void BOARD_InitPins(void);

#if defined(__cplusplus)
}
#endif /* __cplusplus*/

#endif /* _PIN_MUX_H_  */
"""

QUICK_MAIN_C = """/*
 * Copyright (c) 2013 - 2015, Freescale Semiconductor, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of Freescale Semiconductor, Inc. nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */


#include <stdio.h>
#include "main.h"

int main(void) {
  
  BOARD_InitPins(); 
  BOARD_BootClockRUN();
  BOARD_InitDebugConsole();
  
  PRINTF("project_name project\\n");
    
  for(;;) { /* Infinite loop to avoid leaving the main function */
    __asm("NOP"); /* something to use as a breakpoint stop while looping */
  }
}
"""

ADVANCED_MAIN_C = """/*
 * Copyright (c) 2013 - 2015, Freescale Semiconductor, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of Freescale Semiconductor, Inc. nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */


#include "fsl_device_registers.h"
#include "fsl_debug_console.h"
#include "board.h"
#include "pin_mux.h"
#include "clock_config.h"

int main(void) {
  
  BOARD_InitPins(); 
  BOARD_BootClockRUN();
  BOARD_InitDebugConsole();
  
  PRINTF("project_name project\\n");

  for(;;) { /* Infinite loop to avoid leaving the main function */
    __asm("NOP"); /* something to use as a breakpoint stop while looping */
  }
}
"""
DRIVERS_PLACE_HOLDER = '<drivers>'

QUICK_MAIN_H = """/*
 * Copyright (c) 2013 - 2015, Freescale Semiconductor, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of Freescale Semiconductor, Inc. nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

<drivers> 
#include "fsl_device_registers.h"
#include "board.h"
#include "pin_mux.h"
#include "clock_config.h"
"""
 
MAIN_FREERTOS_C = """/*
 * Copyright (c) 2013 - 2015, Freescale Semiconductor, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of Freescale Semiconductor, Inc. nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * This is template for main module created by New Kinetis SDK 2.x Project Wizard. Enjoy!
 **/

#include "board.h"
#include "pin_mux.h"
#include "clock_config.h"
#include "fsl_debug_console.h"

/* FreeRTOS kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "timers.h"


/* Task priorities. */
#define hello_task_PRIORITY (configMAX_PRIORITIES - 1)

/*!
 * @brief Task responsible for printing of "Hello world." message.
 */
static void hello_task(void *pvParameters) {
  for (;;) {
    PRINTF("Hello world.\\r\\n");
    vTaskSuspend(NULL);
  }
}

/*!
 * @brief Application entry point.
 */
int main(void) {
  /* Init board hardware. */
  BOARD_InitPins();
  BOARD_BootClockRUN();
  BOARD_InitDebugConsole();

  /* Create RTOS task */
  xTaskCreate(hello_task, "Hello_task", configMINIMAL_STACK_SIZE, NULL, hello_task_PRIORITY, NULL);
  vTaskStartScheduler();

  /* Add your code here */

  for(;;) { /* Infinite loop to avoid leaving the main function */
    __asm("NOP"); /* something to use as a breakpoint stop while looping */
  }
}
"""

MAIN_UCOSII_C = """/*
 * Copyright (c) 2013 - 2015, Freescale Semiconductor, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of Freescale Semiconductor, Inc. nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * This is template for main module created by New Kinetis SDK 2.x Project Wizard. Enjoy!
 **/

#include "board.h"
#include "pin_mux.h"
#include "clock_config.h"
#include "fsl_debug_console.h"

/* Kernel includes. */
#include "ucos_ii.h"

#define STACK_SIZE 512

OS_STK stack_hello[STACK_SIZE];

/*!
 * @brief Task responsible for printing of "Hello world." message.
 */
void hello_task(void *p_arg) {
  INT8U err;
  for (;;) {
    PRINTF("Hello world.\\r\\n");
    err = OSTaskSuspend(OS_PRIO_SELF);
    if (err != OS_ERR_NONE) {
      PRINTF("Error.");
    }
  }
}

/*!
 * @brief Application entry point.
 */
int main(void) {
  /* Init board hardware. */
  BOARD_InitPins();
  BOARD_BootClockRUN();
  BOARD_InitDebugConsole();

  OSInit();
  OSTaskCreate(hello_task,                   /* Task function */
               NULL,                         /* Creation parameter */
               &stack_hello[STACK_SIZE - 1], /* Stack address */
               5);                           /* Task priority */

  OSStart();

  /* Add your code here */

  for(;;) { /* Infinite loop to avoid leaving the main function */
    __asm("NOP"); /* something to use as a breakpoint stop while looping */
  }
}
"""

MAIN_UCOSIII_C = """/*
 * Copyright (c) 2013 - 2015, Freescale Semiconductor, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of Freescale Semiconductor, Inc. nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * This is template for main module created by New Kinetis SDK 2.x Project Wizard. Enjoy!
 **/

#include "board.h"
#include "pin_mux.h"
#include "clock_config.h"
#include "fsl_debug_console.h"

/* Kernel includes. */
#include "os.h"

#define STACK_SIZE 512

CPU_STK stack_hello[STACK_SIZE];
OS_TCB tcb_hello;

/*!
 * @brief Task responsible for printing of "Hello world." message.
 */
void hello_task(void *p_arg) {
  OS_ERR err;
  for (;;) {
    PRINTF("Hello world.\\r\\n");
    OSTaskSuspend(NULL, &err);
    if (err != OS_ERR_NONE) {
      PRINTF("Error.");
    }
  }
}

/*!
 * @brief Application entry point.
 */
int main(void) {
  OS_ERR err;

  /* Init board hardware. */
  BOARD_InitPins();
  BOARD_BootClockRUN();
  BOARD_InitDebugConsole();

  OSInit(&err);
  OSTaskCreate(&tcb_hello,   /* Task control block pointer. */
               "hello_task", /* Task name. */
               hello_task,   /* Task function pointer. */
               NULL,         /* Task creation parameter. */
               5,            /* Task priority. */
               stack_hello,  /* Task stack base address. */
               0,            /* Task stack limit address. */
               STACK_SIZE,   /* Task stack size. */
               0,            /* Maximum number of messages that can be sent to the task.  */
               0,            /* Time slice. */
               NULL,         /* Pointer to TCB extension. */
               0,            /* Additional options. */
               &err);        /* Error code. */

  OSStart(&err);

  /* Add your code here */

  for(;;) { /* Infinite loop to avoid leaving the main function */
    __asm("NOP"); /* something to use as a breakpoint stop while looping */
  }
}
"""

FREERTOS_CONFIG_H="""
/*
    FreeRTOS V8.2.3 - Copyright (C) 2015 Real Time Engineers Ltd.
    All rights reserved

    VISIT http://www.FreeRTOS.org TO ENSURE YOU ARE USING THE LATEST VERSION.

    This file is part of the FreeRTOS distribution.

    FreeRTOS is free software; you can redistribute it and/or modify it under
    the terms of the GNU General Public License (version 2) as published by the
    Free Software Foundation >>>> AND MODIFIED BY <<<< the FreeRTOS exception.

    ***************************************************************************
    >>!   NOTE: The modification to the GPL is included to allow you to     !<<
    >>!   distribute a combined work that includes FreeRTOS without being   !<<
    >>!   obliged to provide the source code for proprietary components     !<<
    >>!   outside of the FreeRTOS kernel.                                   !<<
    ***************************************************************************

    FreeRTOS is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  Full license text is available on the following
    link: http://www.freertos.org/a00114.html

    ***************************************************************************
     *                                                                       *
     *    FreeRTOS provides completely free yet professionally developed,    *
     *    robust, strictly quality controlled, supported, and cross          *
     *    platform software that is more than just the market leader, it     *
     *    is the industry's de facto standard.                               *
     *                                                                       *
     *    Help yourself get started quickly while simultaneously helping     *
     *    to support the FreeRTOS project by purchasing a FreeRTOS           *
     *    tutorial book, reference manual, or both:                          *
     *    http://www.FreeRTOS.org/Documentation                              *
     *                                                                       *
    ***************************************************************************

    http://www.FreeRTOS.org/FAQHelp.html - Having a problem?  Start by reading
    the FAQ page "My application does not run, what could be wrong?".  Have you
    defined configASSERT()?

    http://www.FreeRTOS.org/support - In return for receiving this top quality
    embedded software for free we request you assist our global community by
    participating in the support forum.

    http://www.FreeRTOS.org/training - Investing in training allows your team to
    be as productive as possible as early as possible.  Now you can receive
    FreeRTOS training directly from Richard Barry, CEO of Real Time Engineers
    Ltd, and the world's leading authority on the world's leading RTOS.

    http://www.FreeRTOS.org/plus - A selection of FreeRTOS ecosystem products,
    including FreeRTOS+Trace - an indispensable productivity tool, a DOS
    compatible FAT file system, and our tiny thread aware UDP/IP stack.

    http://www.FreeRTOS.org/labs - Where new FreeRTOS products go to incubate.
    Come and try FreeRTOS+TCP, our new open source TCP/IP stack for FreeRTOS.

    http://www.OpenRTOS.com - Real Time Engineers ltd. license FreeRTOS to High
    Integrity Systems ltd. to sell under the OpenRTOS brand.  Low cost OpenRTOS
    licenses offer ticketed support, indemnification and commercial middleware.

    http://www.SafeRTOS.com - High Integrity Systems also provide a safety
    engineered and independently SIL3 certified version for use in safety and
    mission critical applications that require provable dependability.

    1 tab == 4 spaces!
*/

#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/*-----------------------------------------------------------
 * Application specific definitions.
 *
 * These definitions should be adjusted for your particular hardware and
 * application requirements.
 *
 * THESE PARAMETERS ARE DESCRIBED WITHIN THE 'CONFIGURATION' SECTION OF THE
 * FreeRTOS API DOCUMENTATION AVAILABLE ON THE FreeRTOS.org WEB SITE.
 *
 * See http://www.freertos.org/a00110.html.
 *----------------------------------------------------------*/

#define configUSE_PREEMPTION 1
#define configUSE_IDLE_HOOK 0
#define configUSE_TICK_HOOK 0
#define configCPU_CLOCK_HZ (SystemCoreClock)
#define configTICK_RATE_HZ ((TickType_t)1000)
#define configMAX_PRIORITIES (5)
#define configMINIMAL_STACK_SIZE ((unsigned short)90)
#define configTOTAL_HEAP_SIZE ((size_t)(10 * 1024))
#define configMAX_TASK_NAME_LEN (10)
#define configUSE_TRACE_FACILITY 1
#define configUSE_16_BIT_TICKS 0
#define configIDLE_SHOULD_YIELD 1
#define configUSE_MUTEXES 1
#define configQUEUE_REGISTRY_SIZE 8
#define configCHECK_FOR_STACK_OVERFLOW 0
#define configUSE_RECURSIVE_MUTEXES 1
#define configUSE_MALLOC_FAILED_HOOK 0
#define configUSE_APPLICATION_TASK_TAG 0
#define configUSE_COUNTING_SEMAPHORES 1
#define configGENERATE_RUN_TIME_STATS 0
#define configUSE_TIME_SLICING 0
#define INCLUDE_xTimerPendFunctionCall 1
#define INCLUDE_xEventGroupSetBitFromISR 1

/* Co-routine definitions. */
#define configUSE_CO_ROUTINES 0
#define configMAX_CO_ROUTINE_PRIORITIES (2)

/* Software timer definitions. */
#define configUSE_TIMERS 1
#define configTIMER_TASK_PRIORITY (2)
#define configTIMER_QUEUE_LENGTH 10
#define configTIMER_TASK_STACK_DEPTH (configMINIMAL_STACK_SIZE * 2)

/* Set the following definitions to 1 to include the API function, or zero
to exclude the API function. */
#define INCLUDE_vTaskPrioritySet 1
#define INCLUDE_uxTaskPriorityGet 1
#define INCLUDE_vTaskDelete 1
#define INCLUDE_vTaskCleanUpResources 1
#define INCLUDE_vTaskSuspend 1
#define INCLUDE_vTaskDelayUntil 1
#define INCLUDE_vTaskDelay 1

/* Cortex-M specific definitions. */
#ifdef __NVIC_PRIO_BITS
/* __BVIC_PRIO_BITS will be specified when CMSIS is being used. */
#define configPRIO_BITS __NVIC_PRIO_BITS
#else
#define configPRIO_BITS 4 /* 15 priority levels */
#endif

/* The lowest interrupt priority that can be used in a call to a "set priority"
function. */
#define configLIBRARY_LOWEST_INTERRUPT_PRIORITY 0xf

/* The highest interrupt priority that can be used by any interrupt service
routine that makes calls to interrupt safe FreeRTOS API functions.  DO NOT CALL
INTERRUPT SAFE FREERTOS API FUNCTIONS FROM ANY INTERRUPT THAT HAS A HIGHER
PRIORITY THAN THIS! (higher priorities are lower numeric values. */
#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY 5

/* Interrupt priorities used by the kernel port layer itself.  These are generic
to all Cortex-M ports, and do not rely on any particular library functions. */
#define configKERNEL_INTERRUPT_PRIORITY (configLIBRARY_LOWEST_INTERRUPT_PRIORITY << (8 - configPRIO_BITS))
/* !!!! configMAX_SYSCALL_INTERRUPT_PRIORITY must not be set to zero !!!!
See http://www.FreeRTOS.org/RTOS-Cortex-M3-M4.html. */
#define configMAX_SYSCALL_INTERRUPT_PRIORITY (configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY << (8 - configPRIO_BITS))

/* Normal assert() semantics without relying on the provision of an assert.h
header file. */
#define configASSERT(x)           \
    if ((x) == 0)                 \
    {                             \
        taskDISABLE_INTERRUPTS(); \
        for (;;)                  \
            ;                     \
    }

/* Definitions that map the FreeRTOS port interrupt handlers to their CMSIS
standard names. */
#define vPortSVCHandler SVC_Handler
#define xPortPendSVHandler PendSV_Handler
#define xPortSysTickHandler SysTick_Handler

#endif /* FREERTOS_CONFIG_H */
"""

UCOSIII_OS_CFG_H="""
/*
************************************************************************************************************************
*                                                      uC/OS-III
*                                                 The Real-Time Kernel
*
*                                  (c) Copyright 2009-2015; Micrium, Inc.; Weston, FL
*                           All rights reserved.  Protected by international copyright laws.
*
*                                                  CONFIGURATION FILE
*
* File    : OS_CFG.H
* By      : JJL
* Version : V3.05.01
*
* LICENSING TERMS:
* ---------------
*           uC/OS-III is provided in source form for FREE short-term evaluation, for educational use or
*           for peaceful research.  If you plan or intend to use uC/OS-III in a commercial application/
*           product then, you need to contact Micrium to properly license uC/OS-III for its use in your
*           application/product.   We provide ALL the source code for your convenience and to help you
*           experience uC/OS-III.  The fact that the source is provided does NOT mean that you can use
*           it commercially without paying a licensing fee.
*
*           Knowledge of the source code may NOT be used to develop a similar product.
*
*           Please help us continue to provide the embedded community with the finest software available.
*           Your honesty is greatly appreciated.
*
*           You can find our product's user manual, API reference, release notes and
*           more information at https://doc.micrium.com.
*           You can contact us at www.micrium.com.
************************************************************************************************************************
*/

#ifndef OS_CFG_H
#define OS_CFG_H

/* --------------------------- MISCELLANEOUS --------------------------- */
#define OS_CFG_APP_HOOKS_EN DEF_DISABLED /* Enable (DEF_ENABLED) application specific hooks                       */
#define OS_CFG_ARG_CHK_EN DEF_ENABLED    /* Enable (DEF_ENABLED) argument checking                                */
#define OS_CFG_CALLED_FROM_ISR_CHK_EN \
    DEF_ENABLED                         /* Enable (DEF_ENABLED) check for called from ISR                        */
#define OS_CFG_DBG_EN DEF_ENABLED       /* Enable (DEF_ENABLED) debug code/variables                             */
#define OS_CFG_DYN_TICK_EN DEF_DISABLED /* Enable (DEF_ENABLED) the Dynamic Tick                                 */
#define OS_CFG_INVALID_OS_CALLS_CHK_EN \
    DEF_DISABLED /* Enable (DEF_ENABLED) checks for invalid kernel calls                  */
#define OS_CFG_ISR_POST_DEFERRED_EN \
    DEF_DISABLED                            /* DEPRECATED Feature: Enable (DEF_ENABLED) deferred ISR posts           */
#define OS_CFG_OBJ_TYPE_CHK_EN DEF_DISABLED /* Enable (DEF_ENABLED) object type checking */
#define OS_CFG_TS_EN DEF_DISABLED           /* Enable (DEF_ENABLED) time stamping                                    */

#define OS_CFG_PEND_MULTI_EN DEF_DISABLED /* DEPRECATED Feature: Enable (DEF_ENABLED) multi-pend feature           */

#define OS_CFG_PRIO_MAX 32u /* Defines the maximum number of task priorities (see OS_PRIO data type) */

#define OS_CFG_SCHED_LOCK_TIME_MEAS_EN \
    DEF_DISABLED /* Include (DEF_ENABLED) code to measure scheduler lock time             */
#define OS_CFG_SCHED_ROUND_ROBIN_EN \
    DEF_DISABLED /* Include (DEF_ENABLED) code for Round-Robin scheduling                 */

#define OS_CFG_STK_SIZE_MIN 64u /* Minimum allowable task stack size                                     */

/* --------------------------- EVENT FLAGS ----------------------------- */
#define OS_CFG_FLAG_EN DEF_ENABLED           /* Enable (DEF_ENABLED) code generation for EVENT FLAGS                  */
#define OS_CFG_FLAG_DEL_EN DEF_ENABLED       /*     Include (DEF_ENABLED) code for OSFlagDel()                        */
#define OS_CFG_FLAG_MODE_CLR_EN DEF_DISABLED /*     Include (DEF_ENABLED) code for Wait on Clear EVENT FLAGS */
#define OS_CFG_FLAG_PEND_ABORT_EN \
    DEF_DISABLED /*     Include (DEF_ENABLED) code for OSFlagPendAbort()                  */

/* ------------------------ MEMORY MANAGEMENT -------------------------  */
#define OS_CFG_MEM_EN DEF_ENABLED /* Enable (DEF_ENABLED) code generation for the MEMORY MANAGER           */

/* ------------------- MUTUAL EXCLUSION SEMAPHORES --------------------  */
#define OS_CFG_MUTEX_EN DEF_ENABLED      /* Enable (DEF_ENABLED) code generation for MUTEX                        */
#define OS_CFG_MUTEX_DEL_EN DEF_DISABLED /*     Include (DEF_ENABLED) code for OSMutexDel()                       */
#define OS_CFG_MUTEX_PEND_ABORT_EN \
    DEF_DISABLED /*     Include (DEF_ENABLED) code for OSMutexPendAbort()                 */

/* -------------------------- MESSAGE QUEUES --------------------------  */
#define OS_CFG_Q_EN DEF_ENABLED            /* Enable (DEF_ENABLED) code generation for QUEUES                       */
#define OS_CFG_Q_DEL_EN DEF_DISABLED       /*     Include (DEF_ENABLED) code for OSQDel()                           */
#define OS_CFG_Q_FLUSH_EN DEF_DISABLED     /*     Include (DEF_ENABLED) code for OSQFlush()                         */
#define OS_CFG_Q_PEND_ABORT_EN DEF_ENABLED /*     Include (DEF_ENABLED) code for OSQPendAbort()                     */

/* ---------------------------- SEMAPHORES ----------------------------- */
#define OS_CFG_SEM_EN DEF_ENABLED            /* Enable (DEF_ENABLED) code generation for SEMAPHORES                   */
#define OS_CFG_SEM_DEL_EN DEF_ENABLED        /*     Include (DEF_ENABLED) code for OSSemDel()                         */
#define OS_CFG_SEM_PEND_ABORT_EN DEF_ENABLED /*     Include (DEF_ENABLED) code for OSSemPendAbort() */
#define OS_CFG_SEM_SET_EN DEF_ENABLED        /*     Include (DEF_ENABLED) code for OSSemSet()                         */

/* ----------------------------- MONITORS ------------------------------ */
#define OS_CFG_MON_EN DEF_ENABLED      /* Enable (DEF_ENABLED) code generation for MONITORS                     */
#define OS_CFG_MON_DEL_EN DEF_DISABLED /*     Include (DEF_ENABLED) code for OSMonDel()                         */

/* -------------------------- TASK MANAGEMENT -------------------------- */
#define OS_CFG_STAT_TASK_EN DEF_ENABLED /* Enable (DEF_ENABLED) the statistics task                              */
#define OS_CFG_STAT_TASK_STK_CHK_EN \
    DEF_ENABLED /*     Check task stacks (DEF_ENABLED) from the statistic task           */

#define OS_CFG_TASK_CHANGE_PRIO_EN \
    DEF_ENABLED                            /* Include (DEF_ENABLED) code for OSTaskChangePrio()                     */
#define OS_CFG_TASK_DEL_EN DEF_DISABLED    /* Include (DEF_ENABLED) code for OSTaskDel()                            */
#define OS_CFG_TASK_IDLE_EN DEF_ENABLED    /* Include (DEF_ENABLED) the idle task                                   */
#define OS_CFG_TASK_PROFILE_EN DEF_ENABLED /* Include (DEF_ENABLED) variables in OS_TCB for profiling               */
#define OS_CFG_TASK_Q_EN DEF_ENABLED       /* Include (DEF_ENABLED) code for OSTaskQXXXX()                          */
#define OS_CFG_TASK_Q_PEND_ABORT_EN \
    DEF_DISABLED                    /* Include (DEF_ENABLED) code for OSTaskQPendAbort()                     */
#define OS_CFG_TASK_REG_TBL_SIZE 1u /* Number of task specific registers                                     */
#define OS_CFG_TASK_STK_REDZONE_EN \
    DEF_DISABLED                         /* Enable (DEF_ENABLED) stack redzone                                    */
#define OS_CFG_TASK_STK_REDZONE_DEPTH 8u /*     Depth of the stack redzone                                        */
#define OS_CFG_TASK_SEM_PEND_ABORT_EN \
    DEF_ENABLED                            /* Include (DEF_ENABLED) code for OSTaskSemPendAbort()                   */
#define OS_CFG_TASK_SUSPEND_EN DEF_ENABLED /* Include (DEF_ENABLED) code for OSTaskSuspend() and OSTaskResume()     */
#define OS_CFG_TASK_TICK_EN DEF_ENABLED    /* Include (DEF_ENABLED) the kernel tick task                            */

/* ------------------ TASK LOCAL STORAGE MANAGEMENT -------------------  */
#define OS_CFG_TLS_TBL_SIZE 0u /* Include (DEF_ENABLED) code for Task Local Storage (TLS) registers     */

/* ------------------------- TIME MANAGEMENT --------------------------  */
#define OS_CFG_TIME_DLY_HMSM_EN DEF_ENABLED /* Include (DEF_ENABLED) code for OSTimeDlyHMSM() */
#define OS_CFG_TIME_DLY_RESUME_EN \
    DEF_DISABLED /* Include (DEF_ENABLED) code for OSTimeDlyResume()                      */

/* ------------------------- TIMER MANAGEMENT -------------------------- */
#define OS_CFG_TMR_EN DEF_ENABLED      /* Enable (DEF_ENABLED) code generation for TIMERS                       */
#define OS_CFG_TMR_DEL_EN DEF_DISABLED /* Enable (DEF_ENABLED) code generation for OSTmrDel()                   */

/* uC/TRACE                                                              */
#define TRACE_CFG_EN DEF_DISABLED /* Enable (DEF_ENABLED) uC/Trace instrumentation                         */

#endif
"""
