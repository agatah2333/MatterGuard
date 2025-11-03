# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for run_dynamic_tests.py
Packages the dynamic test runner with all dependencies
"""

block_cipher = None

a = Analysis(
    ['../Dynamic/run_dynamic_tests.py'],
    pathex=['../Dynamic'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'yaml',
        'yaml.loader',
        'yaml.dumper',
        'yaml.resolver',
        'yaml.scanner',
        'yaml.parser',
        'yaml.composer',
        'yaml.constructor',
        'yaml.emitter',
        'yaml.serializer',
        'yaml.representer',
        'json',
        'logging',
        'subprocess',
        'pathlib',
        'glob',
        're',
        'copy',
        'signal',
        'datetime',
        'dynamic_test_framework',
        'test_enhancer',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Include the framework and enhancer modules
a.datas += [
    ('dynamic_test_framework.py', '../Dynamic/dynamic_test_framework.py', 'DATA'),
    ('test_enhancer.py', '../Dynamic/test_enhancer.py', 'DATA'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run_dynamic_tests',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_dynamic_tests',
)
