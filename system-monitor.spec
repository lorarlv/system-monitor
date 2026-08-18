from pathlib import Path

project_root = Path(SPECPATH)

frontend_dist = project_root / "frontend" / "dist"
hardware_dir = project_root / "vendor" / "LibreHardwareMonitor"

datas = [
    (
        str(frontend_dist),
        "frontend/dist",
    ),
    (
        str(hardware_dir),
        "vendor/LibreHardwareMonitor",
    ),
]

a = Analysis(
    ["build_entry.py"],
    pathex=["src"],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "clr",
    ],
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
    name="SystemMonitor",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="SystemMonitor",
)