Welcome to DemonHunter's documentation!
=======================================

DemnonHunter is a distributed low interaction honeypot with Agent/Master design.

Agents are honeypots of diffrent protocols and master is where receives attack information and shows to honeypot administrators.

By using DemonHunter you are capable of choosing from various protocol handlers, for example you can choose between Apache(v2.4.18) or Nginx(1.10.0). Handlers are fake and you don't need to install anything extra on your server.

Each Agent is capable of holding more than one protocol. And each master can hold unlimitted count of agents.


Users Guide
==================

.. toctree::
   :maxdepth: 2

   install
   cli
