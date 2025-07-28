import yaml
import paramiko
from typing import Optional

# Load Solr Instances
def load_instances(file_path='solr_instances.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data['instances']

def get_instance(instances, host: str, port: int):
    for inst in instances:
        if inst['host'] == host and inst['port'] == port:
            return inst
    return None

# Run Command on Remote Host via SSH
def run_ssh_command(host, command, user='root', password: Optional[str] = None):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if password:
            ssh.connect(hostname=host, username=user, password=password)
        else:
            ssh.connect(hostname=host, username=user)

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()

        return output if output else error

    except Exception as e:
        return f"❌ SSH Error on {host}: {str(e)}"

# Start / Stop / Restart Logic
def run_action(action: str, instance: dict):
    ssh_user = instance.get("ssh_user", "root")
    ssh_pass = instance.get("ssh_password")
    cmd = instance.get(f"{action}_cmd")
    if not cmd:
        return f"❌ No {action}_cmd defined for {instance['host']}:{instance['port']}"
    return run_ssh_command(instance['host'], cmd, ssh_user, ssh_pass)

def restart_instance(host: str, port: int, instances_file='solr_instances.yaml'):
    instances = load_instances(instances_file)
    instance = get_instance(instances, host, port)
    if not instance:
        return f"❌ Instance not found for host={host}, port={port}"

    logs = []
    logs.append(run_action("stop", instance))
    logs.append("--- Restart Wait Done ---")
    logs.append(run_action("start", instance))
    return "\n".join(logs)

