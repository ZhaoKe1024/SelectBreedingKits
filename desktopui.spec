# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['desktopui.py',
    'func.py',
    'graphfromtable.py',
    'BreedingMain.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/analyzer/commonAncestors.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/analyzer/data_example.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/analyzer/LayerGraph.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/procedure/kinship_on_graph.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/procedure/xlsx2graph.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/procedure/xlsxreader.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/selector/entities.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/selector/GASelector.py',
    'C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding/widgets/MainWindow.py',],
    pathex=['C:/Program Files (zk)/PythonOperatOptimiz/SelectBreeding'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='desktopui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='desktopui',
)
