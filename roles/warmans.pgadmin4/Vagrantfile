# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "debian/contrib-jessie64"
  config.vm.network "private_network", ip: "172.72.72.72"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "128"
  end

  config.vm.provision "shell", inline: "apt-get update && apt-get install openssh-server sudo zerofree python ca-certificates -y"
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "vagrant.yml"
  end
end
