# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for create_assistant.py
Packages the OpenAI Assistant creation script
"""

block_cipher = None

a = Analysis(
    ['../create_assistant.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../.env.example', '.'),
    ],
    hiddenimports=[
        'openai',
        'openai.types',
        'openai.types.beta',
        'openai.types.beta.assistant',
        'openai.types.beta.threads',
        'dotenv',
        'pathlib',
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='create_assistant',
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
    name='create_assistant',
)
