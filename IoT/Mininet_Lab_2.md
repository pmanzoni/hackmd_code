# Mininet Lab 2: bis... SDN
###### tags: `RSE` `Labs`
> https://www.youtube.com/watch?v=FyV4MoQ3T0I


In this part you will manage the flow entries on a Open vSwitch (OVS) manually using the `ovs-ofctl` command (see the [ovs-ofctl man page](http://www.openvswitch.org//support/dist-docs-2.5/ovs-ofctl.8.pdf) also at [openswitch.org](openswitch.org)).
Flow entries on an OpenFlow capable switch control the behaviour of the packets. Normally these flows (or rules) are installed dynamically with an SDN controller

## Basic operations

![](https://i.imgur.com/cpC3z8i.png)

You'll use the network above, created using

    sudo mn --topo=single,3 --controller=none --mac

* `--controller=none`  means that commands will be provided manually
* `--mac`  means that MACs will be simplified

Now execute the `dump` and the `net` commands just to check the topology.

The command to see how switch `s1` ports map to openflow port numbers is:

    mininet> sh ovs-ofctl show s1 

:::	success
**`sh`** allow to execute shell commands inside mininet. You could execute them from a separate xterm 
:::


Le't create the first flow entry:

    mininet> sh ovs-ofctl add-flow s1 action=normal

**`normal`** means traditional switch behaviour, that is the classical switch forwarding operations. Let's test with:

    pingall

:::danger
Cual es el resultado? Todo bien?
:::

Now execute:

    mininet> sh ovs-ofctl dump-flows s1

:::danger
Como intepretas lo que sale en pantalla?
:::

No delete the entry using:

    mininet> sh ovs-ofctl del-flows s1
    
this command deletes all flows in s1. Now execute once again:

    mininet> sh ovs-ofctl dump-flows s1

:::danger
Como intepretas lo que sale en pantalla?
:::

Now execute once again:

    mininet> pingall

:::danger
¿Que obtienes? ¿Por que?
:::


## Using layer 1 data
In this Section we will work at the physical ports level. We want to programme the switch so that everything that comes at the switch s1 from OpenFlow Port 1 has to be sent out to OpenFlow Port 2, and viceversa

![](https://i.imgur.com/CwRlguH.png)

So we have to:

    mininet> sh ovs-ofctl add-flow s1 priority=500,in_port=1,actions=output:2
    mininet> sh ovs-ofctl add-flow s1 priority=500,in_port=2,actions=output:1
    
The two instruction basically indicate the switch that what enters from port 1 has to be forwarded to port2... and viceversa.

:::danger
Ejecuta ahora:
h1 ping -c2 h2 y luego
h3 ping -c2 h2
¿Que obtienes? ¿Hay diferencias... Por que?
:::

Now execute once again:

    mininet> sh ovs-ofctl dump-flows s1

now you can see the newly created flows and the infos about them. The priority value is important. If a packet enters a switch and there are various rules, only the one with higher value is executed.

For example, if you add another flow:

    mininet> sh ovs-ofctl add-flow s1 priority=32768,action=drop

This flow has an higher priority (32768 which corresponds to the defaults value). Priorities ranges between 0 and 65535.

:::danger
Cual es el resultado de añadir este flow? Pueba con `ping`.
:::

Let's now eleiminate such a rule

    mininet> sh ovs-ofctl del-flows s1 --strict
    
deletes the flow with all the default parameters

Try again ping.

==Now delete all the flows in the switch==

### Using layer 2 data

In this section will repeat the same operations but instead of using the port numbers, we will use the MAC addresses of the hosts. Since we execture mininet with the **`--mac option`**, the hosts will have those simplified MAC addresses

![](https://i.imgur.com/IEo15XD.png)

    mininet> sh ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,actions=output:2
    mininet> sh ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,actions=output:1

Try pingall to see if it works. As you will see it doesn't work since in this way we aree filtering out ARP data traffic which is used by pingall to determine the MAC address of the host it is trying to ping.
ARP is a broadcast protocol so we need to add another rule:

    mininet> sh ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,action=flood

We are ccreating a rule that "floods" all Ethernet frames of type 0x806 (ARP) to all the ports of the switch. `nw_proto=1` indicate and ARP request.
The reply in ARP is unicast, so we already have the right flows set

we now obrtain:
    mininet-wifi> pingall
    *** Ping: testing ping reachability
    h1 -> h2 X 
    h2 -> h1 X 
    h3 -> X X 
    *** Results: 66% dropped (2/6 received)

which basically means that now h1 and h2 are in contact but h3 still is disconnected

==Now delete all the flows in the switch==


### Using layer 3 data

![](https://i.imgur.com/VyGhxQQ.png)

We'll now use layer 3 (IP) infos for the creation of flows.
All hosts will talk one to another, and also we will give priority to data coming from h3 using DSCP, that is using DiffServ. 

:::info
Differentiated services or DiffServ is a computer networking architecture that specifies a simple and scalable mechanism for classifying and managing network traffic and providing quality of service (QoS) on modern IP networks. DiffServ can, for example, be used to provide low-latency to critical network traffic such as voice or streaming media while providing simple best-effort service to non-critical services such as web traffic or file transfers.
:::

So we first start by 

    mininet> sh ovs-ofctl add-flow s1 priority=500,dl_type=0x800,nw_src=10.0.0.0/24,nw_dst=10.0.0.0/24,actions=normal
    mininet> sh ovs-ofctl add-flow s1 priority=800,dl_type=0x800,nw_src=10.0.0.3,nw_dst=10.0.0.0/24,actions=mod_nw_tos:184,normal
    

:::danger
Describe que hacen estas dos lineas de configuracion.
:::

We use 184 to specify the 46 value becuase the TOS fields because we have to shift them 2 bits on the left according to the usegae of the bits of field s of Tos in the IP packet
in Openflow there are many various rules to modify pacekt contents. Here we are simply seeing the basic ones.

Now we have to again enable ARP. We'll do it in a slsightly different way:

    mininet> sh ovs-ofctl add-flow s1 arp,nw_dst=10.0.0.1,actions=output:1
    mininet> sh ovs-ofctl add-flow s1 arp,nw_dst=10.0.0.2,actions=output:2
    mininet> sh ovs-ofctl add-flow s1 arp,nw_dst=10.0.0.3,actions=output:3

in this case we are not flooding, which can be a useful behaviour (imagine a 24 ports switch)

:::danger
Prueba ahora si funciona con `pingall`. Comprueba con wireshark si efectivamente el DSCP se modifica en los paquete hacia o desde h3
:::

==Now delete all the flows in the switch==


### Using layer 4 data

To concluede we'll see how the same can be done at layer 4, the application layer. In this example a simple pythone web server (the one you used in a previos session) will be executed in host 3, and host 1 and host 2 will connect to that server that runs at port 80.

![](https://i.imgur.com/Siw5wq5.png)

So let's start the web server on h3

    mininet> h3 python -m SimpleHTTPServer 80 &
    
Let's enable ARP (in a simplker way):

    mininet> sh ovs-ofctl add-flow s1 arp,actions=normal

Let's enable TCP traffic (nw_proto=6) to port 80

    mininet> sh ovs-ofctl add-flow s1 priority=500,dl_type=0x800,nw_proto=6,tp_dst=80,actions=output:3
    
All the traffic for port 80 is sent to port 3. This rule ecould be used to redirect all the data traffic to a firewall
    
To allow for return traffic, we have to:

    mininet> sh ovs-ofctl add-flow s1 priority=800,ip,nw_src=10.0.0.3,actions=normal
    
:::danger
Que hace exactamente esta ultima regla
:::

    
To check whether eveything works, try:

    mninet> h1 curl h3
    
    
---