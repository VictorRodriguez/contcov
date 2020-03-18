# Cont Cov
Identify what libraries your test case is excersing on a contianer image

## Usage

```bash
usage: contcov.py [-h] [--diff] [--added] [--base_image BASE_IMG]
	[--new_image NEW_IMG] [--get_coverage]
                  [--test TEST] [--touched_libs]

Coverage tool

optional arguments:
  -h, --help            show this help message and exit
  --touched_libs        Get the libs touched by test (debug mode)

Get container images diff:
  --diff                Get the differnce of two images
  --added               Get added files
  --base_image BASE_IMG
                        Base Image
  --new_image NEW_IMG   New Image

Get % coverage of a test:
  --get_coverage        Get coverage
  --test TEST           Test

```
## Output

```bash
$ python contcov.py --get_coverage
docker run --rm -v /home/vrodri3/devel/contcov/tests:/tests \
	stacks-tensorflow-mkl:latest strace -q -e trace=file \
	/usr/bin/python /tests/numpy_test.py

container-diff diff \
	daemon://clearlinux:latest daemon://stacks-tensorflow-mkl:latest \
	--type=file --quiet --json > result.json 2>/dev/null

Total files added: 70920
Total files deleted : 149
Total files modified: 795

The test numpy_test.py
Exercise 1257 libraries
Exercise 8 binaries
Of a total of 70920 new files on the image under test
Giving a 1.783700 % of coverage

```

## Files generated for debug

* result.json: Shows the difference of base image and new image
* strace.log: Show the strace of the syscalls excersised by the test under analysis
* binaries_touched.txt: Show the list of binaries excersised by the test under analysis
* libraries_touched.txt: Show the list of libraries excersised by the test under analysis

## Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
