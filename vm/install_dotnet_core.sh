#!/bin/bash

# Bash shell script which runs on the Ubuntu VM/DSVM
# to install DotNet Core.  Can be executed remotely by Ansible.
# Chris Joakim, Microsoft, 2020/03/11
# See https://docs.microsoft.com/en-us/dotnet/core/install/linux-package-manager-ubuntu-1604

cd ~

wget -q https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb

sudo apt-get update
sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install dotnet-sdk-3.1
