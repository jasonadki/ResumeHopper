# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(['ResumeHopper.py'],
             pathex=['C:\\Users\\jason\\Desktop\\HR',
       'C:\\Users\\jason\\Downloads\\poppler-0.68.0'],
             binaries=[('C:\\Users\\jason\\Desktop\\HR\\*.exe', 'pdf2image')],
             datas=[('C:\\Users\\jason\\Desktop\\HR\\*.dll', 'pdf2image')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ResumeHopper',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True
          )