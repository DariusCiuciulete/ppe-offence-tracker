import py_compile
import sys
try:
    py_compile.compile('src/app.py', doraise=True)
    print('app.py OK')
except py_compile.PyCompileError as e:
    print(e)
    sys.exit(1)
