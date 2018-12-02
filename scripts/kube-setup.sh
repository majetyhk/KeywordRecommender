sudo apt-get update && sudo apt-get install -y apt-transport-https

sudo apt install docker.io

sudo systemctl start docker
sudo systemctl enable docker

sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add

sudo cat > /etc/apt/sources.list.d/kubernetes.list << EOF
deb http://apt.kubernetes.io/ kubernetes-xenial main 
EOF

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni

sudo swapoff -a && sed -i '/swap/d' /etc/fstab

## just for master node 
sudo ufw disable # disable firewall
# kubeadm init --ignore-preflight-errors Swap

#run as normal user

#mkdir -p $HOME/.kube
#sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
#sudo chown $(id -u):$(id -g) $HOME/.kube/config


#sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
#sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml

