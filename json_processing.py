#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Konstantin Burlachenko (burlachenkok@gmail.com).  All rights reserved.
# Consolde based application for manipulation with JSON data

import sys, json, argparse, math

def dumpKeyInfo(outStream, key, value):
    output = u"%s\t%s\n" % (key, value)
    outStream.write(output.encode('utf8', 'ignore'))

def ArgParseCommandLine():
    parser = argparse.ArgumentParser(add_help=True, version='1.0',
                                     description='By default read from stdin <key> <TAB> <json data> <LF>\n' +
                                                 'Perform simple actions on json data and dump result to stdout')

    subparsers = parser.add_subparsers(help='get|set|del')
    # get supparser
    get_parser = subparsers.add_parser('get', help='Python eval and dump <eval expression with "value")>\\t<key>. If "path" is not exist then do nothing.' +
                                                   '\nWrite to stdout <expt(value)> <key>')
    get_parser.add_argument('-p', '--path', required=True,  action='store', help='Slash style path to something in <json data>.')
    get_parser.add_argument('-e', '--expr', required=False, action='store', help='Some python eval code per extract arg, which is stored in "value" variable"')
    get_parser.add_argument('-i', '--input',   required=False, action='store', help='Filename of input file with stored JSON representation for load"')
    get_parser.add_argument('-ink', '--input_no_key',   required=False, action='store', help='Filename of input file with stored single JSON object for load without key information"')
    get_parser.add_argument('-o', '--output',  required=False, action='store', help='Filename of output file with stored JSON representation for write output"')
    get_parser.set_defaults(mode='get')

    # set supparser
    set_parser = subparsers.add_parser('set', help='Set or update variable in json and output updated json data to stdout' +
                                                   '\nWrite to stdout <key>\\t<new json data>')
    set_parser.add_argument('-p', '--path',  required=True,  action='store', help='Slash style path to something in <json data>.')
    set_parser.add_argument('-v', '--value', required=True,  action='store', help='Setuped value')
    set_parser.add_argument('-t', '--type',  required=True,  action='store', choices = ['int','float','str','bool','json'], help='Value type. In that type data will be setuped in json')
    set_parser.add_argument('-i', '--input',    required=False, action='store', help='Filename of input file with stored JSON representation for load"')
    set_parser.add_argument('-ink', '--input_no_key',   required=False, action='store', help='Filename of input file with stored single JSON object for load without key information"')
    set_parser.add_argument('-o', '--output',   required=False, action='store', help='Filename of output file with stored JSON representation for write output"')
    set_parser.set_defaults(mode='set')

    # del supparser
    del_parser = subparsers.add_parser('del', help='Delete something in json serailized data and prtin to stdout new value' +
                                               '\nWrite to stdout <key>\\t<new json>')
    del_parser.add_argument('-p', '--path', action='store', help='Slash style path to remove json data in <json data>.')
    del_parser.add_argument('-i', '--input',  required=False, action='store', help='Filename of input file with stored JSON representation for load"')
    del_parser.add_argument('-ink', '--input_no_key',   required=False, action='store', help='Filename of input file with stored single JSON object for load without key information"')
    del_parser.add_argument('-o', '--output', required=False, action='store', help='Filename of output file with stored JSON representation for write output"')
    del_parser.set_defaults(mode='del')
    return parser.parse_args()

def TraverseDictinoryTo(dic, path):
    trav = dic
    for i in path:
        if (isinstance(trav, list)):
            if int(i) in xrange(len(trav)):
                trav = trav[int(i)]
            else:
                trav = None
                break
        elif (not isinstance(trav, dict) or not trav.has_key(i)):
            trav = None
            break
        else:
            trav = trav[i]
    return trav

TypeConverter = {"int"   : lambda x : int(x),
                 "str"   : lambda x : str(x),
                 "float" : lambda x : float(x),
                 "bool"  : lambda x : bool(x),
                 "json"  : lambda x : json.loads(x)}

def ProcessTextStream(args, streamIn, streamOut, getKeyValue):
    for line in streamIn:
        if len(line.strip()) == 0:
            continue

        key, orig_value = getKeyValue(line)
        decoded = json.loads(unicode(orig_value, 'utf8', 'ignore'))
        path = args.path.strip("\r\n\t/").split("/")
        trav = TraverseDictinoryTo(decoded, path[:-1])
        lst_path = path[-1]

        if (isinstance(trav, list)):
            lst_path = int(lst_path)
            if lst_path not in xrange(len(trav)):
                trav = None
        elif (not isinstance(trav, dict) or (not trav.has_key(lst_path) and args.mode != "set" )):
            trav = None

        if (args.mode == "get" and trav != None):
            value = trav[lst_path]
            convert_value = value
            if (args.expr != None and len(args.expr) > 0):
                convert_value = eval(args.expr)
            if (isinstance(convert_value, dict) or isinstance(convert_value, list)):
                convert_value = json.dumps(convert_value)
            dumpKeyInfo(streamOut, key, convert_value)
        elif (args.mode == "set"):
            if trav != None:
                trav[lst_path] = TypeConverter[args.type](args.value)
            dumpKeyInfo(streamOut, key, json.dumps(decoded))
        elif (args.mode == "del"):
            if trav != None:
                del trav[lst_path]
            dumpKeyInfo(streamOut, key, json.dumps(decoded))

if __name__ == '__main__':
    args = ArgParseCommandLine()
    finput = sys.stdin
    foutput = sys.stdout

    if args.input != None and args.input_no_key != None:
        print >> sys.stderr, "You provide 'input' and 'input_no_key' simulatenously. It's prohibited."
        sys.exit(-1)

    if args.input != None: 
        finput = open(args.input, "rb")
    if args.output != None: 
        foutput = open(args.output, "wb")
    if args.input_no_key != None: 
        finput = open(args.input_no_key, "rb")
        finput = ["file:" + args.input_no_key + "\t" + finput.read().replace("\r\n", "").replace("\n", "")]

    ProcessTextStream(args, finput, foutput, lambda line : line.strip("\r\n").split("\t", 1))

    if args.input != None:
        finput.close()
    if args.output != None: 
        foutput.close()


