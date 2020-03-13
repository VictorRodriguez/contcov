#!/bin/bash

BASE_IMG="daemon://clearlinux:latest"
NEW_IMG="daemon://stack-01-30-20-15-25-43:test"
TEST="numpy_test.py"

get_img_diff ()
{
container-diff diff $BASE_IMG \
	$NEW_IMG \
	--type=file \
	--quiet \
	--json > result.json 2>/dev/null
}

get_touched_libs()
{
docker run --rm -v $PWD/tests:/tests $NEW_IMG /tests/$TEST
}

print_help()
{
echo "Options"
echo "diff"
echo "touched_libs"
}

if [ "$1" == "diff" ]; then
	get_img_diff
elif [ "$1" == "touched_libs" ]; then
	get_touched_libs
elif [ "$1" == "-h" ]; then
	print_help
else
    echo "Positional parameter 1 is empty"
fi
