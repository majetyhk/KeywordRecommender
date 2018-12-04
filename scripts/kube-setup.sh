sudo apt-get update && sudo apt-get install -y apt-transport-https

sudo apt -y install docker.io

sudo systemctl start docker
sudo systemctl enable docker

sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add

echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" \
	| sudo tee -a /etc/apt/sources.list.d/kubernetes.list
  
# sudo tee -a /etc/apt/sources.list.d/kubernetes.list
#sudo cat > /etc/apt/sources.list.d/kubernetes.list << EOF
#deb http://apt.kubernetes.io/ kubernetes-xenial main 
#EOF

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

## Notes - require high ram, few config changes and firewall rules to enable joining cluster
# basic steps - sysctl net.bridge.bridge-nf-call-iptables=1, sudo swapoff -a, sudo ufw disable, 
# IP rules if needed, these will be flushed frequently, need to run chron job if needed and are vital
# sudo iptables -I INPUT 1 -j ACCEPT, sudo iptables -I FORWARD 1 -j ACCEPT

# sudo kubeadm init —pod-network-cidr=192.168.0.0/16 —apiserver-advertise-address=10.160.0.2
# after init, run the commands shown in log of init mkdir, some setup (failure might result in localhost not reachable error)

# incase the pod-cidr is failed to assign by default, we need to manually assign by using command - kubectl patch node node-name -p '{"spec":{"podCIDR":"CIDR-subnet"}}'
# spin up a simple ubuntu container using -> kubectl run my-shell --rm -i --tty --image ubuntu -- bash
# incase of container running check the pod by using - kubectl describe pod my-shell

# after spin, if want to reset use - sudo kubeadm reset, delete ~/.kube folder and apply CNI rules flanner or caliso as shown in 
# https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/

# general commands - kubectl get componentstatuses
