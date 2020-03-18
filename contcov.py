#!/usr/bin/env python

import argparse
import os
import re
import json
from os import path

base_img = "clearlinux:latest"
new_img="stacks-tensorflow-mkl:latest"
result_json="result.json"
test="numpy_test.py"
strace_log = "strace.log"

libraries = []
binaries = []

def process_json():
    adds = []
    dels = []
    mods = []

    with open(result_json) as json_file:
        data = json.load(json_file)
        for p in data[0]['Diff']['Adds']:
            adds.append(p)
        for p in data[0]['Diff']['Dels']:
            dels.append(p)
        for p in data[0]['Diff']['Mods']:
            mods.append(p)

    return adds,dels,mods

def get_img_diff(args):

    adds = []
    dels = []
    mods = []

    if not path.exists(result_json):
        cmd = "container-diff diff daemon://%s \
            daemon://%s --type=file --quiet --json > %s 2>/dev/null" \
            % (base_img,new_img,result_json)
        print(cmd)
        os.system(cmd)
    adds,dels,mods = process_json()

    print("Total files added: " + str(len(adds)))
    print("Total files deleted : " + str(len(dels)))
    print("Total files modified: " + str(len(mods)))

    if args.get_added:
        for element in adds:
            print(element.get("Name"))

def print_list(list_items,file_name):
    with open(file_name, 'w') as f:
        for item in list_items:
                f.write("%s\n" % item)

def process_log(strace_log):
    with open(strace_log) as fp:
        lines = fp.readlines()
        for line in lines:
            if "/usr/lib" in line:
                #m = re.search('<(.+?)>', line)
                m = re.search('/usr/lib/(.+?)"',line)
                if m:
                    lib = m.group(1)
                    if lib not in libraries:
                        libraries.append( "/usr/lib/"+ lib)
            if "/usr/bin" in line:
                m = re.search('/usr/bin/(.+?)"',line)
                if m:
                    binary = "/usr/bin/" + m.group(1)
                    if binary not in binaries:
                        binaries.append(binary)

    print_list(libraries,"libraries_touched.txt")
    print_list(binaries,"binaries_touched.txt")

def get_touched_libs():

    if not path.exists(strace_log):
        cwd = os.getcwd()
        cmd = "docker run --rm \
        -v %s/tests:/tests %s strace -q -e trace=file /usr/bin/python /tests/%s"\
        % (cwd,new_img,test)
        print(cmd)
        os.system(cmd  + "> %s 2>&1" % (strace_log))

    if path.exists(strace_log):
        process_log(strace_log)

def print_report(bin_exec,lib_exec,adds):
    print("The test " + test)
    print("Exercise %d libraries" % (len(libraries)))
    print("Exercise %d binaries" % (len(binaries)))
    print("Of a total of %d new files on the image under test" % (len(adds)))
    coverage = ((len(libraries) + len(binaries)) / len(adds) ) * 100
    print("Giving a %f %s of coverage" % (coverage,'%'))

def get_coverage(args):

        bin_exec = []
        lib_exec = []

        get_touched_libs()
        get_img_diff(args)
        adds,dels,mods = process_json()
        for element in adds:
            for lib in libraries:
                if lib in element.get("Name"):
                    if lib not in lib_exec:
                        lib_exec.append(lib)
            for binary in binaries:
                if binary in element.get("Name"):
                    if binary not in bin_exec:
                        bin_exec.append(binary)

        print_report(bin_exec,lib_exec,adds)

def main():

    global base_img
    global new_img
    global test

    parser = argparse.ArgumentParser(description='Coverage tool')
    group_diff = parser.add_argument_group('Get container images diff')
    group_diff.add_argument('--diff', dest='get_diff', action='store_true',
               help='Get the differnce of two images')
    group_diff.add_argument('--added', dest='get_added', action='store_true',
               help='Get added files')
    group_diff.add_argument('--base_image', dest='base_img', \
        help='Base Image')
    group_diff.add_argument('--new_image', dest='new_img', \
        help='New Image')

    group_coverage = parser.add_argument_group('Get % coverage of a test')
    group_coverage.add_argument('--get_coverage', dest='get_coverage', \
        action='store_true', help='Get coverage')
    group_coverage.add_argument('--test', dest='test', \
        help='Test')

    parser.add_argument('--touched_libs', dest='touched_libs', \
        action='store_true', help='Get the libs touched by test (debug mode)')


    args = parser.parse_args()

    if args.get_diff \
    or args.get_added:
        get_img_diff(args)
    if args.touched_libs:
        get_touched_libs()
    if args.get_coverage:
        get_coverage(args)

    if args.base_img:
        base_img = args.base_img
    if args.new_img:
        new_img = args.new_img
    if args.test:
        test = args.test


if __name__== "__main__":
    main()
