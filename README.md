# azure-ansible

Examples of the Python Ansible library with Azure VMs

## Setup 

Instructions for macOS and Linux, Windows PowerShell is similar:
Assumes Python 3.7+ is present.

```
$ git clone https://github.com/cjoakim/azure-ansible.git
$ cd azure-ansible
$ python --version
Python 3.7.6
$ ./venv.sh              # Installs the python virtual environment, ansible and other libraries 
$ source bin/activate    # Activate the python virtual environment
$ ansible --version
ansible 2.9.5
```

### Edit Your **hosts** file in the current directory

```
[dsvmall]
40.121.95.166
13.73.17.143

[dsvmeastus]
40.121.95.166

[dsvmjapaneast]
13.73.17.143
```

### Edit Your **ansible.cfg** file in the current directory

```
[defaults]
inventory = hosts
remote_user = cjoakim

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=120s -A
```

### Ping your hosts via ssh

```
$ ansible dsvmall -m ping -i hosts
``