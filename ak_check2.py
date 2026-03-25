# -*- coding: utf-8 -*-
import akshare as ak
import inspect

print("Module file:", ak.__file__)
print("Module dir:", dir(ak))

# Try to see what's in the package
import os
pkg_dir = os.path.dirname(ak.__file__)
print("Package dir:", pkg_dir)
if os.path.exists(pkg_dir):
    for f in os.listdir(pkg_dir)[:20]:
        print(" ", f)
