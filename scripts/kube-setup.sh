sudo apt-get update && apt-get install -y apt-transport-https

sudo apt install docker.io

sudo systemctl start docker
sudo systemctl enable docker

sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add

sudo cat > /etc/apt/sources.list.d/kubernetes.list << EOF
deb http://apt.kubernetes.io/ kubernetes-xenial main 
EOF

apt-get update
apt-get install -y kubelet kubeadm kubectl kubernetes-cni

swapoff -a && sed -i '/swap/d' /etc/fstab

## just for master node 
# ufw disable # disable firewall
# kubeadm init --ignore-preflight-errors Swap

#run as normal user

#mkdir -p $HOME/.kube
#sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
#sudo chown $(id -u):$(id -g) $HOME/.kube/config


#sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
#sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml

