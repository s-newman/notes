# Raspberry PI DHCP/PXE Boot server

This explains how to configure a Raspberry PI with a DHCP/PXE Boot server.

First, make sure to get a fresh installation of Debian on the Pi.

Configure the networking
```shell
sudo vim /etc/network/interfaces
# copy contents of interfaces.txt
sudo systemctl restart networking
```

Update software and install packages
```shell
sudo apt-get update
# This will take A LONG TIME (20+ minutes)!
sudo apt-get upgrade -y
sudo apt-get install -y isc-dhcp-server tftpd-hpa
```

Set the DHCP server defaults
```shell
sudo cat << EOF >> /etc/default/isc-dhcp-server
DHCPD_CONF=/etc/dhcp/dhcpd.conf
DHCPD_PID=/var/run/dhcpd.pid
INTERFACESv4="eth0"
EOF
```

Set the TFTP server defaults
```shell
sudo cat << EOF >> /etc/default/tftpd-hpa
TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure"
EOF
```

Configure the DHCP server
```shell
sudo mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.example.conf
sudo vim /etc/dhcp/dhcpd.conf
# copy contents of dhcpd.conf
```

Add the Ubuntu 18.04.2 net installer to the TFTP server
```shell
wget http://archive.ubuntu.com/ubuntu/dists/bionic-updates/main/installer-amd64/current/images/netboot/netboot.tar.gz
tar -zxvf netboot.tar.gz -C /srv/tftp/
```

Restart/enable DHCP & TFTP servers
```shell
sudo systemctl restart isc-dhcp-server
sudo systemctl enable isc-dhcp-server
sudo systemctl restart tftpd-hpa
sudo systemctl enable tftpd-hpa
```