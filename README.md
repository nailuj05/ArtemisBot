# Artemis Commit Bot

This bot is created to automatically commit and push to Artemis until a desired percentage is achieved.

## Requirements

- (Python)[www.python.org]
- (Selenium)[https://selenium-python.readthedocs.io/installation.html]
- Browser (Firefox/Chrome/Safari)
- (Selenium driver for your browser)[https://selenium-python.readthedocs.io/installation.html#drivers]

## Setup

Create a config.ini file in the root folder of this repo. the config file should contain the following:

```ini
[Auth]
Username=...
Password=...

[Browser]
Browser=Firefox/Chrome/Safari
PathToDriver=Path to your Selenium driver installation
```

