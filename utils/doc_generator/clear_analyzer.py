import sys
import os
import json

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
    if not os.path.isfile(results_json):
        cmd = "docker run -it %s swupd bundle-list -j > %s" % (clr_img,results_json)
        os.system(cmd)

    data = {}

    try:
        with open(results_json) as json_file:
            data = json.load(json_file)
    except ValueError as error:
        print(error)

    for element in data:
        if "msg" in element:
            for key, value in element.iteritems():
                if key == "msg" \
                    and " -" not in value \
                    and "Total" not in value \
                    and "bundles" not in value:
                        print(value)

if __name__ == "__main__":
    main()
