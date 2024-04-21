# Artemis Commit Bot

This bot is created to automatically push empty commits to Artemis until a desired percentage is achieved. Meant for performance testing exercises that are pure server luck. If your code is not sufficiently optimized this will not help you.

It does this by simulating a browser to log into Artemis and read the current percentage. Pushes occure at most only every 10s (if Artemis finished compiling by then) to avoid overloading the server/putting to many build tasks in the queue. 

*This should run on all supported browsers and operating systems, I only tested on Linux and Firefox though.*

## Requirements

- [Python (3.12)](https://www.python.org)
- [Selenium (for python)](https://selenium-python.readthedocs.io/installation.html)
- Browser (Firefox/Chrome/Safari)
- [Selenium driver for your browser](https://selenium-python.readthedocs.io/installation.html#drivers)

## Setup

Create a config.ini file in the root folder of this repo. the config file should contain the following:

```ini
[Auth]
Username=...
Password=...

[Browser]
Browser=Firefox/Chrome/Safari
```

## Usage

Run the Bot using following command:
```bash
$ python bot.py repo_path artemis_url [-p desired_percentage]
```

A help page is also available:
```bash
$ python bot.py -h

usage: bot.py [-h] [-p PERCENTAGE] repo_path artemis_url

Artemis Commit Bot Help

positional arguments:
  repo_path             Path to the repository (locally)
  artemis_url           URL of the Artemis server

options:
  -h, --help            show this help message and exit
  -p PERCENTAGE, --percentage PERCENTAGE
                        Desired percentage (default: 100)
```

## Contact

For any concerns you can contact me here.
