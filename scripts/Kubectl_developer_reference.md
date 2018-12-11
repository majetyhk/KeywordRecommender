Read me for troubleshooting kubernetes 

## Presentation - https://prezi.com/p/ei6gtyfxo-xi/

### IP table rules if Nodes are not able to ping - 
sudo iptables -I INPUT 1 -j ACCEPT
sudo iptables -I FORWARD 1 -j ACCEPT

* Networking to check if the port is up == nc -zv 152.46.16.167 9092

### create image of a running container - 
sudo docker commit -m "Installed required packages and git clone keyword code" --author "Shyam" Running_containerID ImageName:Tag

* execute a pod == kubectl exec -it pod -- /bin/bash
* export pod deployment file == kubectl get deploy pod -o yaml --export
* create pod from image == kubectl run my-shell --rm -i --tty --image ubuntu -- bash
* Permanently store credentials once == git config credential.helper store

* DNS issues in Ubuntu base image == echo "nameserver 8.8.8.8" | sudo tee /etc/resolvconf/resolv.conf.d/base > /dev/null

* Create pod == kubectl run channel -i --tty --image keyword:new
* Command to pod == kubectl exec -it POD -- bash
* Attach terminal == kubectl attach pod_running_name -c pod_name -it
* delete deployment later and spin down node

* If pod deployment failing due to CIDR address issue - manually assign by command =
kubectl patch node node-name -p '{"spec":{"podCIDR":"192.168.0.0/16"}}

* Portable docker images == sudo docker save -o keyword.tar keyword:stable

* scp == sudo scp keyword.tar skatta3@152.46.19.21:/home/skatta3

* Images to spin up a pod should be present in the local node not in the master node, or it will try pulling from docker hub

## Kubernetes on ubuntu
* sudo kubeadm init —pod-network-cidr=192.168.0.0/16 —apiserver-advertise-address=10.160.0.2 --cluster-cidr=10.244.0.0/16 --allocate-node-cidrs=true
* Unjoin == sudo kubeadm reset
* Join command == kubeadm token create --print-join-command

### Install URLs
* https://www.techrepublic.com/article/how-to-quickly-install-kubernetes-on-ubuntu/
* http://www.ethernetresearch.com/geekzone/kubernetes-tutorial-how-to-install-kubernetes-on-ubuntu/

URLs 

https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/


Networking = https://medium.com/@anilkreddyr/kubernetes-with-flannel-understanding-the-networking-part-2-78b53e5364c7
