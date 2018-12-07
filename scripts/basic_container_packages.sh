
echo "nameserver 8.8.8.8" | tee /etc/resolvconf/resolv.conf.d/base > /dev/null

apt-get update
apt-get -y -qq install python3
apt-get -y -qq install python3-pip
apt-get -y -qq install git
apt-get -y -qq install iputils-ping
apt-get -y -qq install iproute2
apt-get -y -qq install vim
apt-get -y -qq install dnsutils
