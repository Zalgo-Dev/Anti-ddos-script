import os
import subprocess

def run_command(command):
    """Helper function to run a shell command"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

# Mettre à jour les paquets
print("Mise à jour des paquets...")
run_command("sudo apt update && sudo apt upgrade -y")

# Installer iptables et fail2ban
print("Installation de iptables et fail2ban...")
run_command("sudo apt install -y iptables-persistent fail2ban ufw")

# Configurer iptables pour limiter les connexions
print("Configuration d'iptables...")
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

# Créer une configuration personnalisée pour fail2ban
print("Configuration de fail2ban...")
jail_local = """
[DEFAULT]
# Bannir une IP pendant 24 heures
bantime = 86400

# Nombre de tentatives avant bannissement
maxretry = 3

# Bloquer toutes les connexions de l'IP bannie
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

# Ajouter des optimisations réseau à /etc/sysctl.conf
print("Optimisation des paramètres réseau...")
sysctl_conf = """
# Protection contre les SYN flood
net.ipv4.tcp_syncookies = 1

# Protection contre les attaques de type "source routing"
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Ignorer les paquets ICMP echo (ping)
net.ipv4.icmp_echo_ignore_all = 1

# Augmenter la taille de la file d'attente
net.core.netdev_max_backlog = 5000

# Limiter les connexions TCP incomplètes
net.ipv4.tcp_max_syn_backlog = 2048

# Activer la protection contre les attaques IP spoofing
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
"""

with open("/etc/sysctl.conf", "a") as file:
    file.write(sysctl_conf)

run_command("sudo sysctl -p")

# Activer ufw avec les règles par défaut
print("Configuration de ufw...")
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

print("Configuration anti-DDoS appliquée avec succès.")
