# -*- mode: python -*-
a = Analysis(['../src/projgen.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='KSDK_Project_Generator.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False , icon='..\\src\\kds_icon.ico')
