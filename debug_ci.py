#!/usr/bin/env python
"""Debug script to help identify CI issues"""
import sys
import os
from pathlib import Path

print("=" * 60)
print("CI DEBUG INFORMATION")
print("=" * 60)

# Python version
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")

# Current directory
print(f"Current Directory: {os.getcwd()}")
print(f"Directory Contents: {list(Path('.').iterdir())}")

# Python path
print("\nPython Path:")
for p in sys.path:
    print(f"  - {p}")

# Check if packages can be imported
print("\nPackage Import Tests:")

packages_to_test = [
    "shadcn_agent",
    "shadcn_agent.cli",
    "components",
    "pytest",
    "requests",
    "bs4",
    "dotenv",
]

for package in packages_to_test:
    try:
        __import__(package)
        print(f"  ✓ {package}")
    except ImportError as e:
        print(f"  ✗ {package}: {e}")

# Check langgraph separately (optional)
try:
    import langgraph
    print(f"  ✓ langgraph (version: {langgraph.__version__ if hasattr(langgraph, '__version__') else 'unknown'})")
except ImportError:
    print(f"  ℹ langgraph: Not available (expected for Python 3.8)")

# Check environment variables
print("\nEnvironment Variables (filtered):")
for key in ["SENDER_EMAIL", "DEFAULT_RECIPIENT", "PYTHONPATH"]:
    value = os.environ.get(key, "NOT SET")
    if key == "SENDER_EMAIL" and value != "NOT SET":
        value = value[:3] + "***"  # Hide email
    print(f"  {key}: {value}")

# Check if test files exist
print("\nTest Files:")
test_dir = Path("tests")
if test_dir.exists():
    for test_file in test_dir.glob("test_*.py"):
        print(f"  - {test_file}")
else:
    print("  ✗ tests directory not found!")

# Check components structure
print("\nComponents Structure:")
comp_dir = Path("components")
if comp_dir.exists():
    for subdir in ["nodes", "workflows"]:
        sub_path = comp_dir / subdir
        if sub_path.exists():
            print(f"  ✓ components/{subdir}/")
            for py_file in sub_path.glob("*.py"):
                print(f"    - {py_file.name}")
        else:
            print(f"  ✗ components/{subdir}/ not found")
else:
    print("  ✗ components directory not found!")

print("=" * 60)
