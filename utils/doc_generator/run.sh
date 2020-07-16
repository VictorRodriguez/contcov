#!/bin/bash
/root/bin/container-diff analyze -j -q  $IMG --type=pip --type=rpm --type=apt --type=file > .result.json
python3 html_report.py .result.json $REPORT_TITLE
