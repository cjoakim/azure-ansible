#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of an
# Azure Data Science Virtual Machine w/Ubuntu Linux.
# Chris Joakim, 2020/03/10
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

# az login

source ./app-config.sh

arg_count=$#

delete() {
    echo 'deleting DSVM rg: '$dsvm2_rg
    az group delete \
        --name $dsvm2_rg \
        --subscription $subscription \
        --yes \
        > tmp/dsvm2_rg_delete.json
}

create() {
    echo 'creating DSVM rg: '$dsvm2_rg
    az group create \
        --location $dsvm2_region \
        --name $dsvm2_rg \
        --subscription $subscription \
        > tmp/dsvm2_rg_create.json

    echo 'creating DSVM: '$dsvm2_name
    az vm create \
        --name $dsvm2_name \
        --resource-group $dsvm2_rg \
        --location $dsvm2_region \
        --image $dsvm2_image \
        --size $dsvm2_size \
        --admin-username $user \
        --authentication-type ssh \
        --generate-ssh-keys \
        --subscription $subscription \
        --verbose \
        --output json \
        > tmp/dsvm2_vm_create.json
}

recreate() {
    delete
    create
    info 
}

info() {
    echo 'az vm list ...'
    az vm list > tmp/vm_list.json

    echo 'az vm show ...'
    az vm show \
        --name $dsvm2_name \
        --resource-group $dsvm2_rg \
        > tmp/vm_show.json
}

dsvm_skus() {
    az vm list-skus --location $dsvm2_region
}

dsvm_sizes() {
    az vm list-sizes --location $dsvm2_region
}

dsvm_usage() {
    az vm list-usage --location $dsvm2_region
}

display_usage() {
    echo 'Usage:'
    echo './dsvm2.sh delete'
    echo './dsvm2.sh create'
    echo './dsvm2.sh recreate'
    echo './dsvm2.sh info'
    echo './dsvm2.sh dsvm_skus'
    echo './dsvm2.sh dsvm_sizes'
    echo './dsvm2.sh dsvm_usage'
}

if [ $arg_count -gt 0 ]
then
    if [ $1 == "delete" ] 
    then
        delete
        exit 0  
    fi

    if [ $1 == "create" ] 
    then
        create
        exit 0
    fi

    if [ $1 == "recreate" ] 
    then
        recreate
        exit 0
    fi

    if [ $1 == "info" ] 
    then
        info
        exit 0
    fi

    if [ $1 == "dsvm_skus" ] 
    then
        dsvm2_skus
        exit 0
    fi

    if [ $1 == "dsvm_sizes" ] 
    then
        dsvm2_sizes
        exit 0
    fi

    if [ $1 == "dsvm_usage" ] 
    then
        dsvm2_usage
        exit 0
    fi

    display_usage
else
    display_usage
fi

echo 'done'
