# 🔒 Script Anti-DDoS

Script Python pour renforcer la sécurité d'un serveur Linux contre les attaques DDoS et les intrusions.

---

## 📋 Fonctionnalités

- 🛡️ Configuration automatique d'un pare-feu strict (`iptables` + `UFW`)
- 🚫 Protection contre les attaques par force brute (`Fail2Ban`)
- 🌐 Optimisation des paramètres réseau (`sysctl`)
- ⚡ Protection contre SYN Flood, IP spoofing et connexions abusives
- 🔄 Mise à jour automatique des paquets système

---

## 📦 Prérequis

- Système d'exploitation : Debian / Ubuntu
- Python 3.x
- Accès root (`sudo`)

---

## 🚀 Installation & Utilisation

1. Téléchargez le script :

```bash
wget [https://github.com/Zalgo-Dev/Anti-ddos-script/blob/main/antiddos.py](https://github.com/Zalgo-Dev/Anti-ddos-script/blob/main/antiddos.py)
```

2. Rendez-le exécutable :

```bash
chmod +x antiddos.py
```

3. Exécutez-le avec les droits root :

```bash
sudo ./antiddos.py
```

---

## ⚙️ Configuration appliquée

### 🔥 Règles `iptables`

- Blocage par défaut du trafic entrant
- Limitation des connexions TCP (10 max)
- Rate limiting HTTP (25 requêtes/minute)
- Autorisation uniquement des ports :  
  - SSH (22)  
  - HTTP (80)  
  - HTTPS (443)

### 🛑 `Fail2Ban`

- Bannissement des IP après **3 échecs SSH**
- Protection contre les attaques HTTP DoS (100 reqs/minute)
- Durée de bannissement :
  - **24h** pour SSH
  - **10 minutes** pour HTTP

### 🌐 Optimisations réseau

- Activation de la protection **SYN cookies**
- Désactivation des requêtes ping (**ICMP**)
- Prévention contre le **spoofing IP**
- Augmentation des files d’attente réseau

---

## ⚠️ Avertissements

Ce script **va** :

- Effacer toutes vos règles `iptables` existantes
- Modifier des fichiers système critiques
- Désactiver les requêtes ping

> **Testez toujours dans un environnement de développement avant déploiement en production.**  
> **Sauvegardez vos configurations existantes :**

```bash
sudo iptables-save > ~/iptables_backup.rules
sudo cp /etc/fail2ban/jail.local ~/jail.local.backup
```

---

## 🔄 Restauration

Pour annuler les changements :

```bash
sudo iptables-restore < ~/iptables_backup.rules
sudo cp ~/jail.local.backup /etc/fail2ban/jail.local
sudo sysctl -p /etc/sysctl.conf.bak
sudo ufw disable
```

---

## 📜 Licence

MIT License - Libre d'utilisation et de modification.
