import sys
from cx_Freeze import setup, Executable
 
base = None

if (sys.platform == "win32"):
    base = "Win32GUI"

packages = []
includes = ['enkanetwork', 'PySimpleGUI', 'json', 'asyncio']
excludes = []
 
# exe にしたい python ファイルを指定
exe = Executable(script = 'Artifacter.py',
                 base = base)
 
# セットアップ
setup(name = 'Artifacter',
      version = '0.1',
      description = 'converter',
      options={'build_exe': {'includes': includes, 'excludes': excludes, 'packages': packages}},
      executables = [exe])