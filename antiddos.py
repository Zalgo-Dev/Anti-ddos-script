import os
import subprocess

def run_command(command):
    """Helper function to run a shell command"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

# Update packages
print("Updating packages...")
run_command("sudo apt update && sudo apt upgrade -y")

# Install iptables and fail2ban
print("Installing iptables and fail2ban...")
run_command("sudo apt install -y iptables-persistent fail2ban ufw")

# Configure iptables to limit connections
print("Configuring iptables...")
commands = [
    "sudo iptables -F",
    "sudo iptables -X",
    "sudo iptables -P INPUT DROP",
    "sudo iptables -P FORWARD DROP",
    "sudo iptables -P OUTPUT ACCEPT",
    "sudo iptables -A INPUT -i lo -j ACCEPT",
    "sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT",
    "sudo iptables -A INPUT -p tcp --syn -m connlimit --connlimit-above 10 -j DROP",
    "sudo iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT",
    "sudo netfilter-persistent save"
]
for command in commands:
    run_command(command)

# Create a custom configuration for fail2ban
print("Configuring fail2ban...")
jail_local = """
[DEFAULT]
# Ban an IP for 24 hours
bantime = 86400

# Number of attempts before banning
maxretry = 3

# Block all connections from the banned IP
banaction = iptables-multiport

[sshd]
enabled = true

[http-get-dos]
enabled = true
port = http,https
filter = http-get-dos
logpath = /var/log/nginx/access.log
maxretry = 100
findtime = 60
bantime = 600
"""

with open("/etc/fail2ban/jail.local", "w") as file:
    file.write(jail_local)

http_get_dos = """
[Definition]
failregex = ^<HOST> -.*"(GET|POST).*
"""

with open("/etc/fail2ban/filter.d/http-get-dos.conf", "w") as file:
    file.write(http_get_dos)

run_command("sudo systemctl restart fail2ban")

# Add network optimizations to /etc/sysctl.conf
print("Optimizing network settings...")
sysctl_conf = """
# Protection against SYN flood
net.ipv4.tcp_syncookies = 1

# Protection against source routing attacks
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Ignore ICMP echo requests (ping)
net.ipv4.icmp_echo_ignore_all = 1

# Increase the size of the queue
net.core.netdev_max_backlog = 5000

# Limit incomplete TCP connections
net.ipv4.tcp_max_syn_backlog = 2048

# Enable protection against IP spoofing attacks
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
"""

with open("/etc/sysctl.conf", "a") as file:
    file.write(sysctl_conf)

run_command("sudo sysctl -p")

# Enable ufw with default rules
print("Configuring ufw...")
commands = [
    "sudo ufw default deny incoming",
    "sudo ufw default allow outgoing",
    "sudo ufw allow ssh",
    "sudo ufw allow 80/tcp",
    "sudo ufw allow 443/tcp",
    "sudo ufw --force enable"
]
for command in commands:
    run_command(command)

print("Anti-DDoS configuration applied successfully.")
