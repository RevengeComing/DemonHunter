# DemonHunter

DemnonHunter is a distributed low interaction honeypot with Agent/Master design.

Agents are honeypots of diffrent protocols and master is where receives attack information and shows to honeypot administrators.

By using DemonHunter you are capable of choosing from various protocol handlers, for example you can choose between Apache(v2.4.18) or Nginx(1.10.0). Handlers are fake and you don't need to install anything extra on your server.

Each Agent is capable of holding more than one protocol. And each master can hold unlimitted count of agents.

![alt text](https://cloud.githubusercontent.com/assets/23046907/26075182/9e23721c-39c9-11e7-87fd-53e9633a02d1.jpg)


## Requirements

DemonHunter is developed under python3.6 and might work on python3.5(testers are welcome to report bugs)

## Documents

I will place documents on http://demonhunter.readthedocs.io

## Installation

For the latest version you can simply install it with pip:
```
$ pip install git+https://github.com/RevengeComing/DemonHunter.git
```
You can also install it from pypi:
```
$ pip install demonhunter
```

## How to run DemonHunter

As i mentioned DemonHunter has 2 sides:
	* Master
	* Agents (Honeypots)

To run Master you can simply execute ```dh_run``` command line interface.
By running dh cli, dh master will run under http://127.0.0.1:8000 + sqlitedb(current_dir/test.db). these are default options for dh_run cli. for changing them run ```dh_run --help``` to have more information on how to change the defaults.

To access DemonHunter's Master interface for first time you can use ```username: admin, password: admin```. After logging in for first time create a user and delete default admin.

## DemonHunter WebMaster Screenshots

![screen_shot1](https://screenshotscdn.firefoxusercontent.com/images/c3e22529-585d-40ad-accd-e70a53b38718.png)
![screen_shot2](https://screenshotscdn.firefoxusercontent.com/images/aa89451e-1a81-432a-8adb-69964bfd0d8b.png)
![screen_shot3](https://screenshotscdn.firefoxusercontent.com/images/9de9a85d-aa0d-480e-9c80-a50f526d907d.png)

## Contribution

I really accept contributions, you can simply open an issue and create a discussion about how DH should move forward.