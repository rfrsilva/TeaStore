# Teastore-Probe
This probe is able collect response time and throughput from TeaStore project.

## Prerequisites
The instructions were tested in `ubuntu`, but should work in other `debian`-based distributions, assuming that you are able to install the key dependencies.

The first step is to install the required components: `docker`, and `kubernetes`.

To install docker, you should execute the following command:
```sh
sudo su -
apt-get install docker.io
```
To install Kubernetes you should execute the following commands:

```sh
sudo su -
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add 
echo -e "deb http://apt.kubernetes.io/ kubernetes-xenial main " >> /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```

In order to use Kubernetes two machines (nodes) are required with different IP addresses for deploying all necessary pods.

These two nodes communicate through network plugin Flannel.
To initialize the Kubernetes cluster, run the following command in the Master machine:

```sh
swapoff -a
kubeadm init --pod-network-cidr=10.244.0.0/16
```

The output of the command above gives the required commands to complete the setup of Kubernetes cluster. Those commands are:

```sh
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


Before joining the other node in this cluster, it is necessary to setup the network plugin that is responsible for the communications between Master and Worker nodes.
To do that, run:

```sh
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml
ip route add 10.96.0.0/16 dev xxxxxx
```

Where xxxxxx is the network interface name.
After these commands, Master node will be at "Ready" state. For joining the other node, paste the last command of the output of the kubeadm init command in that node. One example of this command can be:
```sh
kubeadm join --token TOKEN MASTER_IP:6443
```

Where TOKEN is the token you were presented after initializing the master and MASTER_IP is the IP address of the master.
Now, the Kubernetes cluster are ready to deploy containers.

After completing all steps of the previous section, the first step of project installation is to create the images that deploy Apache Kafka, Apache Zookeeper, the Monitor API REST, and Apache Flume containers. In order to do that, there is a shell script called `build.sh` presented in [`kafka`](https://github.com/eubr-atmosphere/tma-framework-m/tree/master/development/server/kafka), [`zookeeper`](https://github.com/eubr-atmosphere/tma-framework-m/tree/master/development/server/zookeeper), [`monitor-server-python`](https://github.com/eubr-atmosphere/tma-framework-m/tree/master/development/server/monitor-server-python), and [`flume`](https://github.com/eubr-atmosphere/tma-framework-m/tree/master/development/server/flume) folders of this project.

To deploy the monitor, you need to run the script called `build.sh` presented in [`dependency/python-base`](https://github.com/eubr-atmosphere/tma-framework-m/tree/master/development/dependency/python-base "python-base") folder in order to create the base python image that will be used to generate the container that runs the Monitor.
To execute this script for all components of the architecture, you should run the following commands on the worker node:

```sh
cd development/dependency/python-base/
sh build.sh
cd ../../server/kafka
sh build.sh
cd ../zookeeper
sh build.sh
cd ../flume
sh build.sh
cd ../monitor-server-python
sh build.sh
```

After executing this script, all containers are created and we are ready to deploy them on Kubernetes cluster.

The first containers to be deployed in Kubernetes are Apache Zookeeper, Apache Kafka, and Apache Flume. To do that, there is a script called [`setup-testing-mode.sh`](https://github.com/eubr-atmosphere/tma-framework-m/blob/master/development/server/setup-testing-mode.sh) that automates all commands required to deploy these components. To execute the script, run the following command:

```sh
cd ..
sh setup-testing-mode.sh
```

First,  [`setup-testing-mode.sh`](https://github.com/eubr-atmosphere/tma-framework-m/blob/master/development/server/setup-testing-mode.sh) script runs the required commands to create the persistent volumes for Apache Zookeeper and Apache Kafka. Then, it deploys these two components. Then, it creates `topic-monitor` and `queue-listener` topics in Apache Kafka pod. Finnaly, Apache Flume is deployed in Kubernetes Cluster.

With Apache Zookeeper, Apache Kafka, and Apache Flume running and the topics created, the next step is to deploy the Monitor application. The file called [`monitor-api-python.yaml`](https://github.com/eubr-atmosphere/tma-framework-m/blob/master/development/server/monitor-server-python/monitor-api-python.yaml) creates a Kubernetes Deployment of the Monitor application. In order to create that deploy, you should run:

```sh
kubectl create -f monitor-server-python/monitor-api-python.yaml
``` 

To run this probe, you need also to download `tmalibrary` python package. To do that, you should execute the following command:

```sh
pip install tmalibrary
``` 

## Installation

The first step to install this probe is to execute `teastoreresults.sh`. To do that, you should execute the following command:

```sh
./teastoreresults.sh
``` 

With the previous script running, you can run the Teastore-Probe. To do that, you should execute the following command:

```sh
python probe-teastore.py
``` 

## Testing

If everything is working, the probe should print 0s.