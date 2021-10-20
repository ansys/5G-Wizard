# -*- mode: python ; coding: utf-8 -*-




block_cipher = None


a = Analysis(['5G_Wizard.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='5G_Wizard',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None ,
          icon="images/icon.ico")
print(DISTPATH)
import shutil
import os

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path,ignore=shutil.ignore_patterns('*.aedtresults', '*.aedb','*.lock'))

copy_and_overwrite('./validation/','{0}/validation/'.format(DISTPATH))
copy_and_overwrite('./template/','{0}/template/'.format(DISTPATH))
copy_and_overwrite('./static/','{0}/static/'.format(DISTPATH))
copy_and_overwrite('./example_projects/','{0}/example_projects/'.format(DISTPATH))
#shutil.copytree('./static/', '{0}/static/'.format(DISTPATH))