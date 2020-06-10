import sys
import os
import json
import re


def get_size(bundle, clr_img):

    result_json = ".bundle.json"
    if has_entry_point:
        cmd = 'docker run -u 0 -it --entrypoint="" %s swupd bundle-info %s -j > %s' % (
            clr_img, bundle, result_json)
        print(cmd)
        os.system(cmd)
    else:
        cmd = "docker run -u 0 -it %s swupd bundle-info %s -j > %s" % (
            clr_img, bundle, result_json)
        print(cmd)
        os.system(cmd)

    data = {}
    try:
        with open(result_json) as json_file:
            data = json.load(json_file)
    except ValueError as error:
        print(error)
    if data:
        for element in data:
            if "msg" in element:
                for key, value in element.items():
                    if key == "msg" and "Size bundle" in value:
                        if "MB" in value:
                            size = str(value.strip().split(":")[1]).split(" ")[1]
                            return float(size)
                        if "GB" in value:
                            size = str(value.strip().split(":")[1]).split(" ")[1]
                            size = 1000 * float(size)
                            return size
    else:
        return 0


def get_bundles(results_json):

    data = {}
    try:
        with open(results_json) as json_file:
            data = json.load(json_file)
    except ValueError as error:
        print(error)

    bundles = []
    if data:
        for element in data:
            if "msg" in element:
                for key, value in element.items():
                    if key == "msg" \
                            and " -" not in value \
                            and "Total" not in value \
                            and "bundles" not in value \
                            and "manifest" not in value:
                        bundles.append(str(value.strip()))
    return bundles

def has_entry_point(clr_img):
    cmd = "docker inspect --format='{{.Config.Entrypoint}}' %s > .log" % (clr_img)
    os.system(cmd)
    with open(".log") as fp:
        lines = fp.readlines()
        for line in lines:
            if "[]" in line:
                ret = False
            else:
                ret = True
    return ret

def main():
    """
    main function
    """
    if len(sys.argv) < 2:
        print("\nERROR : Missing arguments, the expected arguments are:")
        print("\n   %s <clr img> \n" % (sys.argv[0]))
        print("\n")
        sys.exit(0)

    clr_img = sys.argv[1]

    results_json = ".clear_results.json"
    if has_entry_point:
        cmd = 'docker run -it --entrypoint="" %s swupd bundle-list -j > %s' % (
            clr_img, results_json)
        print(cmd)
        if os.system(cmd):
            sys.exit(0)
    else:
        cmd = "docker run -it %s swupd bundle-list -j > %s" % (
            clr_img, results_json)
        print(cmd)
        os.system(cmd)
        if os.system(cmd):
            sys.exit(0)

    bundles = get_bundles(results_json)

    for bundle in bundles:
        size = get_size(bundle,clr_img)
        print(bundle)
        print(size)
if __name__ == "__main__":
    main()
