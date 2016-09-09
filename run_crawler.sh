#!/bin/sh -eu

TO_HERE="${BASH_SOURCE[0]}";
THIS_FILE=$(basename $TO_HERE)

TO_THIS_DIR=${TO_HERE%$THIS_FILE}

cd $TO_THIS_DIR

echo $(date) >> log_crawler.log
python reddit_crawler.py >> log_crawler.log

echo $(date) >> log_exports.log
python export_jokes.py >> log_exports.log
