import json
import docker
client = docker.from_env()

import templator

SERVER_ID = [net.attrs["IPAM"]["Config"][0]["Subnet"] for net in client.networks.list() if net.name == "bridge"][0].split(".")[1]
SERVER_SUBNET = "168" if SERVER_ID == "17" else "169"

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

    con = client.containers.run("kianjones9/ovs:latest", "ovsdb-server", name=f"rack-{rack_id}-ovsdb-server-0", detach=True)

    ip = increment_ip(ip, 3)
    
    RACK_NUM = int(rack_id)
    RACK_ENV_VARS = {"SERVER_ID":SERVER_ID, "SERVER_SUBNET":SERVER_SUBNET, "RACK_NUM":RACK_NUM}
    RACK_ENV_VARS = prepVars(RACK_ENV_VARS)

    ip = increment_ip(ip, 3)
    ovs = client.containers.run("kianjones9/ovs:latest", "ovs-vswitchd",  volumes_from=[f"rack-{rack_id}-ovsdb-server-0"],
                            name=f"rack-{rack_id}-ovs-vswitchd-0", cap_add=["NET_ADMIN"],
                            environment=RACK_ENV_VARS, detach=True)
    ovs.exec_run("bash /config.sh")


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
            
            con.exec_run("bash /config.sh")

    templator.init_rack_network(RACK_ENV_VARS)

    ovs.exec_run("bash /post-startup_config.sh")
    
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

def prepVars(vars: dict):

    vars["APP_SUBNET"] = ".".join(["192", vars["SERVER_SUBNET"], str(vars["RACK_NUM"])])
    vars["MGMT_SUBNET"] = ".".join(["172", vars["SERVER_ID"], str(vars["RACK_NUM"])])
    vars["RACK_ID"] = (3 - len(str(vars["RACK_NUM"]))) * "0" + str(vars["RACK_NUM"])
    return vars