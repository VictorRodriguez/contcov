import sys
import os
import json
import re


def get_size(bundle, clr_img):

    result_json = ".bundle.json"
    cmd = "docker run -u 0 -it %s swupd bundle-info %s -j > %s" % (
        clr_img, bundle, result_json)
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
                for key, value in element.iteritems():
                    if key == "msg" and "Size bundle" in value:
                        size = str(value.strip().split(":")[1]).split(" ")[1]
                        return int(float(size))


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
                for key, value in element.iteritems():
                    if key == "msg" \
                            and " -" not in value \
                            and "Total" not in value \
                            and "bundles" not in value \
                            and "manifest" not in value:
                        bundles.append(str(value.strip()))
    return bundles


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

    results_json = "results.json"
    cmd = "docker run -it %s swupd bundle-list -j > %s" % (
        clr_img, results_json)
    os.system(cmd)
    get_bundles(results_json)


if __name__ == "__main__":
    main()
