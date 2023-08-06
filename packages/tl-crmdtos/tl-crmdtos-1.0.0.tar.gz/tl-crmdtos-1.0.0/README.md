## Cloudless Resource Management Data Transfer Objects

List of Data Transfer Objects that:
- are encapsulated in UDP packets and transferred back and forth between workers and collector in the generation layer 
- are exchanged within between modules inside either worker or collector

### List of DTOs

#### Internal objects
- `PortInfo`: a pair of (daemon_name,port_number) showing that a daemon can receive packets at certain port, and is encapsulated in `HostInfo` object.
   
   Ex: **collectord:9090** => **collectord** service is listening at port **9090** 
    
- `HostType`: enum class, label of host used to identify which kind that host is and is encapsulated in `HostInfo` object.
    
   Ex: **WORKER** => worker host; **COLLECTOR** => collector host.
    
- `HostInfo`: information of a single host (collector or worker) that will be sent to other host by encapsulated in `ProbeInit` or `ProbeAck` object.
   
   Ex: 
   ```
   COLLECTOR-collector[10.0.0.2] - ports: [coordinatord:10100, collectord:9090]
   ```
   => hostname: **collector**; ip_address: **10.0.0.2**, 2 daemons: **collectord** listening at port **9090** & **coordinatord** listening at port **10100**; host_type: **COLLECTOR**
   
- `CrmPktType`: enum class, label of packet used to identify which kind that data inside a UDP segment is and is encapsulated in `ProbeInit`, `ProbeAck`, or `RegisterAck` object/packet.
   
   Ex: **PROBE_INIT** => UDP packet of type **ProbeInit**; **PROBE_ACK** => UDP packet of type **ProbeAck**; **REG_ACK** => UDP packet of type **RegisterAck** packet.
   
- `RegisterInfo`: information regarding the creation of metric exporters in worker host and is encapsulated in `RegisterAck` object/packet.

   Ex:
   ```
   True - ('Successfully registered at collector host.',) - max remaining retries: 0
   ```
   => status: **True**; message: 'Successfully registered to collector host.'; max_retries: **0**
   ```
   False - ('Failed to register at collector host.',) - max remaining retries: 3
   ```
   => status: **False**; message: 'Failed to register to collector host.'; max_retries: **3**
   
#### Application layer PDU
- `ProbeInit`: broadcasted by collector host (in fixed interval) to all worker host within current subnet.
    
   Ex:
   ```
   {"py/object": "dtos.probe_init.ProbeInit", "id": "78f6ac6d-ec8d-44cf-abc8-584e4255e9d3", "info": {"py/object": "dtos.host_info.HostInfo", "hostname": "collector", "inet_addr": "10.0.0.2", "ports": [{"py/object": "dtos.port_info.PortInfo", "daemon": "coordinatord", "port": 10100}, {"py/object": "dtos.port_info.PortInfo", "daemon": "collectord", "port": 9090}], "type": {"py/reduce": [{"py/type": "dtos.host_type.HostType"}, {"py/tuple": [2]}]}}, "type": {"py/reduce": [{"py/type": "dtos.crm_pkt_type.CrmPktType"}, {"py/tuple": [1]}]}}
   ```
   => object: ProbeInit; packet-id: 78f6ac6d-ec8d-44cf-abc8-584e4255e9d3; HostInfo: hostname=collector, inet_addr=10.0.0.2

- `ProbeAck`:  sent by worker host as reply to `ProbeInit` packet of collector host

   Ex:
   ```
   
   ```
- `RegisterAck`:

#### Versions:
- `2.1.x`: with QueryAck
- `3.x.x`: without QueryAck