import argparse
import os

base_img = "daemon://clearlinux:latest"
new_img="daemon://stacks-tensorflow-mkl:latest"

def get_img_diff():
    cmd = "container-diff diff %s \
	%s --type=file --quiet --json > result.json 2>/dev/null" \
        % (base_img,new_img)
    print(cmd)
    os.system(cmd)


def get_touched_libs():

    cmd = "docker run --rm -v %s/tests:/tests %s /tests/%s" % (pwd,new_img,test)
    print(cmd)


def main():

    parser = argparse.ArgumentParser(description='Coverage tool')
    parser.add_argument('--diff', dest='get_diff', action='store_true',
               help='Get the differnce of two images')
    parser.add_argument('--touched_libs', dest='get_dif', \
        action='store_true', help='Get the libs touched by test')

    args = parser.parse_args()

    if args.get_diff:
        get_img_diff()
    if args.get_touched_libs():
        get_touched_libs()


if __name__== "__main__":
    main()
