# Ceph Learning
Adventures in learning how Ceph works.

## General notes
- Overall thing: Ceph Storage Cluster
  - Required: OSD, Monitor, and Manager
    - Metadata server (MSD) is optional
  - Monitor - maintains the cluster state through a series of maps
    - also responsible for auth between daemons and clients
    - at least three monitors are required for high availability
  - Manager - Keeps track of cluster metrics and state
    - hosts frontends for cluster information
      - REST API
      - Ceph dashboard
    - At least two managers are required for HA
  - OSD (object storage daemon) - does data storage and replication stuff
    - at least three are required for HA (three total)
  - MDS (metadata server) - stores metadata for the ceph filesystem
    - takes some of the load off the storage cluster for common commands

## Hardware requirements
- CPU requirements
  - metadata servers should have significant processor power
  - OSDs don't need quite as much processing power as MDS
  - monitors require the least amount of compute
  - other CPU-intensive processes should be run on separate hosts
    - openstack nova hosts shouldn't share with OSDs or MDSs
- RAM requirements
  - monitors and managers scale with cluster size
    - 1-2 GB for small clusters
    - 5-10+ for larger clusters
  - MDSs - depends on how much cache is configured to consume
    - 1 GB is a general minimum
  - OSDs with Bluestore backend - 3-5 GB of RAM each
- disks - pretty much what you would expect about SSD vs HDD
- network
  - should have a backend 10G network for cluster traffic
  - 1G "public" network for non-storage traffic
  - IPMI should be on a third separate network

## Other stuff
- Placement groups (PGs) are used to distribute objects among OSDs
  - object copies need to be redundantly stored
    - too computationally intensive for objects to be individually copied
  - objects are put in PGs, and each PG is stored over multiple OSDs
    - objects are stored in PGs based on a hash of their OBJ ID
    - PGs are sort of like hash maps for objects