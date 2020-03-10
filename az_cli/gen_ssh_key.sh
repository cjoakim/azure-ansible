#!/bin/bash

# Bash script to generate a ssh key for use with the DSVMs.
# Generates files ~/.ssh/id_rsa and ~/.ssh/id_rsa.pub
# Chris Joakim, 2020/03/10

ssh-keygen -m PEM -t rsa -b 4096
