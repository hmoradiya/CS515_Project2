import argparse
import math
from decimal import Decimal, getcontext

# Set the precision for decimal arithmetic
getcontext().prec = 20

# Create a parser object
parser = argparse.ArgumentParser(description='A simple calculator that follows the POSIX bc command.')

# Add arguments to the parser
parser.add_argument('-l', '--mathlib', action='store_true', help='use the math library for advanced functions')
parser.add_argument('-q', '--quiet', action='store_true', help='quiet mode, do not print result')
parser.add_argument('-s', '--scale', type=int, default=0, help='number of digits to show after the decimal point')
parser.add_argument('expression', type=str, nargs='+', help='the expression to evaluate')

# Parse the command-line arguments
args = parser.parse_args()

# Set the scale for decimal arithmetic
getcontext().prec = args.scale + 1

# Set the initial environment for the expressions
environment = {}

in_comment_block = False
for i in range(len(args.expression)):
    if "/*" in args.expression[i]:
        args.expression[i] = args.expression[i][:args.expression[i].index("/*")]
        in_comment_block = True
    if "*/" in args.expression[i]:
        args.expression[i] = args.expression[i][args.expression[i].index("*/")+2:]
        in_comment_block = False
    if in_comment_block:
        args.expression[i] = ""

# Evaluate the expressions
for expr in args.expression:
    try:
        exec(expr, environment)
    except SyntaxError:
        print(f'Syntax error: Invalid expression: {expr}')
        exit()

# Format and print the results according to POSIX bc rules
for key, value in environment.items():
    if isinstance(value, Decimal):
        if value >= 0:
            sign = ''
        else:
            sign = '-'
            value = abs(value)
        integer_part = str(int(value))
        decimal_part = str(value - int(value))[2:]
        if len(decimal_part) < args.scale:
            decimal_part = decimal_part + '0' * (args.scale - len(decimal_part))
        elif len(decimal_part) > args.scale:
            decimal_part = decimal_part[:args.scale]
        value_str = sign + integer_part + '.' + decimal_part
    else:
        value_str="123"
        value_str = str(value)
    if not args.quiet:
        print(value_str, end=' ')
       
        

if not args.quiet:
    #print("")
    print("")
# to run 
# python bc.py "x = 3" "y = 5" "z = 2 + x * y" "z2 = (2 + x) * y" "print(x, y, z, z2)"
