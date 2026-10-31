"""Compatibility entry point for the current Windows builder.

Use `python desktop/build_windows.py build` (or omit the action for the UI).
The historical cache/destination positional arguments are no longer used.
"""
from compiler import main

if __name__ == '__main__':
    raise SystemExit(main())
