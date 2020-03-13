#!/bin/bash

container-diff &> /dev/null

if [ $? -eq 0 ]
then
	echo "Successfully installed container-diff"
else
	echo "container-diff need to be installed" >&2
curl -LO https://storage.googleapis.com/container-diff/latest/container-diff-linux-amd64 \
	&& chmod +x container-diff-linux-amd64 \
	&& mkdir -p $HOME/bin \
	&& export PATH=$PATH:$HOME/bin \
	&& mv container-diff-linux-amd64 $HOME/bin/container-diff
fi

