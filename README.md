# Anti-DDoS Script for Ubuntu 22.04

This repository contains a Python script that sets up anti-DDoS protection for a web server running on Ubuntu 22.04. The script configures `iptables`, `fail2ban`, and `ufw` to help mitigate DDoS attacks and optimize network settings for better performance.

## Features

- Updates and upgrades system packages
- Installs necessary tools: `iptables-persistent`, `fail2ban`, and `ufw`
- Configures `iptables` to limit incoming connections
- Sets up `fail2ban` to block IP addresses with excessive requests
- Optimizes network settings in `/etc/sysctl.conf`
- Configures `ufw` (Uncomplicated Firewall) with default deny rules and allows necessary ports

## Requirements

- Ubuntu 22.04
- Python 3

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/Zalgoo/Anti-ddos-script.git
    cd Anti-ddos-script
    ```

2. Make the script executable:

    ```bash
    chmod +x antiddos.py
    ```

3. Run the script with sudo:

    ```bash
    sudo python3 antiddos.py
    ```

## Script Details

The script performs the following actions:

1. **Updates System Packages**:
    - Runs `apt update` and `apt upgrade` to ensure all packages are up to date.

2. **Installs Required Tools**:
    - Installs `iptables-persistent` for saving iptables rules.
    - Installs `fail2ban` for blocking IP addresses with suspicious activity.
    - Installs `ufw` for managing firewall rules.

3. **Configures iptables**:
    - Clears existing rules.
    - Sets default policies.
    - Allows loopback and established connections.
    - Limits new connections to prevent flood attacks.

4. **Configures fail2ban**:
    - Creates custom jail settings to monitor and ban IP addresses with too many requests.
    - Sets up a filter to detect HTTP GET DoS attacks.

5. **Optimizes Network Settings**:
    - Adds network optimization settings to `/etc/sysctl.conf`.

6. **Configures ufw**:
    - Sets default deny policy for incoming connections.
    - Allows outgoing connections.
    - Allows necessary ports for SSH, HTTP, and HTTPS.

## Customization

You can customize the script by editing the `antiddos.py` file. For example, you can adjust the connection limits, ban times, and other parameters to better suit your needs.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author

Created by ZalgoDev.
