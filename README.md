Running Minecraft "Open to LAN" on a stable port
====

This is ...
---
- A quick and dirty hacked proof of concept.
- NOT production ready for ANYTHING.
- Totally insecure and very likely to get you in trouble because of hackers using this to get into your network.
- JUST to show the idea.

What is the problem?
---
If you run Minecraft on your local machine and open it to LAN other people in your LAN can join the game and you can play together.

This is very cool, but what if your friend wants to join in and he lives in a different network?

The main problem here is that minecraft uses a random TCP port number to host the local server on.

So a simple port forward in your router would need to be setup everytime you start the server because both IP and port will have changed.

The real solution is to setup a minecraft server where you can simply specifiy the port number.

This is an experiment to see if a server is really needed.

The 'nicest' solution for this is if the Minecraft client would have a config setting where you can specify the port on which the  
"open to lan" server should run on...  but that is not there.


What is the idea?
---
When a minecraft "Open to lan" is run it sends out multicast messages indicating the IP and port on which the Minecraft server is running.

The idea is listening to those messages and based on those messages setup a proxy that forwards a fixed IP and port towards the real server.

The current code POC is intended to run locally on the same machine as where the Minecraft is running ... which has to be a Linux based system.

So what happens here is 

1. Listen to the multicast messages.
2. If a change in the open to lan port is detected generate a new haproxy config file.
3. On change of the config file restart haproxy.
 
The only requirement now is that the system on which Minecraft is run gets a fixed IP from the router.

So now you can setup a permanent port forwarding from the outside to the system running Minecraft and you can open to lan your minecraft server .... which will open it to the entire planet ...

If you want to put this on a server in your home beware that if you open 2 or more minecrafts to lan this setup completely breaks down.

License
=======

    Copyright (C) 2020 Niels Basjes

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

