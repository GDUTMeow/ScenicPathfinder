# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

streamlit_data, streamlit_binary, streamlit_hidden = collect_all('streamlit')
pydantic_data, pydantic_binary, pydantic_hidden = collect_all('pydantic')
networkx_data, networkx_binary, networkx_hidden = collect_all('networkx')


# 你的项目文件
item_datas = [
    ("./app.py", "."),
    ("./pages", "pages"),
    ("./models", "models"),
    ("./context", "context"),
    ("./exceptions", "exceptions"),
    ("./resources", "resources"),
]

all_datas = streamlit_data + pydantic_data + networkx_data + item_datas
all_binaries = streamlit_binary + pydantic_binary + networkx_binary
all_hidden = streamlit_hidden + pydantic_hidden + networkx_hidden + [
    'pydantic.deprecated.decorator',
    'models', 
    'context', 
    'exceptions'
]

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=['./hooks'],
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
    name='ScenicPathfinder 景区寻路系统',
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
    icon='./resources/favicon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScenicPathfinder 景区寻路系统',
)
