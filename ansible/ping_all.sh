#!/bin/bash

# Execute an Ansible ping of the 'dsvmall' group of VMs.
# Chris Joakim, Microsoft, 2020/03/10

ansible dsvmall -m ping
