Hardik Moradiya hmoradiy@stevens.edu
Prashanth Pulikonda ppulikon1@stevens.edu

**URL of GitHub repo** https://github.com/hmoradiya/CS515_Project2

**hr. to complate project** 27hr

**Description of testing**
The lex function takes a string of code and returns a list of tokens, which represent the smallest units of syntax in the language, such as variable names, numbers, and operators. The parse function takes the list of tokens and uses them to construct an abstract syntax tree (AST) that represents the structure of the program. The AST is defined recursively as instances of the ast class, which has a typ attribute that identifies the type of node (such as 'var' for a variable name or 'num' for a number), and a children attribute that contains the sub-trees for the node.

The parse function calls the equal function to parse an expression that has an optional assignment at the end. The disjunction function is called by equal to parse a logical OR expression, which is a sequence of one or more conjunctions separated by the || operator. The conjunction function is called by disjunction to parse a logical AND expression, which is a sequence of one or more comparisons separated by the && operator. The comparison function is called by conjunction to parse a comparison expression, which is a comparison of two values using one of the comparison operators such as <, >, <=, >=, ==, or !=. The term function is called by comparison to parse a term, which is a sequence of one or more factors separated by the + or - operator. The factor function is called by term to parse a factor, which is a sequence of one or more atoms separated by the *, /, %, or ^ operator. The atom function is called by factor to parse an atom, which is either a variable name, a number, a function call, or a parenthesized expression.

Step 1: To run this use this comand line,
python bc.py

step 2: Add your erithamtic equaltion
ex.
a=5
b=3

step 3: print the value or equation which you want to print
print a+b

Some example from testing is mentioned below:
input:
x  = 10
y  = 20
z  = 30 + x + y
print x, y, z
output:
10.0 20.0 60.0

input:
side  = 8
square_area = side^2
print square_area
output:
64.0

**Bugs or Issues - not resolve**

No

**Difficult issue or bug and how you resolved**

NO

**List of the extensions**

**1. Comments**
Added extention of comment in which Multi-line comments begin with /* and end with */, with arbitrary line breaks in between also The # character introduces a single-line comment: from # until the end of the line is treated as a comment.

ex.
input:
x = 20
/* 
x = 20 + 5
*/
y = 40
print x, y
output:
20.0 40.0

**2. Relational operations**
Implimented relational operations ==, <=, >=, !=, <, >, using 1 to mean true and 0 to mean false.

ex.
input:
a = 5 
b = 4
print a > b
output:
true

**3. Boolean operations**
Implimented boolean operations for and/conjunction (&&), or/disjunction (||), and negation (!). Treat any non-zero number as true, but only ever return 1 or 0.

ex.
input:
print 1 && 2, 0 && -100
output:
1 0

**4. Control flow**
Implimented if and while statements which generate output based on conditions.

ex.
input:
x = 10
if (x - 5) {
  print possitive
} else {
  print nagative
}
output:
possitive
