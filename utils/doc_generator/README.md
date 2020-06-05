# Container image doc generator

The goal of this is: 

•	Print what packages are installed on the image (RPM, APT, PIP)
•	Print what files are installed on the image related to the components (i.e. memcached)

It was tested with the image sysstacks/dbrs-memcached-centos8:latest and ubuntu:18.04

## Instructions

1) Create json file with [container-diff](https://github.com/GoogleContainerTools/container-diff)

```
/usr/local/bin/container-diff analyze -j -q \
  daemon://sysstacks/dbrs-memcached-centos8 
  --type=pip \
  --type=rpm \
  --type=file > result_memcached.json
```

or 

```
/usr/local/bin/container-diff analyze -j \
  daemon://ubuntu:18.04 \
  --type=apt > /tmp/result.json
```

2) Once you have the json file with docker image:

```
python html_report.py result_memcached.json report_title
```

it will generate a file:

report_<report_title>.html


