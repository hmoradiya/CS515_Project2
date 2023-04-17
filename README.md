Hardik Moradiya hmoradiy@stevens.edu
Prashanth Pulikonda 

**URL of GitHub repo** https://github.com/hmoradiya/CS515_Project2

**hr. to complate project** 24hr

**Description of testing**

**Testing with basic arithmetic operations**
I ran the code with simple arithmetic operations such as addition, multiplication, and division, to ensure that it correctly evaluates and calculates the expressions based on the given arguments.
Command: python bc.py "x = 3" "y = 5" "z = x + y" "print(z)"
Output: 8

**Testing with advanced math functions using the math library**
I used the "-l" option to enable the use of the math library, and then I tested expressions that involve advanced math functions such as sin, sqrt, and log, to ensure that the code properly handles these functions and returns accurate results.
Command: python bc.py -l "x = 2.5" "y = math.sqrt(x)" "print(y)"
Output: 1.5811388300841898

**Testing with comments in expressions**
I tested expressions that include comments, denoted by "/" and "/", to ensure that the code correctly handles and ignores comments, and only evaluates the valid part of the expressions.
Command: python bc.py "x = 3" "/* This is a comment */" "y = 5" "z = x * y" "print(z)"
Output: 15

**Testing with quiet mode**
I used the "-q" option to enable quiet mode, which suppresses the output, and tested expressions to ensure that the code does not print any results when quiet mode is enabled.
Command: python bc.py -q "x = 3" "y = 5" "z = x + y" "print(z)"
Output: (No output)

**Testing with different scales**
I used different values for the scale argument, which determines the number of digits to show after the decimal point, to test that the code correctly formats and displays the results with the specified scale.
Command: python bc.py -s 3 "x = 1/3" "y = 0.25" "z = x + y" "print(z)"
Output: 0.583

**Testing with invalid expressions**
I intentionally included invalid expressions, such as expressions with syntax errors, to ensure that the code properly catches and reports errors for invalid expressions.
Command: python bc.py "x = 3" "y = 5" "z = x + " "print(z)"
Output: Syntax error: Invalid expression: z = x +

**Bugs or Issues - not resolve**

No

**Difficult issue or bug and how you resolved**

NO

**List of the extensions**

**1. "....**
