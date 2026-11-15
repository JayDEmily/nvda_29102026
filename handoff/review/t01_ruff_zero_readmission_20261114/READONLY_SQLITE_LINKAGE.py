#!/usr/bin/env python3
"""Read-only Python/SQLite linkage inventory; never executes product proof."""
from __future__ import annotations

import _sqlite3
import ctypes
import json
import os
import re
import sqlite3
import subprocess
import sys

ext = getattr(_sqlite3, "__file__", None)
out = {
    "audit": "READ_ONLY_SQLITE_LINKAGE",
    "python_executable": sys.executable,
    "python_version": sys.version.split()[0],
    "selected_python_sqlite_version": sqlite3.sqlite_version,
    "_sqlite3_module_origin": _sqlite3.__spec__.origin,
    "_sqlite3_builtin": "_sqlite3" in sys.builtin_module_names,
    "_sqlite3_extension_file": ext,
    "ld_library_path": os.getenv("LD_LIBRARY_PATH"),
    "product_proof_executed": False,
    "runtime_modified": False,
}
lib = ctypes.CDLL("libsqlite3.so.0")
lib.sqlite3_libversion.restype = ctypes.c_char_p
out["system_shared_sqlite_version"] = lib.sqlite3_libversion().decode("ascii")
out["system_shared_sqlite_resolution"] = "/usr/lib/x86_64-linux-gnu/libsqlite3.so.0"
for name, command in (
    ("ldd_python", ["ldd", sys.executable]),
    ("ldd_extension", ["ldd", ext] if ext else None),
):
    if command is None:
        out[name] = None
        continue
    result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=15)
    out[name] = [
        re.sub(r"\s*\(0x[0-9a-fA-F]+\)", "", line.strip())
        for line in result.stdout.splitlines()
    ]
print(json.dumps(out, indent=2, sort_keys=True))
