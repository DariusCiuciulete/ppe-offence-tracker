#!/usr/bin/env python
import sys
import ast

try:
    with open('src/app.py', 'r') as f:
        code = f.read()
    ast.parse(code)
    print('app.py syntax is OK')
except SyntaxError as e:
    print(f'Syntax error in app.py: {e}')
    print(f'Line {e.lineno}: {e.text}')
    sys.exit(1)
