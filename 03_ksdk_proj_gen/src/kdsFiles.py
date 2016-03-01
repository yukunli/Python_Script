"""
File:  kdsFiles.py
==================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Dictionary of image files**

.. codeauthor:: B45635<getpass.getuser()@freescale.com>

.. sectionauthor:: B45635<getpass.getuser()@freescale.com>

.. versionadded:: 0.0.6

"""

formatted_cproject = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?><?fileVersion 4.0.0?><cproject storage_type_id="org.eclipse.cdt.core.XmlProjectDescriptionStorage"><storageModule moduleId="org.eclipse.cdt.core.settings"><cconfiguration id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861"><storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861" moduleId="org.eclipse.cdt.core.settings" name="debug"><externalSettings/><extensions><extension id="org.eclipse.cdt.core.ELF" point="org.eclipse.cdt.core.BinaryParser"/><extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/><extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/><extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/><extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/></extensions></storageModule><storageModule moduleId="cdtBuildSystem" version="4.0.0"><configuration artifactName="${ProjName}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exe" buildProperties="org.eclipse.cdt.build.core.buildType=org.eclipse.cdt.build.core.buildType.debug,org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exe" cleanCommand="${cross_rm} -rf" description="" id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861" name="debug" parent="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug" artifactExtension="elf"><folderInfo id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861." name="/" resourcePath=""><toolChain id="ilg.gnuarmeclipse.managedbuild.cross.toolchain.elf.debug.439601044" name="Cross ARM GCC" superClass="ilg.gnuarmeclipse.managedbuild.cross.toolchain.elf.debug"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.level.780228407" name="Optimization Level" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.level" value="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.level.size" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.messagelength.1547417078" name="Message length (-fmessage-length=0)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.messagelength" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.signedchar.765602671" name="'char' is signed (-fsigned-char)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.signedchar" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.functionsections.910567930" name="Function sections (-ffunction-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.functionsections" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.datasections.243581182" name="Data sections (-fdata-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.datasections" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.allwarn.416266830" name="Enable all common warnings (-Wall)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.allwarn" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.level.1613409592" name="debug level" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.level" value="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.level.default" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.format.556186202" name="debug format" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.format" value="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.format.default"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.name.873832382" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.name" value="Custom" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.architecture.1923839154" name="Architecture" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.architecture" value="ilg.gnuarmeclipse.managedbuild.cross.option.architecture.arm" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.family.292907889" name="ARM family" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.family" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.mcpu.cortex-m4" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.instructionset.1510156849" name="Instruction set" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.instructionset" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.instructionset.thumb" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.prefix.1110645397" name="Prefix" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.prefix" value="arm-none-eabi-" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.c.1996567256" name="C compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.c" value="gcc" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.cpp.2014665560" name="C++ compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.cpp" value="g++" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.objcopy.867581768" name="Hex/Bin converter" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.objcopy" value="objcopy" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.objdump.315789427" name="Listing generator" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.objdump" value="objdump" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.size.348642956" name="Size command" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.size" value="size" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.make.670689833" name="Build command" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.make" value="make" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.rm.654501139" name="Remove command" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.rm" value="rm" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createflash.967248865" name="Create flash image" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createflash" value="false" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.printsize.1390211406" name="Print size" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.printsize" value="false" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.useglobalpath.228343129" name="Use global path" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.useglobalpath" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.unit.1173170148" name="FPU Type" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.unit" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.unit.fpv4spd16" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi.1949324826" name="Float ABI" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi.hard" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.ar.1370140886" name="Archiver" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.ar" value="ar" valueType="string"/><targetPlatform archList="all" binaryParser="org.eclipse.cdt.core.ELF" id="ilg.gnuarmeclipse.managedbuild.cross.targetPlatform.1777290613" isAbstract="false" osList="all" superClass="ilg.gnuarmeclipse.managedbuild.cross.targetPlatform"/><builder buildPath="${workspace_loc:/k64f}/debug" id="ilg.gnuarmeclipse.managedbuild.cross.builder.1406291427" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="Gnu Make Builder" parallelBuildOn="true" parallelizationNumber="optimal" stopOnErr="false" superClass="ilg.gnuarmeclipse.managedbuild.cross.builder"/><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler.2007968129" name="Cross ARM GNU Assembler" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.usepreprocessor.1246588554" name="Use preprocessor" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.usepreprocessor" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.include.paths.2122094274" name="Include paths (-I)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.include.paths" valueType="includePath"/><inputType id="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler.input.2014783385" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler.input"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.defs.9135873444" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.defs" valueType="definedSymbols"><listOptionValue builtIn="false" value="DEBUG"/></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.nostdinc.1053541580" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.nostdinc" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.other.173715309" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.other" valueType="string" value="-fno-common  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin  -Os  -mapcs  -std=gnu99"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.1397207158" name="Cross ARM C Compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.include.paths.336878990" name="Include paths (-I)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.include.paths" useByScannerDiscovery="false" valueType="includePath"></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.std.933718024" name="Language standard" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.std" useByScannerDiscovery="true" value="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.std.gnu99" valueType="enumerated"/><inputType id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.input.1895544709" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.input"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.defs.869311397" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.defs" valueType="definedSymbols"><listOptionValue builtIn="false" value="DEBUG"/></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.nostdinc.4671085848" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.nostdinc" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.other.2661180054" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.other" valueType="string" value="-fno-common  -ffreestanding  -fno-builtin  -mapcs"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.compiler.435207489" name="Cross ARM C++ Compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.compiler"/><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker.1681324840" name="Cross ARM C Linker" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker" outputPrefix="" commandLinePattern="${COMMAND} ${cross_toolchain_flags} ${FLAGS} ${OUTPUT_FLAG} ${OUTPUT_PREFIX}${OUTPUT} -Xlinker --start-group ${INPUTS} -Xlinker --end-group"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.gcsections.1850945755" name="Remove unused sections (-Xlinker --gc-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.gcsections" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.scriptfile.1573832003" name="Script files (-T)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.scriptfile" valueType="stringList"></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.libs.2061142742" name="Libraries (-l)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.libs"><listOptionValue builtIn="false" value="m"/><listOptionValue builtIn="false" value="g"/><listOptionValue builtIn="false" value="gcc"/><listOptionValue builtIn="false" value="nosys"/></option><inputType id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker.input.1168552163" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker.input"><additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/><additionalInput kind="additionalinput" paths="$(LIBS)"/></inputType><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.otherobjs.3524946900" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.otherobjs" valueType="userObjs"></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostart.6031988652" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostart" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nodeflibs.1607275937" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nodeflibs" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostdlibs.3232119319" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostdlibs" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.cref.7071123662" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.cref" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.printgcsections.7393360104" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.printgcsections" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.strip.1021177932" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.strip" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.other.7241614120" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.other" valueType="string" value="-Xlinker -z  -Xlinker muldefs   --specs=nano.specs          -Wall  -fno-common  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin  -Os  -mapcs  -Xlinker -static "/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.linker.1475612095" name="Cross ARM C++ Linker" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.linker"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.cpp.linker.gcsections.42905068" name="Remove unused sections (-Xlinker --gc-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.cpp.linker.gcsections" value="true" valueType="boolean"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.archiver.717958418" name="Cross ARM GNU Archiver" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.archiver"/><tool command="${cross_prefix}${cross_objcopy}${cross_suffix}" commandLinePattern="${COMMAND} ${FLAGS} ${OUTPUT_FLAG} ${OUTPUT_PREFIX}${OUTPUT}" id="ilg.gnuarmeclipse.managedbuild.cross.tool.createflash.1498748442" name="Cross ARM GNU Create Flash Image" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.createflash"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createflash.choice.396105459" name="Output file format (-O)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createflash.choice" value="ilg.gnuarmeclipse.managedbuild.cross.option.createflash.choice.srec" valueType="enumerated"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.createlisting.1921141825" name="Cross ARM GNU Create Listing" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.createlisting"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.source.1147761851" name="Display source (--source|-S)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.source" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.allheaders.326654770" name="Display all headers (--all-headers|-x)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.allheaders" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.demangle.2012585764" name="Demangle names (--demangle|-C)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.demangle" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.linenumbers.1639985926" name="Display line numbers (--line-numbers|-l)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.linenumbers" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.wide.795915960" name="Wide lines (--wide|-w)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.wide" value="true" valueType="boolean"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.printsize.204256629" name="Cross ARM GNU Print Size" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.printsize"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.printsize.format.48990078" name="Size format" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.printsize.format"/></tool><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.nowarn.125059113" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.nowarn" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.extrawarn.3161081234" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.extrawarn" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.conversion.6366181077" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.conversion" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.unitialized.8210852711" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.unitialized" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.floatequal.6608258382" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.floatequal" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.shadow.9019869902" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.shadow" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.pointerarith.9951999698" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.pointerarith" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.badfunctioncast.3029317604" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.badfunctioncast" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.logicalop.7242512433" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.logicalop" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.agreggatereturn.5547623719" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.agreggatereturn" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.missingdeclaration.1319479159" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.missingdeclaration" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.toerrors.2662680550" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.toerrors" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createlisting.5968890558" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createlisting" valueType="boolean" value="false"/></toolChain></folderInfo><sourceEntries/></configuration></storageModule><storageModule moduleId="org.eclipse.cdt.core.externalSettings"/></cconfiguration><cconfiguration id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.release.1939339834"><storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.release.1939339834" moduleId="org.eclipse.cdt.core.settings" name="release"><externalSettings/><extensions><extension id="org.eclipse.cdt.core.ELF" point="org.eclipse.cdt.core.BinaryParser"/><extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/><extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/><extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/><extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/></extensions></storageModule><storageModule moduleId="cdtBuildSystem" version="4.0.0"><configuration artifactName="${ProjName}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exe" buildProperties="org.eclipse.cdt.build.core.buildType=org.eclipse.cdt.build.core.buildType.release,org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exe" cleanCommand="${cross_rm} -rf" description="" id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.release.1939339834" name="release" parent="ilg.gnuarmeclipse.managedbuild.cross.config.elf.release" artifactExtension="elf"><folderInfo id="ilg.gnuarmeclipse.managedbuild.cross.config.elf.release.1939339834." name="/" resourcePath=""><toolChain id="ilg.gnuarmeclipse.managedbuild.cross.toolchain.elf.release.338803166" name="Cross ARM GCC" superClass="ilg.gnuarmeclipse.managedbuild.cross.toolchain.elf.release"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.level.1916499380" name="Optimization Level" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.level" value="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.level.size" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.messagelength.1460543599" name="Message length (-fmessage-length=0)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.messagelength" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.signedchar.177322323" name="'char' is signed (-fsigned-char)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.signedchar" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.functionsections.356292453" name="Function sections (-ffunction-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.functionsections" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.datasections.666658360" name="Data sections (-fdata-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.optimization.datasections" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.allwarn.1018775359" name="Enable all common warnings (-Wall)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.allwarn" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.level.597989734" name="debug level" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.level" value="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.level.none"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.format.773110826" name="debug format" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.format" value="ilg.gnuarmeclipse.managedbuild.cross.option.debugging.format.default"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.name.28437861" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.name" value="Custom" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.architecture.1461080496" name="Architecture" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.architecture" value="ilg.gnuarmeclipse.managedbuild.cross.option.architecture.arm" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.family.1124565964" name="ARM family" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.family" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.mcpu.cortex-m4" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.instructionset.1600158089" name="Instruction set" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.instructionset" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.instructionset.thumb" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.prefix.1115996221" name="Prefix" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.prefix" value="arm-none-eabi-" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.c.1677262447" name="C compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.c" value="gcc" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.cpp.1626484215" name="C++ compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.cpp" value="g++" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.objcopy.634682233" name="Hex/Bin converter" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.objcopy" value="objcopy" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.objdump.361919006" name="Listing generator" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.objdump" value="objdump" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.size.279076886" name="Size command" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.size" value="size" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.make.1573227602" name="Build command" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.make" value="make" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.rm.1269834234" name="Remove command" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.rm" value="rm" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createflash.286942610" name="Create flash image" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createflash" value="false" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.printsize.992362786" name="Print size" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.printsize" value="false" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.useglobalpath.1682061124" name="Use global path" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.toolchain.useglobalpath" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.command.ar.43762243" name="Archiver" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.command.ar" value="ar" valueType="string"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi.1631437179" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi.hard" valueType="enumerated"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.unit.977377894" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.unit" value="ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.unit.fpv4spd16" valueType="enumerated"/><targetPlatform archList="all" binaryParser="org.eclipse.cdt.core.ELF" id="ilg.gnuarmeclipse.managedbuild.cross.targetPlatform.1508624923" isAbstract="false" osList="all" superClass="ilg.gnuarmeclipse.managedbuild.cross.targetPlatform"/><builder buildPath="${workspace_loc:/k64f}/release" id="ilg.gnuarmeclipse.managedbuild.cross.builder.506636371" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="Gnu Make Builder" parallelBuildOn="false" stopOnErr="false" superClass="ilg.gnuarmeclipse.managedbuild.cross.builder"/><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler.142183468" name="Cross ARM GNU Assembler" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.usepreprocessor.260968363" name="Use preprocessor" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.usepreprocessor" value="true" valueType="boolean"/><inputType id="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler.input.871599837" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.assembler.input"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.include.paths.5567074147" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.include.paths" valueType="includePath"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.defs.9611736493" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.defs" valueType="definedSymbols"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.nostdinc.409975085" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.nostdinc" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.other.5521860251" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.assembler.other" valueType="string" value="-fno-common  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin  -Os  -mapcs  -std=gnu99"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.955273220" name="Cross ARM C Compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.include.paths.767758500" name="Include paths (-I)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.include.paths" useByScannerDiscovery="false" valueType="includePath"></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.std.997197032" name="Language standard" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.std" useByScannerDiscovery="true" value="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.std.gnu99" valueType="enumerated"/><inputType id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.input.1711058916" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.input"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.defs.2881285214" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.defs" valueType="definedSymbols"><listOptionValue builtIn="false" value="NDEBUG"/></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.nostdinc.4475251566" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.nostdinc" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.other.4053677756" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.other" valueType="string" value="-fno-common  -ffreestanding  -fno-builtin  -mapcs"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.compiler.270191615" name="Cross ARM C++ Compiler" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.compiler"/><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker.1286541465" name="Cross ARM C Linker" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker" outputPrefix="" commandLinePattern="${COMMAND} ${cross_toolchain_flags} ${FLAGS} ${OUTPUT_FLAG} ${OUTPUT_PREFIX}${OUTPUT} -Xlinker --start-group ${INPUTS} -Xlinker --end-group"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.gcsections.1012325190" name="Remove unused sections (-Xlinker --gc-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.gcsections" value="true" valueType="boolean"/><inputType id="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker.input.1297163151" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker.input"><additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/><additionalInput kind="additionalinput" paths="$(LIBS)"/></inputType><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.otherobjs.7937988098" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.otherobjs" valueType="userObjs"></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.scriptfile.6469517" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.scriptfile" valueType="stringList"></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostart.9736990526" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostart" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nodeflibs.8816006162" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nodeflibs" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostdlibs.1203463195" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.nostdlibs" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.libs.9935362500" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.libs" valueType="libs"><listOptionValue builtIn="false" value="m"/><listOptionValue builtIn="false" value="g"/><listOptionValue builtIn="false" value="gcc"/><listOptionValue builtIn="false" value="nosys"/></option><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.cref.1145674860" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.cref" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.printgcsections.382914792" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.printgcsections" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.strip.7846751806" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.strip" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.other.8910989286" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.other" valueType="string" value="-Xlinker -z  -Xlinker muldefs   --specs=nano.specs          -Wall  -fno-common  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin  -Os  -mapcs  -Xlinker -static "/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.linker.1288631479" name="Cross ARM C++ Linker" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.cpp.linker"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.cpp.linker.gcsections.1722094624" name="Remove unused sections (-Xlinker --gc-sections)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.cpp.linker.gcsections" value="true" valueType="boolean"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.archiver.571275503" name="Cross ARM GNU Archiver" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.archiver"/><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.createflash.815118717" name="Cross ARM GNU Create Flash Image" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.createflash"/><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.createlisting.254728314" name="Cross ARM GNU Create Listing" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.createlisting"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.source.1925404631" name="Display source (--source|-S)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.source" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.allheaders.167640084" name="Display all headers (--all-headers|-x)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.allheaders" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.demangle.1474313123" name="Demangle names (--demangle|-C)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.demangle" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.linenumbers.1969680589" name="Display line numbers (--line-numbers|-l)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.linenumbers" value="true" valueType="boolean"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.wide.240541858" name="Wide lines (--wide|-w)" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.createlisting.wide" value="true" valueType="boolean"/></tool><tool id="ilg.gnuarmeclipse.managedbuild.cross.tool.printsize.572718337" name="Cross ARM GNU Print Size" superClass="ilg.gnuarmeclipse.managedbuild.cross.tool.printsize"><option id="ilg.gnuarmeclipse.managedbuild.cross.option.printsize.format.1162591107" name="Size format" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.printsize.format"/></tool><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.nowarn.4190204815" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.nowarn" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.extrawarn.5139173489" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.extrawarn" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.conversion.8572175177" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.conversion" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.unitialized.5482879550" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.unitialized" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.floatequal.4110423051" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.floatequal" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.shadow.1162004361" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.shadow" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.pointerarith.8222562428" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.pointerarith" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.badfunctioncast.2834760048" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.badfunctioncast" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.logicalop.5556409328" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.logicalop" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.agreggatereturn.3098654561" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.agreggatereturn" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.missingdeclaration.2101929494" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.missingdeclaration" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.toerrors.5285909601" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.warnings.toerrors" valueType="boolean" value="false"/><option id="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createlisting.9692488858" superClass="ilg.gnuarmeclipse.managedbuild.cross.option.addtools.createlisting" valueType="boolean" value="false"/></toolChain></folderInfo><sourceEntries/></configuration></storageModule><storageModule moduleId="org.eclipse.cdt.core.externalSettings"/></cconfiguration></storageModule><storageModule moduleId="cdtBuildSystem" version="4.0.0"><project id="k64f.ilg.gnuarmeclipse.managedbuild.cross.target.elf.1537007018" name="Executable" projectType="ilg.gnuarmeclipse.managedbuild.cross.target.elf"/></storageModule><storageModule moduleId="scannerConfiguration"><autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId=""/><scannerConfigBuildInfo instanceId="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861;ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861.;ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.1397207158;ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.input.1895544709"><autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId=""/></scannerConfigBuildInfo><scannerConfigBuildInfo instanceId="ilg.gnuarmeclipse.managedbuild.cross.config.elf.release.1939339834;ilg.gnuarmeclipse.managedbuild.cross.config.elf.release.1939339834.;ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.955273220;ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler.input.1711058916"><autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId=""/></scannerConfigBuildInfo></storageModule><storageModule moduleId="org.eclipse.cdt.core.LanguageSettingsProviders"/><storageModule moduleId="refreshScope" versionNumber="2"><configuration configurationName="release"><resource resourceType="PROJECT" workspacePath="/FRDM-K64F_Test"/></configuration><configuration configurationName="Multiple configurations"><resource resourceType="PROJECT" workspacePath="/FRDM-K64F_Demo"/></configuration><configuration configurationName="debug"><resource resourceType="PROJECT" workspacePath="/FRDM-K64F_Test"/></configuration></storageModule><storageModule moduleId="org.eclipse.cdt.make.core.buildtargets"/></cproject>
"""

formatted_project = \
"""<?xml version="1.0" encoding="UTF-8"?><projectDescription><name></name><comment/><projects></projects><buildSpec><buildCommand><name>com.freescale.processorexpert.core.expertprojectbuilder</name><arguments></arguments></buildCommand><buildCommand><name>org.eclipse.cdt.managedbuilder.core.genmakebuilder</name><triggers>clean,full,incremental,</triggers><arguments></arguments></buildCommand><buildCommand><name>org.eclipse.cdt.managedbuilder.core.ScannerConfigBuilder</name><triggers>full,incremental,</triggers><arguments></arguments></buildCommand></buildSpec><natures><nature>com.freescale.processorexpert.core.expertprojectnature</nature><nature>org.eclipse.cdt.core.cnature</nature><nature>org.eclipse.cdt.managedbuilder.core.managedBuildNature</nature><nature>org.eclipse.cdt.managedbuilder.core.ScannerConfigNature</nature></natures><linkedResources></linkedResources></projectDescription>
"""

formatted_wsd = \
"""<?xml version="1.0"?><workspace xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="workingsets.xsd"><projects></projects><workingsets></workingsets><cdtconfigurations></cdtconfigurations></workspace>
"""

project_board_debug_cmsisdap_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="ilg.gnuarmeclipse.debug.gdbjtag.openocd.launchConfigurationType">
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doConnectToRunning" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doContinue" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doFirstReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doGdbServerAllocateConsole" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doGdbServerAllocateTelnetConsole" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doSecondReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doStartGdbServer" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.enableSemihosting" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.enableSemihostingIoclientTelnet" value="false"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.firstResetType" value="init"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbClientOtherCommands" value="set mem inaccessible-by-default off"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbClientOtherOptions" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerConnectionAddress" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerExecutable" value="${openocd_path}/${openocd_executable}"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerGdbPortNumber" value="3333"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerLog" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerOther" value="-f kinetis.cfg"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerTelnetPortNumber" value="4444"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.otherInitCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.otherRunCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.secondResetType" value="halt"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageOffset" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.ipAddress" value="localhost"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.jtagDevice" value="GNU ARM OpenOCD"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadSymbols" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.pcRegister" value=""/>
<intAttribute key="org.eclipse.cdt.debug.gdbjtag.core.portNumber" value="3333"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setPcRegister" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setResume" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setStopAt" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.stopAt" value="main"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsOffset" value=""/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForImage" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForSymbols" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForSymbols" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useRemoteTarget" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${cross_prefix}gdb${cross_suffix}"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="debug/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;/&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

project_board_debug_jlink_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="ilg.gnuarmeclipse.debug.gdbjtag.jlink.launchConfigurationType">
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doConnectToRunning" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doContinue" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doFirstReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerAllocateConsole" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerAllocateSemihostingConsole" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerInitRegs" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerLocalOnly" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerSilent" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerVerifyDownload" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doSecondReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doStartGdbServer" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableFlashBreakpoints" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSemihosting" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSemihostingIoclientGdbClient" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSemihostingIoclientTelnet" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSwo" value="false"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.firstResetSpeed" value="30"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.firstResetType" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbClientOtherCommands" value="set mem inaccessible-by-default off"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbClientOtherOptions" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerConnection" value="usb"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerConnectionAddress" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDebugInterface" value="swd"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDeviceEndianness" value="little"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDeviceName" value="jlinkDEVICE"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDeviceSpeed" value="30"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerExecutable" value="${jlink_path}/${jlink_gdbserver}"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerGdbPortNumber" value="2331"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerLog" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerOther" value="-s"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerSwoPortNumber" value="2332"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerTelnetPortNumber" value="2333"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.interfaceSpeed" value="auto"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.otherInitCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.otherRunCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.secondResetType" value=""/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.swoEnableTargetCpuFreq" value="0"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.swoEnableTargetPortMask" value="0x1"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.swoEnableTargetSwoFreq" value="0"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageOffset" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.ipAddress" value="localhost"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.jtagDevice" value="GNU ARM J-Link"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadSymbols" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.pcRegister" value=""/>
<intAttribute key="org.eclipse.cdt.debug.gdbjtag.core.portNumber" value="2331"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setPcRegister" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setResume" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setStopAt" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.stopAt" value="main"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsOffset" value=""/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForImage" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForSymbols" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForSymbols" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useRemoteTarget" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${cross_prefix}gdb${cross_suffix}"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="debug/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;&gt;&#13;&#10;&lt;gdbmemoryBlockExpression address=&quot;0&quot; label=&quot;0&quot;/&gt;&#13;&#10;&lt;/memoryBlockExpressionList&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

project_board_debug_pne_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="com.pemicro.debug.gdbjtag.pne.launchConfigurationType">
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.DEVICE_NAME" value="pneDEVICE"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.GDB_IP" value="127.0.0.1"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.GDB_OPTIONS" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.GDB_PORT" value="7224"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.PE.HARDWARE_INTERFACE" value="6"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.LAST_ATTRIBUTE_HEADER" value="com.pemicro.debug.gdbjtag.pne.sda."/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.PE.USE_EXTERNAL_SERVER" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doConnectToRunning" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doContinue" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doFirstReset" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerAllocateConsole" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerAllocateSemihostingConsole" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerInitRegs" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerLocalOnly" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerSilent" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerVerifyDownload" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doSecondReset" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doStartGdbServer" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableFlashBreakpoints" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSemihosting" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSemihostingIoclientGdbClient" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSemihostingIoclientTelnet" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSwo" value="true"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.firstResetSpeed" value="30"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.firstResetType" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbClientOtherCommands" value="set mem inaccessible-by-default off&#13;&#10;set tcp auto-retry on&#13;&#10;set tcp connect-timeout 30"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbClientOtherOptions" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerConnection" value="usb"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerConnectionAddress" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDebugInterface" value="swd"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDeviceEndianness" value="little"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDeviceName" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDeviceSpeed" value="30"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerExecutable" value="${jlink_path}/JLinkGDBServerCL"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerGdbPortNumber" value="7224"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerLog" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerOther" value="-s"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerSwoPortNumber" value="2332"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerTelnetPortNumber" value="51794"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.interfaceSpeed" value="auto"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.ml.INTERFACE_PORT" value="-1"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.POWER_UP_DELAY" value="1000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.ml.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.STARTUP_USE_SWD" value="true"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.otherInitCommands" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.otherRunCommands" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.sda.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.INTERFACE_PORT_STRING" value="USB1"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.POWER_DOWN_DELAY" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.POWER_UP_DELAY" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.sda.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.STARTUP_USE_SWD" value="true"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.secondResetType" value=""/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.swoEnableTargetCpuFreq" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.swoEnableTargetPortMask" value="0x1"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.swoEnableTargetSwoFreq" value="0"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.STARTUP_USE_SWD" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageOffset" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.ipAddress" value="127.0.0.1"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.jtagDevice" value="GNU ARM J-Link"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadSymbols" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.pcRegister" value=""/>
<intAttribute key="org.eclipse.cdt.debug.gdbjtag.core.portNumber" value="7224"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setPcRegister" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setResume" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setStopAt" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.stopAt" value="main"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsOffset" value=""/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForImage" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForSymbols" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForSymbols" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useRemoteTarget" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${cross_prefix}gdb${cross_suffix}"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="debug/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<booleanAttribute key="org.eclipse.debug.ui.ATTR_LAUNCH_IN_BACKGROUND" value="false"/>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;/&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

project_board_release_cmsisdap_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="ilg.gnuarmeclipse.debug.gdbjtag.openocd.launchConfigurationType">
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doConnectToRunning" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doContinue" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doFirstReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doGdbServerAllocateConsole" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doGdbServerAllocateTelnetConsole" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doSecondReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.doStartGdbServer" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.enableSemihosting" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.enableSemihostingIoclientTelnet" value="false"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.firstResetType" value="init"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbClientOtherCommands" value="set mem inaccessible-by-default off"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbClientOtherOptions" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerConnectionAddress" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerExecutable" value="${openocd_path}/${openocd_executable}"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerGdbPortNumber" value="3333"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerLog" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerOther" value="-f kinetis.cfg"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.gdbServerTelnetPortNumber" value="4444"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.otherInitCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.otherRunCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.openocd.secondResetType" value="halt"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageOffset" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.ipAddress" value="localhost"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.jtagDevice" value="GNU ARM OpenOCD"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadSymbols" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.pcRegister" value=""/>
<intAttribute key="org.eclipse.cdt.debug.gdbjtag.core.portNumber" value="3333"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setPcRegister" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setResume" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setStopAt" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.stopAt" value="main"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsOffset" value=""/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForImage" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForSymbols" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForSymbols" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useRemoteTarget" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${cross_prefix}gdb${cross_suffix}"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="release/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861"/>
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
<launchConfiguration type="ilg.gnuarmeclipse.debug.gdbjtag.jlink.launchConfigurationType">
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doConnectToRunning" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doContinue" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doFirstReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerAllocateConsole" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerAllocateSemihostingConsole" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerInitRegs" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerLocalOnly" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerSilent" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doGdbServerVerifyDownload" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doSecondReset" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.doStartGdbServer" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableFlashBreakpoints" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSemihosting" value="true"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSemihostingIoclientGdbClient" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSemihostingIoclientTelnet" value="false"/>
<booleanAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.enableSwo" value="false"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.firstResetSpeed" value="30"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.firstResetType" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbClientOtherCommands" value="set mem inaccessible-by-default off"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbClientOtherOptions" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerConnection" value="usb"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerConnectionAddress" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDebugInterface" value="swd"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDeviceEndianness" value="little"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDeviceName" value="jlinkDEVICE"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerDeviceSpeed" value="30"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerExecutable" value="${jlink_path}/${jlink_gdbserver}"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerGdbPortNumber" value="2331"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerLog" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerOther" value="-s"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerSwoPortNumber" value="2332"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.gdbServerTelnetPortNumber" value="2333"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.interfaceSpeed" value="auto"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.otherInitCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.otherRunCommands" value=""/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.secondResetType" value=""/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.swoEnableTargetCpuFreq" value="0"/>
<stringAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.swoEnableTargetPortMask" value="0x1"/>
<intAttribute key="ilg.gnuarmeclipse.debug.gdbjtag.jlink.swoEnableTargetSwoFreq" value="0"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageOffset" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.ipAddress" value="localhost"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.jtagDevice" value="GNU ARM J-Link"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadSymbols" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.pcRegister" value=""/>
<intAttribute key="org.eclipse.cdt.debug.gdbjtag.core.portNumber" value="2331"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setPcRegister" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setResume" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setStopAt" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.stopAt" value="main"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsOffset" value=""/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForImage" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForSymbols" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForSymbols" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useRemoteTarget" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${cross_prefix}gdb${cross_suffix}"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="release/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;&gt;&#13;&#10;&lt;gdbmemoryBlockExpression address=&quot;0&quot; label=&quot;0&quot;/&gt;&#13;&#10;&lt;/memoryBlockExpressionList&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

project_board_release_pne_launch = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<launchConfiguration type="com.pemicro.debug.gdbjtag.pne.launchConfigurationType">
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.DEVICE_NAME" value="pneDEVICE"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.GDB_IP" value="127.0.0.1"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.GDB_OPTIONS" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.GDB_PORT" value="7224"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.PE.HARDWARE_INTERFACE" value="6"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.PE.LAST_ATTRIBUTE_HEADER" value="com.pemicro.debug.gdbjtag.pne.sda."/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.PE.USE_EXTERNAL_SERVER" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_eth.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_ser.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.cyc_usb.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doConnectToRunning" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doContinue" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doFirstReset" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerAllocateConsole" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerAllocateSemihostingConsole" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerInitRegs" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerLocalOnly" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerSilent" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doGdbServerVerifyDownload" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doSecondReset" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.doStartGdbServer" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableFlashBreakpoints" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSemihosting" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSemihostingIoclientGdbClient" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSemihostingIoclientTelnet" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.enableSwo" value="true"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.firstResetSpeed" value="30"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.firstResetType" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbClientOtherCommands" value="set mem inaccessible-by-default off&#13;&#10;set tcp auto-retry on&#13;&#10;set tcp connect-timeout 30"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbClientOtherOptions" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerConnection" value="usb"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerConnectionAddress" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDebugInterface" value="swd"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDeviceEndianness" value="little"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDeviceName" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerDeviceSpeed" value="30"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerExecutable" value="${jlink_path}/JLinkGDBServerCL"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerGdbPortNumber" value="7224"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerLog" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerOther" value="-s"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerSwoPortNumber" value="2332"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.gdbServerTelnetPortNumber" value="51794"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.interfaceSpeed" value="auto"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.ml.INTERFACE_PORT" value="-1"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.POWER_UP_DELAY" value="1000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.ml.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.ml.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.ml.STARTUP_USE_SWD" value="true"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.otherInitCommands" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.otherRunCommands" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.sda.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.INTERFACE_PORT_STRING" value="USB1"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.POWER_DOWN_DELAY" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.POWER_UP_DELAY" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.sda.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.sda.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.sda.STARTUP_USE_SWD" value="true"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.secondResetType" value=""/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.swoEnableTargetCpuFreq" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.swoEnableTargetPortMask" value="0x1"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.swoEnableTargetSwoFreq" value="0"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_eth.STARTUP_USE_SWD" value="true"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.ALWAYS_ERASE" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.CYCLONE_IP" value=""/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.DO_RESET_DELAY" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.INTERFACE_PORT" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.INTERFACE_PORT_STRING" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.NETWORK_CARD_IP" value=""/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.POWER_DOWN_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.POWER_OFF" value="false"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.POWER_UP_DELAY" value="250"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.PROVIDE_POWER" value="false"/>
<intAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.REGULATOR_VOLTAGE" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.RESET_DELAY" value="0"/>
<stringAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.SHIFT_FREQ" value="5000"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.SPECIFY_IP" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.SPECIFY_NETWORK_CARD" value="false"/>
<booleanAttribute key="com.pemicro.debug.gdbjtag.pne.trc_usb.STARTUP_USE_SWD" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.imageOffset" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.ipAddress" value="127.0.0.1"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.jtagDevice" value="GNU ARM J-Link"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.loadSymbols" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.pcRegister" value=""/>
<intAttribute key="org.eclipse.cdt.debug.gdbjtag.core.portNumber" value="7224"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setPcRegister" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setResume" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.setStopAt" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.stopAt" value="main"/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsFileName" value=""/>
<stringAttribute key="org.eclipse.cdt.debug.gdbjtag.core.symbolsOffset" value=""/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForImage" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useFileForSymbols" value="false"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForImage" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useProjBinaryForSymbols" value="true"/>
<booleanAttribute key="org.eclipse.cdt.debug.gdbjtag.core.useRemoteTarget" value="true"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.commandFactory" value="Standard (Windows)"/>
<stringAttribute key="org.eclipse.cdt.debug.mi.core.protocol" value="mi"/>
<booleanAttribute key="org.eclipse.cdt.debug.mi.core.verboseMode" value="false"/>
<stringAttribute key="org.eclipse.cdt.dsf.gdb.DEBUG_NAME" value="${cross_prefix}gdb${cross_suffix}"/>
<booleanAttribute key="org.eclipse.cdt.dsf.gdb.UPDATE_THREADLIST_ON_SUSPEND" value="false"/>
<intAttribute key="org.eclipse.cdt.launch.ATTR_BUILD_BEFORE_LAUNCH_ATTR" value="2"/>
<stringAttribute key="org.eclipse.cdt.launch.COREFILE_PATH" value=""/>
<stringAttribute key="org.eclipse.cdt.launch.PROGRAM_NAME" value="release/project_board.elf"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_ATTR" value="project_board"/>
<booleanAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_AUTO_ATTR" value="true"/>
<stringAttribute key="org.eclipse.cdt.launch.PROJECT_BUILD_CONFIG_ID_ATTR" value="ilg.gnuarmeclipse.managedbuild.cross.config.elf.debug.1792027861"/>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_PATHS">

<listEntry value="/project_board"/></listAttribute>
<listAttribute key="org.eclipse.debug.core.MAPPED_RESOURCE_TYPES">
<listEntry value="4"/>
</listAttribute>
<booleanAttribute key="org.eclipse.debug.ui.ATTR_LAUNCH_IN_BACKGROUND" value="false"/>
<stringAttribute key="org.eclipse.dsf.launch.MEMORY_BLOCKS" value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; standalone=&quot;no&quot;?&gt;&#13;&#10;&lt;memoryBlockExpressionList context=&quot;reserved-for-future-use&quot;/&gt;&#13;&#10;"/>
<stringAttribute key="process_factory_id" value="org.eclipse.cdt.dsf.gdb.GdbProcessFactory"/>
</launchConfiguration>
"""

