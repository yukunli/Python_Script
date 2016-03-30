"""
File:  atlFiles.py
==================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Dictionary of image files**

.. codeauthor:: B45635<getpass.getuser()@freescale.com>

.. sectionauthor:: B45635<getpass.getuser()@freescale.com>

.. versionadded:: 0.0.6

"""

com_atollic_truestudio_debug_hardware_device_prefs = \
"""BOARD=None
CODE_LOCATION=FLASH
ENDIAN=Little-endian
MCU=settingDevice
MCU_VENDOR=Freescale
MODEL=Pro
PROJECT_FORMAT_VERSION=2
TARGET=ARM\u00AE
VERSION=5.1.1
eclipse.preferences.version=1
"""

formatted_cproject = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?fileVersion 4.0.0?>
<cproject storage_type_id="org.eclipse.cdt.core.XmlProjectDescriptionStorage">
    <storageModule moduleId="org.eclipse.cdt.core.settings">
        <cconfiguration id="com.atollic.truestudio.exe.debug.1332848918">
            <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="com.atollic.truestudio.exe.debug.1332848918" moduleId="org.eclipse.cdt.core.settings" name="debug">
                <externalSettings/>
                <extensions>
                    <extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.ELF" point="org.eclipse.cdt.core.BinaryParser"/>
                </extensions>
            </storageModule>
            <storageModule moduleId="cdtBuildSystem" version="4.0.0">
                <configuration artifactExtension="elf" artifactName="${ProjName}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exe" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exe" cleanCommand="rm -rf" description="" id="com.atollic.truestudio.exe.debug.1332848918" name="debug" parent="com.atollic.truestudio.exe.debug">
                    <folderInfo id="com.atollic.truestudio.exe.debug.1332848918." name="/" resourcePath="">
                        <toolChain id="com.atollic.truestudio.exe.debug.toolchain.837293693" name="Atollic ARM Tools" superClass="com.atollic.truestudio.exe.debug.toolchain">
                            <targetPlatform archList="all" binaryParser="org.eclipse.cdt.core.ELF" id="com.atollic.truestudio.exe.debug.toolchain.platform.1111249909" isAbstract="false" name="debug platform" superClass="com.atollic.truestudio.exe.debug.toolchain.platform"/>
                            <builder buildPath="${workspace_loc:/TWR-K40/debug}" customBuilderProperties="toolChainpathType=1|toolChainpathString=C:/Freescale/TrueSTUDIO for ARM Pro 5.1.1/ARMTools/bin|" id="com.atollic.truestudio.mbs.builder1.808522275" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="CDT Internal Builder" superClass="com.atollic.truestudio.mbs.builder1">
                                <outputEntries>
                                    <entry flags="VALUE_WORKSPACE_PATH|RESOLVED" kind="outputPath" name="debug"/>
                                    <entry flags="VALUE_WORKSPACE_PATH|RESOLVED" kind="outputPath" name="release"/>
                                </outputEntries>
                            </builder>
                            <tool id="com.atollic.truestudio.exe.debug.toolchain.as.248597907" name="Assembler" superClass="com.atollic.truestudio.exe.debug.toolchain.as">
                                <option id="com.atollic.truestudio.common_options.target.endianess.1261678008" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess" value="com.atollic.truestudio.common_options.target.endianess.little" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.1032230591" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.1028189096" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.1176373879" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.as.symbols.defined.1040709735" name="Defined symbols" superClass="com.atollic.truestudio.as.symbols.defined" valueType="definedSymbols">
                                    <listOptionValue builtIn="false" value="DEBUG"/>
                                    <listOptionValue builtIn="false" value="__START=main"/>
                                    <listOptionValue builtIn="false" value="__ATOLLIC__"/>
                                </option>
                                <option id="com.atollic.truestudio.as.general.incpath.242031498" name="Include path" superClass="com.atollic.truestudio.as.general.incpath" valueType="includePath">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.1137199777" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                                <inputType id="com.atollic.truestudio.as.input.1393747936" name="Input" superClass="com.atollic.truestudio.as.input"/>
                                <option id="com.atollic.truestudio.as.general.warnings.6695407371" superClass="com.atollic.truestudio.as.general.warnings" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.as.general.version.4320870621" superClass="com.atollic.truestudio.as.general.version" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.as.general.preprocess.7318362338" superClass="com.atollic.truestudio.as.general.preprocess" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.exe.debug.toolchain.as.debug.flags.1339008301" superClass="com.atollic.truestudio.exe.debug.toolchain.as.debug.flags" valueType="enumerated" name="Debug Level" value="com.atollic.truestudio.as.debug.flags.2"/>
                                <option id="com.atollic.truestudio.as.general.otherflags.8525048051" superClass="com.atollic.truestudio.as.general.otherflags" valueType="string" value=" -mcpu=cortex-m4 "/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.debug.toolchain.gcc.157216120" name="C Compiler" superClass="com.atollic.truestudio.exe.debug.toolchain.gcc">
                                <option id="com.atollic.truestudio.gcc.symbols.defined.1911392732" name="Defined symbols" superClass="com.atollic.truestudio.gcc.symbols.defined" valueType="definedSymbols">
                                    <listOptionValue builtIn="false" value="DEBUG"/>
                                    <listOptionValue builtIn="false" value="ATOLLIC"/>
                                </option>
                                <option id="com.atollic.truestudio.gcc.directories.select.1212414964" name="Include path" superClass="com.atollic.truestudio.gcc.directories.select">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.endianess.1111924591" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess" value="com.atollic.truestudio.common_options.target.endianess.little" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.1558174321" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.441908344" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.972718727" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.gcc.optimization.prep_garbage.401161765" name="Prepare dead code removal " superClass="com.atollic.truestudio.gcc.optimization.prep_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.gcc.optimization.prep_data.276687480" name="Prepare dead data removal" superClass="com.atollic.truestudio.gcc.optimization.prep_data" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.gcc.misc.otherflags.2102010282" name="Other options" superClass="com.atollic.truestudio.gcc.misc.otherflags" value=" -mcpu=cortex-m4 " valueType="string"/>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.570712226" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                                <inputType id="com.atollic.truestudio.gcc.input.1331079379" superClass="com.atollic.truestudio.gcc.input"/>
                                <option id="com.atollic.truestudio.common_options.target.interwork.1017054618" superClass="com.atollic.truestudio.common_options.target.interwork" valueType="boolean" name="Mix ARM/Thumb" value="false"/>
                                <option id="com.atollic.truestudio.gcc.misc.longcalls.4948408544" superClass="com.atollic.truestudio.gcc.misc.longcalls" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.gcc.cstandard.9650378441" superClass="com.atollic.truestudio.gcc.cstandard" valueType="enumerated" name="C standard" value="com.atollic.truestudio.gcc.cstandard.gnu99"/>
                                <option id="com.atollic.truestudio.exe.debug.toolchain.gcc.optimization.level.9071299810" superClass="com.atollic.truestudio.exe.debug.toolchain.gcc.optimization.level" valueType="enumerated" value="com.atollic.truestudio.gcc.optimization.level.0"/>
                                <option id="com.atollic.truestudio.gcc.optimization.no_strict_aliasing.317309142" superClass="com.atollic.truestudio.gcc.optimization.no_strict_aliasing" valueType="boolean" name="No strict aliasing" value="false"/>
                                <option id="com.atollic.truestudio.exe.debug.toolchain.gcc.debug.info.9979355478" superClass="com.atollic.truestudio.exe.debug.toolchain.gcc.debug.info" valueType="enumerated" name="Debug Level" value="com.atollic.truestudio.gcc.debug.info.2"/>
                                <option id=" com.atollic.truestudio.gcc.misc.stackusage.4741512840" superClass=" com.atollic.truestudio.gcc.misc.stackusage" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.all.5883900166" superClass="com.atollic.truestudio.gcc.warnings.all" valueType="boolean" value="true"/>
                                <option id="com.atollic.truestudio.gcc.warnings.extra.5163439328" superClass="com.atollic.truestudio.gcc.warnings.extra" valueType="boolean" name="Enable extra warning flags" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.fatal.6047779321" superClass="com.atollic.truestudio.gcc.warnings.fatal" valueType="boolean" name="Abort compilation on first error" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.pedantic.9434632405" superClass="com.atollic.truestudio.gcc.warnings.pedantic" valueType="boolean" name="Issue all warnings demanded by strict ISO C and ISO C++" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.pedanticerrors.2355620623" superClass="com.atollic.truestudio.gcc.warnings.pedanticerrors" valueType="boolean" name="Generate error instead of warnings from strict ISO C and C++" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.missing_include_dirs.4768118685" superClass="com.atollic.truestudio.gcc.warnings.missing_include_dirs" valueType="boolean" name="Warn if a user-supplied include directory does not exist" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.w_switch_default.4048373092" superClass="com.atollic.truestudio.gcc.warnings.w_switch_default" valueType="boolean" name="Warn when switch statement does not have a default case" value="false"/>
                                <option id=" com.atollic.truestudio.gcc.warnings.w_switch_enum.8440240159" superClass=" com.atollic.truestudio.gcc.warnings.w_switch_enum" valueType="boolean" name="Warn if switch is used on enum type and switch statement lacks case for some enumerations" value="false"/>
                            </tool>
                            <tool commandLinePattern="${COMMAND} -Wl,--start-group ${INPUTS} -Wl,--end-group ${OUTPUT_FLAG} ${OUTPUT} ${FLAGS}" id="com.atollic.truestudio.exe.debug.toolchain.ld.85585038" name="C Linker" superClass="com.atollic.truestudio.exe.debug.toolchain.ld">
                                <option id="com.atollic.truestudio.common_options.target.endianess.331908851" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess" value="com.atollic.truestudio.common_options.target.endianess.little" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.1471739127" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.1216358513" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.1652649564" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.ld.general.scriptfile.1257108926" name="Linker script" superClass="com.atollic.truestudio.ld.general.scriptfile" value="../../../../../../platform/devices/MK64F12/linker/gcc/MK64FN1M0xxx12_flash.ld" valueType="string"/>
                                <option id="com.atollic.truestudio.ld.optimization.do_garbage.14195695" name="Dead code removal " superClass="com.atollic.truestudio.ld.optimization.do_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.ld.libraries.list.1896671041" name="Libraries" superClass="com.atollic.truestudio.ld.libraries.list">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.2011019692" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.ld.misc.linkerflags.1817504083" name="Other options" superClass="com.atollic.truestudio.ld.misc.linkerflags" value="-Wl,-cref,-u,Reset_Handler  -g  -mcpu=cortex-m4    -Xlinker -z  -Xlinker muldefs  -Xlinker --defsym=__stack_size__=0x2000  -Xlinker --defsym=__heap_size__=0x2000 " valueType="string"/>
                                <inputType id="com.atollic.truestudio.ld.input.631678650" name="Input" superClass="com.atollic.truestudio.ld.input">
                                    <additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/>
                                    <additionalInput kind="additionalinput" paths="$(LIBS)"/>
                                </inputType>
                                <option id="com.atollic.truestudio.ld.libraries.searchpath.9110425380" superClass="com.atollic.truestudio.ld.libraries.searchpath" valueType="libPaths">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.interwork.8633372160" superClass="com.atollic.truestudio.common_options.target.interwork" valueType="boolean" name="Mix ARM/Thumb" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.clib.7505776997" superClass="com.atollic.truestudio.ld.general.clib" valueType="enumerated" name="Runtime Library:" value="com.atollic.truestudio.ld.general.clib.small"/>
                                <option id="com.atollic.truestudio.ld.general.nostartfiles.7919244705" superClass="com.atollic.truestudio.ld.general.nostartfiles" valueType="boolean" name="Do not use standard start files" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.nodefaultlibs.5457490412" superClass="com.atollic.truestudio.ld.general.nodefaultlibs" valueType="boolean" name="Do not use default libraries" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.nostdlib.7434937581" superClass="com.atollic.truestudio.ld.general.nostdlib" valueType="boolean" name="No startup or default libs" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.static.6721998184" superClass="com.atollic.truestudio.ld.general.static" valueType="boolean" name="No shared libraries" value="true"/>
                                <option id="com.atollic.truestudio.ld.optimization.malloc_page_size.6395305942" superClass="com.atollic.truestudio.ld.optimization.malloc_page_size" valueType="enumerated" value="com.atollic.truestudio.ld.optimization.malloc_page_size.128"/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.debug.toolchain.gpp.79718194" name="C++ Compiler" superClass="com.atollic.truestudio.exe.debug.toolchain.gpp">
                                <option id="com.atollic.truestudio.gpp.symbols.defined.1222927268" name="Defined symbols" superClass="com.atollic.truestudio.gpp.symbols.defined" valueType="definedSymbols">
                                    <listOptionValue builtIn="false" value="TWR_K40X256"/>
                                    <listOptionValue builtIn="false" value="MK40DX256Vyy10"/>
                                </option>
                                <option id="com.atollic.truestudio.gpp.directories.select.1961066684" name="Include path" superClass="com.atollic.truestudio.gpp.directories.select" valueType="includePath">
                                    <listOptionValue builtIn="false" value="../Libraries/Device/MK40DZ10/Include"/>
                                    <listOptionValue builtIn="false" value="../Libraries/CMSIS/Include"/>
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.endianess.1582630576" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess" value="com.atollic.truestudio.common_options.target.endianess.little" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.1556059168" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="MK64FN1M0xxx12" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.1050653589" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb2" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.1265489365" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu"/>
                                <option id="com.atollic.truestudio.gpp.optimization.prep_garbage.2010194253" name="Prepare dead code removal" superClass="com.atollic.truestudio.gpp.optimization.prep_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.gpp.optimization.prep_data.2107446157" name="Prepare dead data removal" superClass="com.atollic.truestudio.gpp.optimization.prep_data" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.gpp.optimization.fno_rtti.2070871605" name="Disable RTTI" superClass="com.atollic.truestudio.gpp.optimization.fno_rtti"/>
                                <option id="com.atollic.truestudio.gpp.optimization.fno_exceptions.1017954361" name="Disable exception handling" superClass="com.atollic.truestudio.gpp.optimization.fno_exceptions"/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.debug.toolchain.ldcc.1340569148" name="C++ Linker" superClass="com.atollic.truestudio.exe.debug.toolchain.ldcc">
                                <option id="com.atollic.truestudio.common_options.target.endianess.1643684024" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess" value="com.atollic.truestudio.common_options.target.endianess.little" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.1516148465" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="MK64FN1M0xxx12" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.284185666" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb2" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.1998420085" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.ldcc.optimization.do_garbage.1663662193" name="Dead code removal" superClass="com.atollic.truestudio.ldcc.optimization.do_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.ldcc.general.scriptfile.2065826101" name="Linker script" superClass="com.atollic.truestudio.ldcc.general.scriptfile" value="..\Kinetis_flash.ld" valueType="string"/>
                                <option id="com.atollic.truestudio.ldcc.libraries.list.960076013" name="Libraries" superClass="com.atollic.truestudio.ldcc.libraries.list" valueType="libs">
                                    <listOptionValue builtIn="false" value="m"/>
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.400308295" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.debug.toolchain.secoutput.714615194" name="Other" superClass="com.atollic.truestudio.exe.debug.toolchain.secoutput"/>
                            <tool id="com.atollic.truestudio.ar.base.1183352833" name="Archiver" superClass="com.atollic.truestudio.ar.base"/>
                        </toolChain>
                    </folderInfo>
                    <sourceEntries/>
                </configuration>
            </storageModule>
            <storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>
        </cconfiguration>
        <cconfiguration id="com.atollic.truestudio.configuration.release.1896242851">
            <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="com.atollic.truestudio.configuration.release.1896242851" moduleId="org.eclipse.cdt.core.settings" name="release">
                <externalSettings/>
                <extensions>
                    <extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.ELF" point="org.eclipse.cdt.core.BinaryParser"/>
                </extensions>
            </storageModule>
            <storageModule moduleId="cdtBuildSystem" version="4.0.0">
                <configuration artifactExtension="elf" artifactName="${ProjName}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exe" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exe" cleanCommand="rm -rf" description="" id="com.atollic.truestudio.configuration.release.1896242851" name="release" parent="com.atollic.truestudio.configuration.release">
                    <folderInfo id="com.atollic.truestudio.configuration.release.1896242851." name="/" resourcePath="">
                        <toolChain id="com.atollic.truestudio.exe.release.toolchain.911269405" name="Atollic ARM Tools" superClass="com.atollic.truestudio.exe.release.toolchain">
                            <targetPlatform archList="all" binaryParser="org.eclipse.cdt.core.ELF" id="com.atollic.truestudio.exe.release.toolchain.platform.1914785304" isAbstract="false" name="release platform" superClass="com.atollic.truestudio.exe.release.toolchain.platform"/>
                            <builder buildPath="${workspace_loc:/TWR-K40/release}" customBuilderProperties="toolChainpathType=1|toolChainpathString=C:/Freescale/TrueSTUDIO for ARM Pro 5.1.1/ARMTools/bin|" id="com.atollic.truestudio.mbs.builder1.1270368140" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="CDT Internal Builder" superClass="com.atollic.truestudio.mbs.builder1"/>
                            <tool id="com.atollic.truestudio.exe.release.toolchain.as.1538550214" name="Assembler" superClass="com.atollic.truestudio.exe.release.toolchain.as">
                                <option id="com.atollic.truestudio.common_options.target.endianess.410621641" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.95962099" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.36842247" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.914307117" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.as.symbols.defined.985068769" name="Defined symbols" superClass="com.atollic.truestudio.as.symbols.defined" valueType="definedSymbols">
                                    <listOptionValue builtIn="false" value="__START=main"/>
                                    <listOptionValue builtIn="false" value="__ATOLLIC__"/>
                                </option>
                                <option id="com.atollic.truestudio.as.general.incpath.1447655736" name="Include path" superClass="com.atollic.truestudio.as.general.incpath" valueType="includePath">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.300012467" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                                <inputType id="com.atollic.truestudio.as.input.23254039" name="Input" superClass="com.atollic.truestudio.as.input"/>
                                <option id="com.atollic.truestudio.as.general.warnings.4477031417" superClass="com.atollic.truestudio.as.general.warnings" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.as.general.version.2932660703" superClass="com.atollic.truestudio.as.general.version" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.as.general.preprocess.4708523849" superClass="com.atollic.truestudio.as.general.preprocess" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.exe.release.toolchain.as.debug.flags.6926312641" superClass="com.atollic.truestudio.exe.release.toolchain.as.debug.flags" valueType="enumerated" name="Debug Level" value="com.atollic.truestudio.as.debug.flags.0"/>
                                <option id="com.atollic.truestudio.as.general.otherflags.1856035887" superClass="com.atollic.truestudio.as.general.otherflags" valueType="string" value=" -mcpu=cortex-m4 "/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.release.toolchain.gcc.1026267958" name="C Compiler" superClass="com.atollic.truestudio.exe.release.toolchain.gcc">
                                <option id="com.atollic.truestudio.gcc.symbols.defined.1865450346" name="Defined symbols" superClass="com.atollic.truestudio.gcc.symbols.defined" valueType="definedSymbols">
                                    <listOptionValue builtIn="false" value="NDEBUG"/>
                                    <listOptionValue builtIn="false" value="ATOLLIC"/>
                                </option>
                                <option id="com.atollic.truestudio.gcc.directories.select.721868316" name="Include path" superClass="com.atollic.truestudio.gcc.directories.select">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.endianess.765626319" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.105097713" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.1916165178" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.1888042170" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.gcc.optimization.prep_garbage.1678181225" name="Prepare dead code removal " superClass="com.atollic.truestudio.gcc.optimization.prep_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.gcc.optimization.prep_data.895522558" name="Prepare dead data removal" superClass="com.atollic.truestudio.gcc.optimization.prep_data" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.1864429197" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.interwork.44305196" name="Mix ARM/Thumb" superClass="com.atollic.truestudio.common_options.target.interwork" value="false"/>
                                <inputType id="com.atollic.truestudio.gcc.input.503979310" superClass="com.atollic.truestudio.gcc.input"/>
                                <option id="com.atollic.truestudio.gcc.misc.longcalls.2713825367" superClass="com.atollic.truestudio.gcc.misc.longcalls" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.gcc.cstandard.7159655685" superClass="com.atollic.truestudio.gcc.cstandard" valueType="enumerated" name="C standard" value="com.atollic.truestudio.gcc.cstandard.gnu99"/>
                                <option id="com.atollic.truestudio.exe.release.toolchain.gcc.optimization.level.1614627591" superClass="com.atollic.truestudio.exe.release.toolchain.gcc.optimization.level" valueType="enumerated" value="com.atollic.truestudio.gcc.optimization.level.0s"/>
                                <option id="com.atollic.truestudio.gcc.optimization.no_strict_aliasing.1196818154" superClass="com.atollic.truestudio.gcc.optimization.no_strict_aliasing" valueType="boolean" name="No strict aliasing" value="false"/>
                                <option id="com.atollic.truestudio.exe.release.toolchain.gcc.debug.info.789959592" superClass="com.atollic.truestudio.exe.release.toolchain.gcc.debug.info" valueType="enumerated" name="Debug Level" value="com.atollic.truestudio.gcc.debug.info.0"/>
                                <option id=" com.atollic.truestudio.gcc.misc.stackusage.5371505366" superClass=" com.atollic.truestudio.gcc.misc.stackusage" valueType="boolean" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.all.5761454616" superClass="com.atollic.truestudio.gcc.warnings.all" valueType="boolean" value="true"/>
                                <option id="com.atollic.truestudio.gcc.warnings.extra.6300153508" superClass="com.atollic.truestudio.gcc.warnings.extra" valueType="boolean" name="Enable extra warning flags" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.fatal.7924695884" superClass="com.atollic.truestudio.gcc.warnings.fatal" valueType="boolean" name="Abort compilation on first error" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.pedantic.9533287069" superClass="com.atollic.truestudio.gcc.warnings.pedantic" valueType="boolean" name="Issue all warnings demanded by strict ISO C and ISO C++" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.pedanticerrors.4976289374" superClass="com.atollic.truestudio.gcc.warnings.pedanticerrors" valueType="boolean" name="Generate error instead of warnings from strict ISO C and C++" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.missing_include_dirs.46845483" superClass="com.atollic.truestudio.gcc.warnings.missing_include_dirs" valueType="boolean" name="Warn if a user-supplied include directory does not exist" value="false"/>
                                <option id="com.atollic.truestudio.gcc.warnings.w_switch_default.5824760967" superClass="com.atollic.truestudio.gcc.warnings.w_switch_default" valueType="boolean" name="Warn when switch statement does not have a default case" value="false"/>
                                <option id=" com.atollic.truestudio.gcc.warnings.w_switch_enum.9082682825" superClass=" com.atollic.truestudio.gcc.warnings.w_switch_enum" valueType="boolean" name="Warn if switch is used on enum type and switch statement lacks case for some enumerations" value="false"/>
                                <option id="com.atollic.truestudio.gcc.misc.otherflags.579815142" superClass="com.atollic.truestudio.gcc.misc.otherflags" valueType="string" value=" -mcpu=cortex-m4 "/>
                            </tool>
                            <tool commandLinePattern="${COMMAND} -Wl,--start-group ${INPUTS} -Wl,--end-group ${OUTPUT_FLAG} ${OUTPUT} ${FLAGS}" id="com.atollic.truestudio.exe.release.toolchain.ld.1066951895" name="C Linker" superClass="com.atollic.truestudio.exe.release.toolchain.ld">
                                <option id="com.atollic.truestudio.common_options.target.endianess.1275255457" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.1671727696" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.1698909671" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.968665588" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.ld.general.scriptfile.1244807755" name="Linker script" superClass="com.atollic.truestudio.ld.general.scriptfile" value="../../../../../../platform/devices/MK64F12/linker/gcc/MK64FN1M0xxx12_flash.ld" valueType="string"/>
                                <option id="com.atollic.truestudio.ld.optimization.do_garbage.919093955" name="Dead code removal " superClass="com.atollic.truestudio.ld.optimization.do_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.ld.libraries.list.1862036761" name="Libraries" superClass="com.atollic.truestudio.ld.libraries.list" valueType="libs">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.1856844648" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.ld.misc.linkerflags.1378937887" name="Other options" superClass="com.atollic.truestudio.ld.misc.linkerflags" value="-Wl,-cref,-u,Reset_Handler  -mcpu=cortex-m4    -Xlinker -z  -Xlinker muldefs  -Xlinker --defsym=__stack_size__=0x2000  -Xlinker --defsym=__heap_size__=0x2000 " valueType="string"/>
                                <inputType id="com.atollic.truestudio.ld.input.1587956591" name="Input" superClass="com.atollic.truestudio.ld.input">
                                    <additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/>
                                    <additionalInput kind="additionalinput" paths="$(LIBS)"/>
                                </inputType>
                                <option id="com.atollic.truestudio.ld.libraries.searchpath.7595966969" superClass="com.atollic.truestudio.ld.libraries.searchpath" valueType="libPaths">
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.interwork.8097570174" superClass="com.atollic.truestudio.common_options.target.interwork" valueType="boolean" name="Mix ARM/Thumb" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.clib.671923063" superClass="com.atollic.truestudio.ld.general.clib" valueType="enumerated" name="Runtime Library:" value="com.atollic.truestudio.ld.general.clib.small"/>
                                <option id="com.atollic.truestudio.ld.general.nostartfiles.727604474" superClass="com.atollic.truestudio.ld.general.nostartfiles" valueType="boolean" name="Do not use standard start files" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.nodefaultlibs.442074017" superClass="com.atollic.truestudio.ld.general.nodefaultlibs" valueType="boolean" name="Do not use default libraries" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.nostdlib.7636346097" superClass="com.atollic.truestudio.ld.general.nostdlib" valueType="boolean" name="No startup or default libs" value="false"/>
                                <option id="com.atollic.truestudio.ld.general.static.1747409906" superClass="com.atollic.truestudio.ld.general.static" valueType="boolean" name="No shared libraries" value="true"/>
                                <option id="com.atollic.truestudio.ld.optimization.malloc_page_size.7891897653" superClass="com.atollic.truestudio.ld.optimization.malloc_page_size" valueType="enumerated" value="com.atollic.truestudio.ld.optimization.malloc_page_size.128"/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.release.toolchain.gpp.1011724318" name="C++ Compiler" superClass="com.atollic.truestudio.exe.release.toolchain.gpp">
                                <option id="com.atollic.truestudio.gpp.symbols.defined.2057471513" name="Defined symbols" superClass="com.atollic.truestudio.gpp.symbols.defined" valueType="definedSymbols">
                                    <listOptionValue builtIn="false" value="TWR_K40X256"/>
                                    <listOptionValue builtIn="false" value="MK40DX256Vyy10"/>
                                </option>
                                <option id="com.atollic.truestudio.gpp.directories.select.2139131698" name="Include path" superClass="com.atollic.truestudio.gpp.directories.select" valueType="includePath">
                                    <listOptionValue builtIn="false" value="../Libraries/Device/MK40DZ10/Include"/>
                                    <listOptionValue builtIn="false" value="../Libraries/CMSIS/Include"/>
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.endianess.695161034" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.1991606448" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="MK64FN1M0xxx12" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.576197098" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb2" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.607944584" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu"/>
                                <option id="com.atollic.truestudio.gpp.optimization.prep_garbage.326877261" name="Prepare dead code removal" superClass="com.atollic.truestudio.gpp.optimization.prep_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.gpp.optimization.prep_data.1542484412" name="Prepare dead data removal" superClass="com.atollic.truestudio.gpp.optimization.prep_data" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.gpp.optimization.fno_rtti.799481401" name="Disable RTTI" superClass="com.atollic.truestudio.gpp.optimization.fno_rtti"/>
                                <option id="com.atollic.truestudio.gpp.optimization.fno_exceptions.1387972702" name="Disable exception handling" superClass="com.atollic.truestudio.gpp.optimization.fno_exceptions"/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.release.toolchain.ldcc.700119183" name="C++ Linker" superClass="com.atollic.truestudio.exe.release.toolchain.ldcc">
                                <option id="com.atollic.truestudio.common_options.target.endianess.250840981" name="Endianess" superClass="com.atollic.truestudio.common_options.target.endianess"/>
                                <option id="com.atollic.truestudio.common_options.target.mcpu.756749863" name="Microcontroller" superClass="com.atollic.truestudio.common_options.target.mcpu" value="MK64FN1M0xxx12" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.instr_set.316305170" name="Instruction set" superClass="com.atollic.truestudio.common_options.target.instr_set" value="com.atollic.truestudio.common_options.target.instr_set.thumb2" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.common_options.target.fpu.653665834" name="Floating point" superClass="com.atollic.truestudio.common_options.target.fpu" value="com.atollic.truestudio.common_options.target.fpu.hard" valueType="enumerated"/>
                                <option id="com.atollic.truestudio.ldcc.optimization.do_garbage.70687813" name="Dead code removal" superClass="com.atollic.truestudio.ldcc.optimization.do_garbage" value="true" valueType="boolean"/>
                                <option id="com.atollic.truestudio.ldcc.general.scriptfile.471739918" name="Linker script" superClass="com.atollic.truestudio.ldcc.general.scriptfile" value="..\Kinetis_flash.ld" valueType="string"/>
                                <option id="com.atollic.truestudio.ldcc.libraries.list.1459903321" name="Libraries" superClass="com.atollic.truestudio.ldcc.libraries.list" valueType="libs">
                                    <listOptionValue builtIn="false" value="m"/>
                                </option>
                                <option id="com.atollic.truestudio.common_options.target.fpucore.57539850" name="FPU" superClass="com.atollic.truestudio.common_options.target.fpucore" value="com.atollic.truestudio.common_options.target.fpucore.fpv4-sp-d16" valueType="enumerated"/>
                            </tool>
                            <tool id="com.atollic.truestudio.exe.release.toolchain.secoutput.1936331422" name="Other" superClass="com.atollic.truestudio.exe.release.toolchain.secoutput"/>
                            <tool id="com.atollic.truestudio.ar.base.480388206" name="Archiver" superClass="com.atollic.truestudio.ar.base"/>
                        </toolChain>
                    </folderInfo>
                    <sourceEntries/>
                </configuration>
            </storageModule>
            <storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>
        </cconfiguration>
    </storageModule>
    <storageModule moduleId="cdtBuildSystem" version="4.0.0">
        <project id="TWR-K40.com.atollic.truestudio.exe.681821844" name="Executable" projectType="com.atollic.truestudio.exe"/>
    </storageModule>
    <storageModule moduleId="scannerConfiguration">
        <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId=""/>
        <scannerConfigBuildInfo instanceId="com.atollic.truestudio.exe.debug.1332848918;com.atollic.truestudio.exe.debug.1332848918.;com.atollic.truestudio.exe.debug.toolchain.gcc.157216120;com.atollic.truestudio.gcc.input.1331079379">
            <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="org.eclipse.cdt.managedbuilder.core.GCCManagedMakePerProjectProfileC"/>
        </scannerConfigBuildInfo>
        <scannerConfigBuildInfo instanceId="com.atollic.truestudio.exe.debug.1332848918;com.atollic.truestudio.exe.debug.1332848918.1759451831;com.atollic.truestudio.exe.debug.toolchain.gcc.584703463;com.atollic.truestudio.gcc.input.642039042">
            <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="org.eclipse.cdt.managedbuilder.core.GCCManagedMakePerProjectProfileC"/>
        </scannerConfigBuildInfo>
        <scannerConfigBuildInfo instanceId="com.atollic.truestudio.exe.debug.1332848918;com.atollic.truestudio.exe.debug.1332848918.1285558872;com.atollic.truestudio.exe.debug.toolchain.gcc.1040411370;com.atollic.truestudio.gcc.input.1053333102">
            <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="org.eclipse.cdt.managedbuilder.core.GCCManagedMakePerProjectProfileC"/>
        </scannerConfigBuildInfo>
        <scannerConfigBuildInfo instanceId="com.atollic.truestudio.exe.debug.1332848918;com.atollic.truestudio.exe.debug.1332848918.289217477;com.atollic.truestudio.exe.debug.toolchain.gcc.1163244267;com.atollic.truestudio.gcc.input.1763945807">
            <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="org.eclipse.cdt.managedbuilder.core.GCCManagedMakePerProjectProfileC"/>
        </scannerConfigBuildInfo>
        <scannerConfigBuildInfo instanceId="com.atollic.truestudio.configuration.release.1896242851;com.atollic.truestudio.configuration.release.1896242851.;com.atollic.truestudio.exe.release.toolchain.gcc.1026267958;com.atollic.truestudio.gcc.input.503979310">
            <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="org.eclipse.cdt.managedbuilder.core.GCCManagedMakePerProjectProfileC"/>
        </scannerConfigBuildInfo>
        <scannerConfigBuildInfo instanceId="com.atollic.truestudio.exe.debug.1332848918;com.atollic.truestudio.exe.debug.1332848918.648981591;com.atollic.truestudio.exe.debug.toolchain.gcc.1932888756;com.atollic.truestudio.gcc.input.2091495926">
            <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId="org.eclipse.cdt.managedbuilder.core.GCCManagedMakePerProjectProfileC"/>
        </scannerConfigBuildInfo>
    </storageModule>
    <storageModule moduleId="refreshScope" versionNumber="1">
        <resource resourceType="PROJECT" workspacePath="/TWR-K40"/>
    </storageModule>
    <storageModule moduleId="org.eclipse.cdt.core.LanguageSettingsProviders"/>
</cproject>
"""

formatted_project = \
"""<?xml version="1.0" encoding="UTF-8"?><projectDescription><name>hello_world_frdmk64f</name><comment/><projects></projects><buildSpec><buildCommand><name>org.eclipse.cdt.managedbuilder.core.genmakebuilder</name><triggers>clean,full,incremental,</triggers><arguments><dictionary><key>?children?</key><value>?name?=outputEntries\|?children?=?name?=entry\\\\\\\|\\\|?name?=entry\\\\\\\|\\\|\||</value></dictionary><dictionary><key>?name?</key><value/></dictionary><dictionary><key>org.eclipse.cdt.make.core.append_environment</key><value>true</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.buildArguments</key><value/></dictionary><dictionary><key>org.eclipse.cdt.make.core.buildCommand</key><value>make</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.buildLocation</key><value>${workspace_loc:/TWR-K40/Debug}</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.contents</key><value>org.eclipse.cdt.make.core.activeConfigSettings</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.enableAutoBuild</key><value>false</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.enableCleanBuild</key><value>true</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.enableFullBuild</key><value>true</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.stopOnError</key><value>true</value></dictionary><dictionary><key>org.eclipse.cdt.make.core.useDefaultBuildCmd</key><value>true</value></dictionary></arguments></buildCommand><buildCommand><name>org.eclipse.cdt.managedbuilder.core.ScannerConfigBuilder</name><triggers>full,incremental,</triggers><arguments></arguments></buildCommand></buildSpec><natures><nature>org.eclipse.cdt.core.cnature</nature><nature>org.eclipse.cdt.managedbuilder.core.managedBuildNature</nature><nature>org.eclipse.cdt.managedbuilder.core.ScannerConfigNature</nature></natures><linkedResources></linkedResources></projectDescription>
"""

language_settings_xml = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project>
    <configuration id="com.atollic.truestudio.exe.debug.1332848918" name="Debug">
        <extension point="org.eclipse.cdt.core.LanguageSettingsProvider">
            <provider copy-of="extension" id="org.eclipse.cdt.ui.UserLanguageSettingsProvider"/>
            <provider-reference id="org.eclipse.cdt.managedbuilder.core.MBSLanguageSettingsProvider" ref="shared-provider"/>
            <provider class="com.atollic.truestudio.mbs.GCCSpecsDetectorAtollicArm" console="false" env-hash="-1513791958" id="com.atollic.truestudio.mbs.provider" keep-relative-paths="false" name="Atollic ARM Tools Language Settings" parameter="${COMMAND} -E -P -v -dD &quot;${INPUTS}&quot;" prefer-non-shared="true">
                <language-scope id="org.eclipse.cdt.core.gcc"/>
                <language-scope id="org.eclipse.cdt.core.g++"/>
            </provider>
        </extension>
    </configuration>
    <configuration id="com.atollic.truestudio.configuration.release.1896242851" name="Release">
        <extension point="org.eclipse.cdt.core.LanguageSettingsProvider">
            <provider copy-of="extension" id="org.eclipse.cdt.ui.UserLanguageSettingsProvider"/>
            <provider-reference id="org.eclipse.cdt.managedbuilder.core.MBSLanguageSettingsProvider" ref="shared-provider"/>
            <provider class="com.atollic.truestudio.mbs.GCCSpecsDetectorAtollicArm" console="false" env-hash="-1513791958" id="com.atollic.truestudio.mbs.provider" keep-relative-paths="false" name="Atollic ARM Tools Language Settings" parameter="${COMMAND} -E -P -v -dD &quot;${INPUTS}&quot;" prefer-non-shared="true">
                <language-scope id="org.eclipse.cdt.core.gcc"/>
                <language-scope id="org.eclipse.cdt.core.g++"/>
            </provider>
        </extension>
    </configuration>
</project>
"""

project_board_debug_jlink_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="com.atollic.hardwaredebug.launch.launchConfigurationType">
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.cpu_core" value="Cortex-M"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.device" value="jlinkDEVICE"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.endian" value="little"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.init_speed" value="4000"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_path" value=""/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_used" value="false"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_trace_port_cfg_path" value="C:\Freescale\TrueSTUDIO for ARM Pro 5.1.1\ide\plugins\com.atollic.truestudio.tsp.freescale_1.0.0.201408201543\tsp\etm\MKxx.init"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_tracebuffer_size" value="16"/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_auto" value="true"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_irpre" value="0"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_pos" value="0"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.analyzeCommands" value="# Default GDB command file (FLASH) for SEGGER J-LINK and Freescale Kinetis devices.&#13;&#10;&#13;&#10;# Set character encoding&#13;&#10;set host-charset CP1252&#13;&#10;set target-charset CP1252&#13;&#10;&#13;&#10;# Set JTAG speed to 30 kHz&#13;&#10;monitor speed 30&#13;&#10;&#13;&#10;# Set GDBServer to little endian&#13;&#10;monitor endian little&#13;&#10;&#13;&#10;# Reset the chip to get to a known state.&#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set auto JTAG speed&#13;&#10;monitor speed auto&#13;&#10;&#13;&#10;# Setup GDB FOR FASTER DOWNLOADS&#13;&#10;set remote memory-write-packet-size 1024&#13;&#10;set remote memory-write-packet-size fixed&#13;&#10;&#13;&#10;# Enable flash download&#13;&#10;monitor flash download = 1&#13;&#10;&#13;&#10;# Flash device&#13;&#10;monitor flash device = jlinkDEVICE&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;&#13;&#10;# Reset the chip to get to a known state. Remove &quot;monitor reset&quot; command &#13;&#10;#  if the code is not located at default address and does not run by reset. &#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Start the executable&#13;&#10;continue"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.enable_live_expr" value="true"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.enable_swv" value="false"/>
<intAttribute key="com.atollic.hardwaredebug.launch.formatVersion" value="2"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.hwinitCommands" value="# Initialize your hardware here&#13;&#10;"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.ipAddress" value="localhost"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.jtagDevice" value="SEGGER J-LINK"/>
<intAttribute key="com.atollic.hardwaredebug.launch.portNumber" value="2331"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.remoteCommand" value="target extended-remote"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.runCommands" value="# Default GDB command file (FLASH) for SEGGER J-LINK and Freescale Kinetis devices.&#13;&#10;&#13;&#10;# Set character encoding&#13;&#10;set host-charset CP1252&#13;&#10;set target-charset CP1252&#13;&#10;&#13;&#10;# Set JTAG speed to 30 kHz&#13;&#10;monitor speed 30&#13;&#10;&#13;&#10;# Set GDBServer to little endian&#13;&#10;monitor endian little&#13;&#10;&#13;&#10;# Reset the chip to get to a known state.&#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set auto JTAG speed&#13;&#10;monitor speed auto&#13;&#10;&#13;&#10;# Setup GDB FOR FASTER DOWNLOADS&#13;&#10;set remote memory-write-packet-size 1024&#13;&#10;set remote memory-write-packet-size fixed&#13;&#10;&#13;&#10;# Enable flash download&#13;&#10;monitor flash download = 1&#13;&#10;&#13;&#10;# Flash device&#13;&#10;monitor flash device = jlinkDEVICE&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;&#13;&#10;# Reset the chip to get to a known state. Remove &quot;monitor reset&quot; command &#13;&#10;#  if the code is not located at default address and does not run by reset. &#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set a breakpoint at main().&#13;&#10;tbreak main&#13;&#10;&#13;&#10;# Run to the breakpoint.&#13;&#10;continue"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.serverParam" value="-port 2331 -s -CPU Cortex-M -device jlinkDEVICE -endian little -speed 4000 -if swd"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.startServer" value="true"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.swd_mode" value="true"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_port" value="2332"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_div" value="8"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_hclk" value="8000000"/>
<intAttribute key="com.atollic.hardwaredebug.launch.trace_system" value="0"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.useRemoteTarget" value="true"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.verifyCommands" value="# Default GDB command file (FLASH) for SEGGER J-LINK and Freescale Kinetis devices.&#13;&#10;&#13;&#10;# Set character encoding&#13;&#10;set host-charset CP1252&#13;&#10;set target-charset CP1252&#13;&#10;&#13;&#10;# Set JTAG speed to 30 kHz&#13;&#10;monitor speed 30&#13;&#10;&#13;&#10;# Set GDBServer to little endian&#13;&#10;monitor endian little&#13;&#10;&#13;&#10;# Reset the chip to get to a known state.&#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set auto JTAG speed&#13;&#10;monitor speed auto&#13;&#10;&#13;&#10;# Setup GDB FOR FASTER DOWNLOADS&#13;&#10;set remote memory-write-packet-size 1024&#13;&#10;set remote memory-write-packet-size fixed&#13;&#10;&#13;&#10;# Enable flash download&#13;&#10;monitor flash download = 1&#13;&#10;&#13;&#10;# Flash device&#13;&#10;monitor flash device = jlinkDEVICE&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;&#13;&#10;# Reset the chip to get to a known state. Remove &quot;monitor reset&quot; command &#13;&#10;#  if the code is not located at default address and does not run by reset. &#13;&#10;monitor reset&#13;&#10;&#13;&#10;# The executable starts automatically"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="debug/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="com.atollic.truestudio.exe.debug.1332848918"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;/&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

project_board_debug_pne_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="com.atollic.hardwaredebug.launch.launchConfigurationType">
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.cpu_core" value="Cortex-M"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.device" value="pneDEVICE"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.endian" value="little"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.init_speed" value="4000"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_path" value=""/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_used" value="false"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_trace_port_cfg_path" value="C:\Freescale\TrueSTUDIO for ARM Pro 5.1.1\ide\plugins\com.atollic.truestudio.tsp.freescale_1.0.0.201408201543\tsp\etm\MKxx.init"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_tracebuffer_size" value="16"/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_auto" value="true"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_irpre" value="0"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_pos" value="0"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.analyzeCommands" value="# Default GDB command file for P&amp;E Micro supported probes&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;"/>
<intAttribute key="com.atollic.hardwaredebug.launch.formatVersion" value="2"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.hwinitCommands" value="# Initialize your hardware here&#13;&#10;"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.ipAddress" value="localhost"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.jtagDevice" value="P&amp;E Micro"/>
<intAttribute key="com.atollic.hardwaredebug.launch.portNumber" value="7224"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.remoteCommand" value="target remote"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.runCommands" value="# Default GDB command file for P&amp;E Micro supported probes&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;# Set a breakpoint at main().&#13;&#10;tbreak main&#13;&#10;&#13;&#10;# Run to the breakpoint.&#13;&#10;continue"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.serverParam" value="/crp  "/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.startServer" value="true"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.swd_mode" value="false"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_port" value="2332"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_div" value="8"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_hclk" value="8000000"/>
<intAttribute key="com.atollic.hardwaredebug.launch.trace_system" value="0"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.useRemoteTarget" value="true"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.verifyCommands" value="# Default GDB command file for P&amp;E Micro supported probes&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="debug/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="com.atollic.truestudio.exe.debug.1332848918"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;/&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

project_board_release_jlink_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="com.atollic.hardwaredebug.launch.launchConfigurationType">
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.cpu_core" value="Cortex-M"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.device" value="jlinkDEVICE"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.endian" value="little"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.init_speed" value="4000"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_path" value=""/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_used" value="false"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_trace_port_cfg_path" value="C:\Freescale\TrueSTUDIO for ARM Pro 5.1.1\ide\plugins\com.atollic.truestudio.tsp.freescale_1.0.0.201408201543\tsp\etm\MKxx.init"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_tracebuffer_size" value="16"/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_auto" value="true"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_irpre" value="0"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_pos" value="0"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.analyzeCommands" value="# Default GDB command file (FLASH) for SEGGER J-LINK and Freescale Kinetis devices.&#13;&#10;&#13;&#10;# Set character encoding&#13;&#10;set host-charset CP1252&#13;&#10;set target-charset CP1252&#13;&#10;&#13;&#10;# Set JTAG speed to 30 kHz&#13;&#10;monitor speed 30&#13;&#10;&#13;&#10;# Set GDBServer to little endian&#13;&#10;monitor endian little&#13;&#10;&#13;&#10;# Reset the chip to get to a known state.&#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set auto JTAG speed&#13;&#10;monitor speed auto&#13;&#10;&#13;&#10;# Setup GDB FOR FASTER DOWNLOADS&#13;&#10;set remote memory-write-packet-size 1024&#13;&#10;set remote memory-write-packet-size fixed&#13;&#10;&#13;&#10;# Enable flash download&#13;&#10;monitor flash download = 1&#13;&#10;&#13;&#10;# Flash device&#13;&#10;monitor flash device = jlinkDEVICE&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;&#13;&#10;# Reset the chip to get to a known state. Remove &quot;monitor reset&quot; command &#13;&#10;#  if the code is not located at default address and does not run by reset. &#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Start the executable&#13;&#10;continue"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.enable_live_expr" value="true"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.enable_swv" value="false"/>
<intAttribute key="com.atollic.hardwaredebug.launch.formatVersion" value="2"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.hwinitCommands" value="# Initialize your hardware here&#13;&#10;"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.ipAddress" value="localhost"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.jtagDevice" value="SEGGER J-LINK"/>
<intAttribute key="com.atollic.hardwaredebug.launch.portNumber" value="2331"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.remoteCommand" value="target extended-remote"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.runCommands" value="# Default GDB command file (FLASH) for SEGGER J-LINK and Freescale Kinetis devices.&#13;&#10;&#13;&#10;# Set character encoding&#13;&#10;set host-charset CP1252&#13;&#10;set target-charset CP1252&#13;&#10;&#13;&#10;# Set JTAG speed to 30 kHz&#13;&#10;monitor speed 30&#13;&#10;&#13;&#10;# Set GDBServer to little endian&#13;&#10;monitor endian little&#13;&#10;&#13;&#10;# Reset the chip to get to a known state.&#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set auto JTAG speed&#13;&#10;monitor speed auto&#13;&#10;&#13;&#10;# Setup GDB FOR FASTER DOWNLOADS&#13;&#10;set remote memory-write-packet-size 1024&#13;&#10;set remote memory-write-packet-size fixed&#13;&#10;&#13;&#10;# Enable flash download&#13;&#10;monitor flash download = 1&#13;&#10;&#13;&#10;# Flash device&#13;&#10;monitor flash device = jlinkDEVICE&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;&#13;&#10;# Reset the chip to get to a known state. Remove &quot;monitor reset&quot; command &#13;&#10;#  if the code is not located at default address and does not run by reset. &#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set a breakpoint at main().&#13;&#10;tbreak main&#13;&#10;&#13;&#10;# Run to the breakpoint.&#13;&#10;continue"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.serverParam" value="-port 2331 -s -CPU Cortex-M -device jlinkDEVICE -endian little -speed 4000 -if swd"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.startServer" value="true"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.swd_mode" value="true"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_port" value="2332"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_div" value="8"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_hclk" value="8000000"/>
<intAttribute key="com.atollic.hardwaredebug.launch.trace_system" value="0"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.useRemoteTarget" value="true"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.verifyCommands" value="# Default GDB command file (FLASH) for SEGGER J-LINK and Freescale Kinetis devices.&#13;&#10;&#13;&#10;# Set character encoding&#13;&#10;set host-charset CP1252&#13;&#10;set target-charset CP1252&#13;&#10;&#13;&#10;# Set JTAG speed to 30 kHz&#13;&#10;monitor speed 30&#13;&#10;&#13;&#10;# Set GDBServer to little endian&#13;&#10;monitor endian little&#13;&#10;&#13;&#10;# Reset the chip to get to a known state.&#13;&#10;monitor reset&#13;&#10;&#13;&#10;# Set auto JTAG speed&#13;&#10;monitor speed auto&#13;&#10;&#13;&#10;# Setup GDB FOR FASTER DOWNLOADS&#13;&#10;set remote memory-write-packet-size 1024&#13;&#10;set remote memory-write-packet-size fixed&#13;&#10;&#13;&#10;# Enable flash download&#13;&#10;monitor flash download = 1&#13;&#10;&#13;&#10;# Flash device&#13;&#10;monitor flash device = jlinkDEVICE&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;&#13;&#10;# Reset the chip to get to a known state. Remove &quot;monitor reset&quot; command &#13;&#10;#  if the code is not located at default address and does not run by reset. &#13;&#10;monitor reset&#13;&#10;&#13;&#10;# The executable starts automatically"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="release/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="com.atollic.truestudio.exe.debug.1332848918"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;/&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

project_board_release_pne_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="com.atollic.hardwaredebug.launch.launchConfigurationType">
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.cpu_core" value="Cortex-M"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.device" value="pneDEVICE"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.endian" value="little"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.init_speed" value="4000"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_path" value=""/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_script_used" value="false"/>
<stringAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_trace_port_cfg_path" value="C:\Freescale\TrueSTUDIO for ARM Pro 5.1.1\ide\plugins\com.atollic.truestudio.tsp.freescale_1.0.0.201408201543\tsp\etm\MKxx.init"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.jlink_tracebuffer_size" value="16"/>
<booleanAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_auto" value="true"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_irpre" value="0"/>
<intAttribute key="com.atollic.hardwaredebug.jlink_common.scan_chain_pos" value="0"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.analyzeCommands" value="# Default GDB command file for P&amp;E Micro supported probes&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;"/>
<intAttribute key="com.atollic.hardwaredebug.launch.formatVersion" value="2"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.hwinitCommands" value="# Initialize your hardware here&#13;&#10;"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.ipAddress" value="localhost"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.jtagDevice" value="P&amp;E Micro"/>
<intAttribute key="com.atollic.hardwaredebug.launch.portNumber" value="7224"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.remoteCommand" value="target remote"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.runCommands" value="# Default GDB command file for P&amp;E Micro supported probes&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;# Set a breakpoint at main().&#13;&#10;tbreak main&#13;&#10;&#13;&#10;# Run to the breakpoint.&#13;&#10;continue"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.serverParam" value="/crp  "/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.startServer" value="true"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.swd_mode" value="false"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_port" value="2332"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_div" value="8"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.swv_trace_hclk" value="8000000"/>
<intAttribute key="com.atollic.hardwaredebug.launch.trace_system" value="0"/>
<booleanAttribute key="com.atollic.hardwaredebug.launch.useRemoteTarget" value="true"/>
<stringAttribute key="com.atollic.hardwaredebug.launch.verifyCommands" value="# Default GDB command file for P&amp;E Micro supported probes&#13;&#10;&#13;&#10;# Load the program executable&#13;&#10;load&#13;&#10;"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${TOOLCHAIN_PATH}/arm-atollic-eabi-gdb"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="release/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="com.atollic.truestudio.exe.debug.1332848918"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;/&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

