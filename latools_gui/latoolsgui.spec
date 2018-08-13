# -*- mode: python -*-

block_cipher = None

folder = os.getcwd()

extra_datas = [('graphics', 'graphics'), 
		('project/recentProjects.txt', 'project'),
		('data', 'data'),
		('latools', 'latools'),
		('logs', 'logs'),
		('logging.conf', ''),
		('information', 'information')]

hiddenimports = ['pandas._libs.tslibs.timedeltas',
		'scipy._lib.messagestream',
		'sklearn.neighbors.typedefs',
		'sklearn.neighbors.quad_tree',
		'sklearn.tree',
		'sklearn',
		'sklearn.tree._utils',
		'pandas._libs.tslibs.np_datetime',
		'pandas._libs.tslibs.nattype',
		'pandas._libs.skiplist',
		'PyQt5.sip',
		'ipykernel.datapub']

a = Analysis(['latoolsgui.py'],
             pathex=[folder],
             binaries=[],
             datas=extra_datas,
             hiddenimports=hiddenimports,
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
          exclude_binaries=True,
          name='latoolsgui',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='latoolsgui')
