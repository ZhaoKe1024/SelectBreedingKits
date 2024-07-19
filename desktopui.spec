# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['desktopui.py',
    'func.py',
    'graphfromtable.py',
    'BreedingMain.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/analyzer/commonAncestors.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/analyzer/data_example.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/analyzer/LayerGraph.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/procedure/kinship_on_graph.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/procedure/xlsx2graph.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/procedure/xlsxreader.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/selector/entities.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/selector/GASelector.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/widgets_tab/LoginWindow.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/widgets_tab/MainWindow.py',
    'D:/kingz/pythonFiles/SelectBreedingKits/widgets_tab/RegisterWindow.py',],
    pathex=['D:/kingz/pythonFiles/SelectBreedingKits/'],
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
