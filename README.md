# azure-ansible

Examples of the Python Ansible library with Azure VMs

## Ansible Links

- https://docs.microsoft.com/en-us/azure/ansible/
- https://www.ansible.com
- https://docs.ansible.com 
- https://www.ansible.com/integrations/infrastructure/windows
- https://docs.ansible.com/ansible/latest/modules/list_of_windows_modules.html
- https://pypi.org/project/ansible/
- https://www.azuredevopslabs.com/labs/vstsextend/ansible/

---

## Setup for this example repo

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

### Create your Data Science Virtual Machines (DSVMs)

```
$ cd az_cli/
$ ./gen_ssh_key.sh   (optional, you can use your current id_rsa key)
$ ./dsvm1.sh create ; ./dsvm2.sh create ; ./dsvm3.sh create
```

See the **tmp/dsvm<n>_vm_create.json** files to obtain the IP Address of each DSVM.

### ssh into your DSVMs to test connectivity

```
$ ssh -A <your-user-id>@<your-dsvm-ip>
$ ssh -A chris@1.2.3.4
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
```

---

## Example Use

Remotely configure the git user on the remote VMs:
```
$ ansible-playbook git-setup.yml
```

Same command with verbose debug information:
```
$ export ANSIBLE_DEBUG=1 ; ansible-playbook git-setup.yml
```

Pull the latest code to a git repository:
```
$ ansible-playbook git-pull.yml
```

Install the DotNet Core 3.1 SDK on the Ubuntu VM:
```
$ ansible-playbook apt-install-dotnet-core.yml
```
