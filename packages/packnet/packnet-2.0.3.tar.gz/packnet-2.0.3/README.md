# PACKNET
*Hacked together into entirety by c0mplh4cks*

____


## About

This package is created to build low-level networking packets which can be used when building various types of applications. Using this package, it is possible to make packets ranging from OSI model level 2 to level 7. One of the endless applications could be a network device discovery tool using the address resolution protocol for example. Apart from only building numerous headers and payloads, this package makes it also possible to read received data and extract useful information, making it possible to interact with a Python script.


____


## Table of Contents
* [OSI model](#osi-model)
* [Protocols](#protocols)
  * Layer 2
    1. [Ethernet](#ethernet-protocol)
  * Layer 3
    1. [ARP](#arp-protocol)
    1. [IPv4](#ipv4-protocol)
    1. [IPv6 ](#ipv6-protocol)
    1. [ICMP](#icmp-protocol)
    1. [ICMPv6](#icmpv6-protocol)
  * Layer 4
    1. [UDP](#udp-protocol)
    1. [TCP](#tcp-protocol)
  * Layer 7
    1. [DNS](#dns-protocol)
    1. [MQTT](#mqtt-protocol)
* [Installation](#installation)
  1. [PyPi](#installation-from-pypi)
  1. [GitHub](#installation-from-github)
* [Importing packnet](#import)
* [Building packets](#building)
  1. [ARP request](#arp-request-encode)
  1. [TCP message](#tcp-message-encode)
  1. [UDP message](#udp-message-encode)
  1. [DNS query](#dns-query-encode)
* [Reading packets](#reading)
  1. [ARP](#arp-decode)
  1. [TCP](#tcp-decode)
  1. [DNS](#dns-decode)
* [Interface](#interface)


____


## OSI model

Open Systems Interconnection model


No | Layer        | Function                    | Protocol *(included in package)*
---|--------------|-----------------------------|------------------------------
7  | Application  | Application communication   | DNS, MQTT
6  | Presentation | Representation & Encryption |
5  | Session      | Interhost communication     |
4  | Transport    | Connections & QoS           | TCP, UDP
3  | Network      | IP                          | IPv4, IPv6, ICMP, ICMPv6, ARP
2  | Data Link    | MAC                         | Ethernet
1  | Physical     | Bits                        |


Introduced to standardize networking protocols, allowing multiple networking devices from different developers to communicate among each other. The model consists of multiple layers with its own functions. The OSI model differs from the TCP/IP model since it has the presentation and session layers.


____


## Protocols

An explanation of the datagrams for each protocol included in this package. Every protocol described here contains a table with the contents of the protocols datagram in order. The tables contain the length of the data in bits and bytes, a description and a type field. The type field explains in which type the data must be set when used in Python.


____


### Ethernet protocol

Ethernet makes part of the data link layer.

* #### Header

  Bits | Bytes | Data                    | Type | Description
  -----|-------|-------------------------|------|------------
  48   | 6     | Destination MAC Address | str  | destination MAC address
  48   | 6     | Source MAC Address      | str  | source MAC address
  16   | 2     | Protocol                | int  | each layer 3 packet has its own protocol value


____


### ARP protocol

ARP makes part of the network layer.

* #### Header

  Bits | Bytes | Data                    | Type | Description
  -----|-------|-------------------------|------|------------
  16   | 2     | Hardware Type           | int  | type of hardware address
  16   | 2     | Protocol Type           | int  | type of protocol address
  8    | 1     | Hardware Size           | int  | size of hardware address
  8    | 1     | Protocol Size           | int  | size of protocol address
  16   | 2     | Operation Code          | int  | 1 for request, 2 for response
  48   | 6     | Source MAC Address      | str  | source MAC address
  32   | 4     | Source IP Address       | str  | source IP address
  48   | 6     | Destination MAC Address | str  | destination MAC address
  32   | 4     | Destination IP Address  | str  | destination IP address


____


### IPv4 protocol

IPv4 makes part of the network layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  4    | -     | Version                      | int  | version of IP
  4    | -     | Header length                | int  | length of ipv4 header
  8    | 1     | Differentiated Service Field | int  | differentiated service field
  16   | 2     | Total length                 | int  | total length of packet
  16   | 2     | ID                           | int  | identifier for IPv4 packet
  16   | 2     | Flags                        | int  | flags
  8    | 1     | TTL                          | int  | time to live
  8    | 1     | Protocol                     | int  | protocol of following header
  16   | 2     | Checksum                     | int  | for calculating errors
  32   | 4     | Source IP Address            | str  | source IP address
  32   | 4     | Destination IP Address       | str  | destination IP address


____


### IPv6 protocol

IPv6 makes part of the network layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  4    | -     | Version                      | int  | version of IP
  8    | 1     | Traffic class                | int  | traffic class
  20   | -     | Flow label                   | int  | flow label
  16   | 2     | Payload length               | int  | length of payload
  8    | 1     | Next header                  | int  | type identifier of next header
  8    | 1     | Hop limit                    | int  | hop limit
  126  | 16    | Source IPv6 Address          | str  | source IPv6 address
  126  | 16    | Destination IPv6 Address     | str  | destination IPv6 address


____


### ICMP protocol

ICMP makes part of the network layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  8    | 1     | Type                         | int  | type
  8    | 1     | Code                         | int  | subtype
  16   | 2     | Checksum                     | -    | for calculating errors


* #### Echo

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | ID                           | int  | echo identifier
  16   | 2     | Sequence Number              | int  | sequence number
  64   | 8     | Timestamp                    | int  | timestamp
  \>0  | >0    | Payload                      | bstr | payload (variable size)


* #### TimeExceeded

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  32   | 4     | Unused                       | -    | unused
  \>160| >20  | Data                         | bstr | IPv4 Header & ICMP Header


____


### ICMPv6 protocol

ICMPv6 makes part of the network layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  8    | 1     | Type                         | int  | type
  8    | 1     | Code                         | int  | subtype
  16   | 2     | Checksum                     | int  | for calculating errors


* #### Echo

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | ID                           | int  | echo identifier
  16   | 2     | Sequence Number              | int  | sequence number
  \>0  | >0    | Payload                      | bstr | payload (variable size)


____


### UDP protocol

UDP makes part of the transport layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | Source PORT                  | int  | source port
  16   | 2     | Destination PORT             | int  | destination port
  16   | 2     | Total length                 | int  | total length of header & payload
  16   | 2     | Checksum                     | -    | for calculating errors


____


### TCP protocol

TCP makes part of the transport layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | Source PORT                  | int  | source port
  16   | 2     | Destination PORT             | int  | destination port
  32   | 4     | Sequence number              | int  | sequence number
  32   | 4     | Acknowledgement number       | int  | acknowledgment number
  4    | -     | Header length                | int  | length of header
  12   | -     | Flags                        | int  | flags
  16   | 2     | Window size                  | int  | size of window
  16   | 2     | Checksum                     | int  | for calculating errors
  16   | 2     | Urgent pointer               | int  | urgent pointer
  \>0  | >0    | Options                      | obj  | options


____


### DNS protocol

DNS makes part of the application layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | ID                           | int  | echo identifier
  16   | 2     | Flags                        | int  | flags
  16   | 2     | Questions                    | int  | amount of questions
  16   | 2     | Answer RRs                   | int  | amount of answer RRs
  16   | 2     | Authority RRs                | int  | amount of authority RRs
  16   | 2     | Additional RRs               | int  | amount of additional RRs


* #### Query

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  \>8  | >1    | Name                         | str  | name in question
  16   | 2     | Type                         | int  | name type
  16   | 2     | Class                        | int  | name class


* #### Answer

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  \>8  | >1    | Name                         | str  | name in question
  16   | 2     | Type                         | int  | cname type
  16   | 2     | Class                        | int  | cname class
  32   | 4     | Time To Live                 | int  | time to live for answer
  16   | 2     | Length                       | int  | total length of answer
  \>8  | >1    | Cname                        | str  | answer on question


____


### MQTT protocol

MQTT makes part of the application layer.

* #### Header

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  8    | 1     | Flags                        | int  | flags
  8    | 1     | Payload length               | int  | length of payload


* #### Connect

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | Protocol length              | int  | length of protocol
  \>0  | >0    | Protocol                     | str  | protocol
  8    | 1     | Version                      | int  | version
  8    | 1     | Flags                        | int  | flags
  16   | 2     | Keep alive                   | int  | keep alive
  16   | 2     | ID length                    | int  | length of identifier
  \>0  | >0    | ID                           | str  | identifier


* #### ConnectACK

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  8    | 1     | Flags                        | int  | flags  
  8    | 1     | Return code                  | int  | return code


* #### Subscribe

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | Message ID                   | int  | identifier of message
  16   | 2     | Topic length                 | int  | length of topic
  \>0  | >0    | Topic                        | str  | topic
  8    | 1     | Requested QoS                | int  | requested type of QoS


* #### SubscribeACK

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | Message ID                   | int  | identifier of message
  8    | 1     | Granted QoS                  | int  | granted type of QoS


* #### Publish

  Bits | Bytes | Data                         | Type | Description
  -----|-------|------------------------------|------|------------
  16   | 2     | Topic length                 | int  | length of topic
  \>0  | >0    | Topic                        | str  | topic
  \>0  | >0    | Message                      | str  | message




____


## Installation

The following will show how this package can be installed.


### Installation from PyPi

Install package by using `pip`:
```
pip3 install packnet
```
or
```
pip install packnet
```


### Installation from Github

Clone the repository:
```
git clone https://github.com/c0mplh4cks/packnet
```

Move inside the directory:
```
cd packnet
```

Install the library by running the following command:
```
pip3 install .
```


____


## Import

Packages can be imported using different methods in Python. The following examples will show how this package can be imported and used in numerous ways.  
*(Note that the first and third examples are preferred)*
```python
import packnet  # Imports everything inside the package.

packnet.standards.maclookup("00:00:00:00:00:00")
packnet.standards.encode.ip("127.0.0.1")
interface = packnet.Interface()
ethernet_header = packnet.ETHERNET.Header()
dns_query = packnet.DNS.Query()
```

```python
from packnet import * # Imports everything inside the package. NOT RECOMMENDED!

standards.maclookup("00:00:00:00:00:00")
standards.encode.ip("127.0.0.1")
interface = Interface()
ethernet_header = ETHERNET.Header()
dns_query = DNS.Query()
```

```python
from packnet import standards, Interface, ETHERNET, DNS   # Imports specific modules/objects/functions from package.

standards.maclookup("00:00:00:00:00:00")
standards.encode.ip("127.0.0.1")
interface = Interface()
ethernet_header = ETHERNET.Header()
dns_query = DNS.Query()
```


____


## Building

The following snippets of code will serve as an example when building different types of packets.


### ARP request encode

```python
from packnet import ETHERNET, ARP   # importing ETHERNET and ARP objects


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]


arp = ARP.Header()    # defining ARP Header object
arp.src = src         # setting source address
arp.dst = dst         # setting destination address
arp.op = 1            # setting operation code to 1(request)
arp.build()           # building ARP Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0806    # setting protocol 0x0806(ARP)
ethernet.data = arp.packet    # adding ARP Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build ARP request including ethernet header
```


### TCP message encode

```python
from packnet import ETHERNET, IPv4, TCP


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]

msg = "hello".encode()      # defining TCP payload

tcp = TCP.Header()    # defining TCP Header object
tcp.src = src         # setting source address
tcp.dst = dst         # setting destination address
tcp.seq = 1234        # setting sequence number
tcp.ack = 4321        # setting acknowledgment number
tcp.data = msg        # setting payload
tcp.build()           # building TCP Header

ipv4 = IPv4.Header()    # defining IPv4 Header object
ipv4.src = src          # setting source address
ipv4.dst = dst          # setting destination address
ipv4.id = 31415         # setting identifier
ipv4.protocol = 6       # setting protocol 6(TCP)
ipv4.data = tcp.packet  # adding TCP Header
ipv4.build()            # building IPv4 Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0800    # setting protocol 0x0800(IPv4)
ethernet.data = ipv4.packet   # adding IPv4 Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build UDP packet including IPv4 and ETHERNET headers
```


### UDP message encode

```python
from packnet import ETHERNET, IPv4, UDP


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]

msg = "hello".encode()      # defining UDP payload


udp = UDP.Header()    # defining UDP Header object
udp.src = src         # setting source address
udp.dst = dst         # setting destination address
udp.data = msg        # setting payload
udp.build()           # building UDP Header

ipv4 = IPv4.Header()    # defining IPv4 Header object
ipv4.src = src          # setting source address
ipv4.dst = dst          # setting destination address
ipv4.id = 1234          # setting identifier
ipv4.protocol = 17      # setting protocol 17(UDP)
ipv4.data = udp.packet  # adding UDP Header
ipv4.build()            # building IPv4 Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0800    # setting protocol 0x0800(IPv4)
ethernet.data = ipv4.packet   # adding IPv4 Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build UDP packet including IPv4 and ETHERNET headers

```


### DNS query encode

```python
from packnet import ETHERNET, IPv4, UDP, DNS


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]


query = DNS.Query()         # defining DNS Query object
query.name = "github.com"   # setting name to be resolved

dns = DNS.Header()          # defining DNS Header object
dns.id = 1234               # setting identifier
dns.question.append(query)  # adding query to header
dns.build()                 # building DNS Header

udp = UDP.Header()      # defining UDP Header object
udp.src = src           # setting source address
udp.dst = dst           # setting destination address
udp.data = dns.packet   # adding DNS Header
udp.build()             # building UDP Header

ipv4 = IPv4.Header()    # defining IPv4 Header object
ipv4.src = src          # setting source address
ipv4.dst = dst          # setting destination address
ipv4.protocol = 17      # setting protocol 17(UDP)
ipv4.data = udp.packet  # adding UDP Header
ipv4.build()            # building IPv4 Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0800    # setting protocol 0x0800(IPv4)
ethernet.data = ipv4.packet   # adding IPv4 Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build UDP packet including IPv4 and ETHERNET headers
```


____


## Reading

The following snippets of code will serve as an example when reading various types of packets and requiring the information.


### ARP decode

```python
from packnet import ETHERNET, ARP


packet = b'""""""\x11\x11\x11\x11\x11\x11\x08\x06\x00\x01\x08\x00\x06\x04\x00\x02\x11\x11\x11\x11\x11\x11\x01\x01\x01\x01""""""\x02\x02\x02\x02'
# ^ packet which must be decoded


ethernet = ETHERNET.Header(packet)    # defining ETHERNET Header object & parsing encoded packet
ethernet.read()                       # reading ETHERNET Header

print( "ETHERNET HEADER" )            # displaying acquired data
print( f" length   { ethernet.length }" )
print( f" source   { ethernet.src }" )
print( f" target   { ethernet.dst }" )
print( f" protocol { ethernet.protocol }" )
print()


if ethernet.protocol == 0x0806:     # check if packet contains an ARP Header
  arp = ARP.Header(ethernet.data)   # defining ARP Header object & parsing encoded data
  arp.read()                        # reading ARP Header

  print( "ARP HEADER" )             # displaying acquired data
  print( f" length    { arp.length }" )
  print( f" source    { arp.src }" )
  print( f" target    { arp.dst }" )
  print( f" operation { arp.op }" )
  print()
```


### TCP decode

```python
from packnet import ETHERNET, IPv4, TCP


packet = b'""""""\x11\x11\x11\x11\x11\x11\x08\x00E\x00\x00(z\xb7@\x00@\x06\xba\x13\x01\x01\x01\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x04\xd2\x00\x00\x10\xe1P\x00\xfd\xe8\x96C\x00\x00hello'
# ^ packet which must be decoded


ethernet = ETHERNET.Header(packet)    # defining ETHERNET Header object & parsing encoded packet
ethernet.read()                       # reading ETHERNET Header

print( "ETHERNET HEADER" )            # displaying acquired data
print( f" length   { ethernet.length }" )
print( f" source   { ethernet.src }" )
print( f" target   { ethernet.dst }" )
print( f" protocol { ethernet.protocol }" )
print()


if ethernet.protocol == 0x0800:     # check if packet contains an IPv4 Header
  ipv4 = IPv4.Header(ethernet.data) # defining IPv4 Header object & parsing encoded data
  ipv4.read()                       # reading IPv4 Header

  print( "IPv4 HEADER" )            # displaying acquired data
  print( f" length   { ipv4.length }" )
  print( f" source   { ipv4.src }" )
  print( f" target   { ipv4.dst }" )
  print( f" id       { ipv4.id }" )
  print( f" protocol { ipv4.protocol }" )
  print()


  if ipv4.protocol == 6:          # check if packet contains an TCP Header
    tcp = TCP.Header(ipv4.data)   # defining TCP Header object & parsing encoded data
    tcp.read()                    # reading TCP Header

    print( "TCP HEADER" )         # displaying acquired data
    print( f" length                 { tcp.length }" )
    print( f" source                 { tcp.src }" )
    print( f" target                 { tcp.dst }" )
    print( f" sequence number        { tcp.seq }" )
    print( f" acknowledgement number { tcp.ack }" )
    for option in tcp.options:
      print( f" option kind { option.kind }" )
    print( f"data { tcp.data }" )
    print()

```


### DNS decode

```python
from packnet import ETHERNET, IPv4, UDP, DNS


packet = b'""""""\x11\x11\x11\x11\x11\x11\x08\x00E\x00\x008\x00\x00@\x00@\x114\xb0\x01\x01\x01\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00$\xe9\xc3\x04\xd2\x00@\x00\x01\x00\x00\x00\x00\x00\x00\x06github\x03com\x00\x00\x05\x00\x01'
# ^ packet which must be decoded


ethernet = ETHERNET.Header(packet)    # defining ETHERNET Header object & parsing encoded packet
ethernet.read()                       # reading ETHERNET Header

print( "ETHERNET HEADER" )            # displaying acquired data
print( f" length   { ethernet.length }" )
print( f" source   { ethernet.src }" )
print( f" target   { ethernet.dst }" )
print( f" protocol { ethernet.protocol }" )
print()


if ethernet.protocol == 0x0800:     # check if packet contains an IPv4 Header
  ipv4 = IPv4.Header(ethernet.data) # defining IPv4 Header object & parsing encoded data
  ipv4.read()                       # reading IPv4 Header

  print( "IPv4 HEADER" )            # displaying acquired data
  print( f"length    { ipv4.length }" )
  print( f" source   { ipv4.src }" )
  print( f" target   { ipv4.dst }" )
  print( f" protocol { ipv4.protocol }" )
  print( f" id       { ipv4.id }" )
  print()


  if ipv4.protocol == 17:         # check if packet contains an UDP Header
    udp = UDP.Header(ipv4.data)   # defining UDP Header object & parsing encoded data
    udp.read()                    # reading UDP Header

    print( "UDP HEADER" )         # displaying acquired data
    print( f" length { udp.length }" )
    print( f" source { udp.src }" )
    print( f" target { udp.dst }" )
    print()


    dns = DNS.Header(udp.data)  # defining DNS Header object & parsing encoded data
    dns.read()                  # reading DNS Header

    print( "DNS HEADER" )         # displaying acquired data
    print( f" id { dns.id }" )
    print( f" questions      { len(dns.question) }" )
    print( f" answer RRs     { len(dns.answer) }" )
    print( f" authority RRs  { len(dns.authority) }" )
    print( f" additional RRs { len(dns.additional) }" )
    print()

    for question in dns.question:
      print( "DNS QUERY" )         # displaying acquired data
      print( f"name   { question.name }" )
      print( f"type   { question.type }" )
      print( f"classs { question.classif }" )
      print()

    for answer in dns.answer:
      print( "DNS ANSWER" )         # displaying acquired data
      print( f"name   { answer.name }" )
      print( f"type   { answer.type }" )
      print( f"classs { answer.classif }" )
      print( f"ttl    { answer.ttl }" )
      print( f"cname  { answer.cname }" )
      print()
```


____


## Interface

Interface is a special module which can be used for creating low-level sockets and automatically requiring address information from the specified interface. Below an example from an use case.  
**Requires `sudo` rights!**

```python
from packnet import Interface


interface = Interface(card="eth0", port=0, passive=False)

print(interface.addr)

interface.send(b"hello")
print(interface.recv())
```
