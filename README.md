# HGP Joke Crawler

## Setup

### MongoDB
__You will only do this once for the project, during the first-time setup on your machine.__

Run the following in a terminal:
```mongo --quiet init_counters.js```
This will create the sequences collection, which is used by the `exporting.py` to export jokes from the `hgp_crawler` database to the `hgp_webapp` database.

### Python
You must be running Python 2.7 to run this code.

#### Install Dependencies
In a terminal, run the following:
```bash
pip install pymongo --user
```

## Running
To run the crawler once, run the following:
```python reddit_crawler.py```

To run the crawler at an interval, set up a cron job on whichever server/virtual machine this will run on, and have it point to the `run_crawler.sh` script.

## Obtaining the `secrets.json` file
The `reddit_crawler.py` file relies on a file called `secrets.json` which is not published on GitHub because it contains API keys. To obtain the file, check the Georgia Tech GitHub (github.gatech.edu) for the Humor Genome group and obtain it from there. It will most likely be published as a GitHub gist.


Contact:
===========
msakhi3@gatech.edu
