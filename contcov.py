import argparse
import os
import re
import json
from os import path

base_img = "clearlinux:latest"
new_img="stacks-tensorflow-mkl:latest"
result_json="result.json"
test="numpy_test.py"
strace_log = "/tmp/log"

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

def get_touched_libs():

    cwd = os.getcwd()
    cmd = "docker run --rm \
    -v %s/tests:/tests %s strace -q -e trace=file /usr/bin/python /tests/%s"\
    % (cwd,new_img,test)
    print(cmd)
    os.system(cmd  + "> %s 2>&1" % (strace_log))

    if path.exists(strace_log):
        process_log(strace_log)

def main():

    parser = argparse.ArgumentParser(description='Coverage tool')
    parser.add_argument('--diff', dest='get_diff', action='store_true',
               help='Get the differnce of two images')
    parser.add_argument('--added', dest='get_added', action='store_true',
               help='Get added files')
    parser.add_argument('--touched_libs', dest='touched_libs', \
        action='store_true', help='Get the libs touched by test')

    args = parser.parse_args()

    if args.get_diff:
        get_img_diff(args)
    if args.touched_libs:
        get_touched_libs()

if __name__== "__main__":
    main()
