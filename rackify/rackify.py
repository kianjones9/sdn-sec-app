import json
import docker
client = docker.from_env()

SERVER_ID = [net.attrs["IPAM"]["Config"][0]["Subnet"] for net in client.networks.list() if net.name == "bridge"][0].split(".")[1]

def increment_ip(ip, octet_to_inc):
    
    split = ip.split(".")
    octet = int(split[octet_to_inc]) + 1
    split[octet_to_inc] = str(octet)
    ip = ".".join(split)
    
    return ip

def create_rack(rack_config, ip):
    
    # Generate container network IP scheme
    sub = ip
    ip = ip + "10"

    pool = docker.types.IPAMPool(
        subnet=sub+"/24",
        gateway=ip
    )
    
    ipam = docker.types.IPAMConfig(
        pool_configs=[pool]
    )


    # Generate rack-id
    rack_id = ip.split(".")[-2]
    rack_id = "0" * max(3 - len(rack_id), 0) + rack_id

    print("Creating rack with rack id: " + rack_id)

    
    # run and connect OVS containers
    net = client.networks.create(name="rack-"+rack_id, ipam=ipam)

    con = client.containers.run("kianjones9/ovs:latest", "ovsdb-server", name=f"rack-{rack_id}-ovsdb-server-1", detach=True)

    ip = increment_ip(ip, 3)
    net.connect(con.id, ipv4_address=ip)
    
    RACK_NUM = int(rack_id)
    print(RACK_NUM)

    ip = increment_ip(ip, 3)
    con = client.containers.run("kianjones9/ovs:latest", "ovs-vswitchd",  volumes_from=[f"rack-{rack_id}-ovsdb-server-1"],
                            name=f"rack-{rack_id}-ovs-vswitchd-1", cap_add=["NET_ADMIN"], environment={"SERVER_ID":SERVER_ID, "RACK_NUM":RACK_NUM},
                            detach=True)
    con.exec_run("bash /config.sh")
    net.connect(con.id, ipv4_address=ip)


    # Run and connect the rest of the applications in the rack 

    for app in rack_config:
        
        print(f"Starting {app['replicas']} container(s) of {app['app']}")
        
        for i in range(app["replicas"]):
            
            ip = increment_ip(ip, 3)

            if app["app_name"] == "blog":
                
                db_addr = app["args"]["environment"]["BLOG_MYSQL_HOST"]
                
                db_addr = db_addr.split(".")
                db_addr[2] = rack_id # a.b.2.d -> a.b.2.d
                db_addr[3] = ip.split(".")[-1] # a.b.c.13 -> a.b.c.13
                db_addr = ".".join(db_addr)

                app["args"]["environment"]["BLOG_MYSQL_HOST"] = db_addr
            
            con = client.containers.run(app["app"], name=f"rack-{rack_id}-{app['app_name']}-{i}", cap_add=["NET_ADMIN"], detach=True, **app["args"])
            net.connect(con.id, ipv4_address=ip)
            con.exec_run("bash /config.sh")

    print(f"Rack {rack_id} created")



def create(filename):

    # read in config file
    f = open(filename, "r")
    config = json.load(f)

    # parse config
    topo = config["topology"]
    net = topo["first_subnet"]

    # For the number f rack requested
    for i in range(topo["rack_replicas"]):

        # Create rack with parameters from rack_config using subnet net
        create_rack(topo["rack_config"], net)
        
        # increment third octet of subnet used (i.e. next subnet for next rack)
        net = increment_ip(net, 2)


def delete(filter):

    cons = client.containers.list(filters={"name":filter})

    [con.kill() for con in cons]
    client.containers.prune()
    client.networks.prune()
