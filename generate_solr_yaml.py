import yaml

USERCONFIG_FILE = "userconfig.yaml"
OUTPUT_FILE = "solr_instances.yaml"

def load_user_config():
    with open(USERCONFIG_FILE, "r") as f:
        docs = f.read()

    # Handle multiple 'nodes:' blocks by merging manually
    chunks = docs.split("nodes:")
    merged_nodes = []
    final_yaml = {}

    for i, chunk in enumerate(chunks):
        if i == 0:
            # Process everything before the first 'nodes:' block
            final_yaml.update(yaml.safe_load(chunk) or {})
        else:
            try:
                data = yaml.safe_load("nodes:" + chunk)
                if data and "nodes" in data:
                    merged_nodes.extend(data["nodes"])
            except yaml.YAMLError as e:
                print(f"❌ YAML error: {e}")

    final_yaml["nodes"] = merged_nodes
    return final_yaml

def generate_instance_entries(config):
    instances = []
    global_user = config.get("default_ssh", {}).get("ssh_user")
    global_pass = config.get("default_ssh", {}).get("ssh_password")

    for node in config["nodes"]:
        host = node["host"]
        ports = node["ports"]
        paths = node["paths"]
        zone = node.get("zone")
        ssh_user = node.get("ssh_user", global_user)
        ssh_password = node.get("ssh_password", global_pass)

        for port, path in zip(ports, paths):
            instances.append({
                "host": host,
                "port": port,
                "solr_home": path,
                "ssh_user": ssh_user,
                "ssh_password": ssh_password,
                "start_cmd": f"{path}/bin/solr start -p {port}",
                "stop_cmd": f"{path}/bin/solr stop -p {port}",
                "zone": zone
            })
    return {"instances": instances}

def save_yaml(instances):
    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(instances, f, default_flow_style=False)
    print(f"✅ Generated {OUTPUT_FILE} with {len(instances['instances'])} instance(s)")

if __name__ == "__main__":
    config = load_user_config()
    instance_data = generate_instance_entries(config)
    save_yaml(instance_data)

