#!/usr/bin/env bash
set -o xtrace
PATH_TO_SCRIPT=./../

cat test_input_for_process.json 
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py get -p "isAlive"
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py get -p "phoneNumbers"
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py get -p "phoneNumbers/1"
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py get -p "phoneNumbers/0"
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py del -p "phoneNumbers/0"
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py del -p "phoneNumbers/1"
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py set -p "firstName" -v "Stephen P." -t str
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py set -p "newIntField" -v "10" -t int
cat test_input_for_process.json | ${PATH_TO_SCRIPT}/json_processing.py get -p "age" -e " \"My age is \" + str(value) "

