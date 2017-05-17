# DemonHunter

If you want to create low interaction Honepot servers and their agents, plus a manager to check logs, in less than an hour, you should follow this repository.

DemonHunter allows you to create your honeynet all costumized by yourself, from ports to protocol handlers.
For example you want to have http protocol, you can have nginx 1.10.0 honeypot or apache 2.4.18 or maybe IIS ?
For example you want to have telnet protocol, you can have Microsoft Telnet Service honeypot or Debian GNU Linux honeypot ?
Or maybe you want to run a honeypot(any protocol) on another port ?
Maybe you want your honeypot work as Agent and send data to another server ?

We support them all!

![alt text](https://cloud.githubusercontent.com/assets/23046907/26075182/9e23721c-39c9-11e7-87fd-53e9633a02d1.jpg)


## Requirements
Python 3.5

## Installation

For the latest version
```
$ pip install git+https://github.com/RevengeComing/DemonHunter.git
```
For stable version
```
$ pip install demonhunter
```

## Want a Demo ?

To run a demo run dh_test in command line after demonhunter installation
```
$ dh_test
```

## Documentation

check [Here](https://revengecoming.github.io/DemonHunter/) , i'll place all docs here.

## Contribution

I will be glad to have a contributor on protocols. or maybe bugfixes and/or suggests on how it should work.
