# json_processing script

This is a script for some usefull manipulation with JSON data. I tested this application with Python 2.7*. This script should be used in the way that it is console user interface program:

Input is reading from stdin as it's a textfile in format:

<USER_DEFINED_KEY> <TAB> <JSON_REPRESENTATION> <LF>

<USER_DEFINED_KEY> <TAB> <JSON_REPRESENTATION> <LF>
...
  
Where 
<TAB> -- is tab symbol
<LF> -- is line feeding, a.k.a new line.

So before use this script you should convert text representation of JSON object into representation which doesn't include line feeding.

# Features
Goal is to handle several usefull things for text JSON representaion which can be considered as hierarchical representaion of data:
[1] extract some variable from JSON object by path
[2] extract some variable from JSON object by path and evaluated arbitarily Python expression on this variable. To reference to variable use "value" in your expression
[2] delete some variable from JSON object by path
[3] set some variable to specific value if previously variable was contained within JSON object
[4] set some variable to specific value if previously variable was not contained within JSON object

# Actual Source code for script

https://github.com/burlachenkok/

# Author
Konstantin Burlachenko (burlachenkok@gmail.com)

# Various links
1. Example of usage https://github.com/burlachenkok/json_processing/blob/master/example/demo.sh
2. Data for example https://github.com/burlachenkok/json_processing/blob/master/example 
