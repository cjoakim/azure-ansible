#!/bin/bash

# Bash shell that defines parameters and environment variables used 
# in this app, and is "sourced" by the other scripts in this repo.
# Chris Joakim, Microsoft, 2020/03/10

export subscription=$AZURE_SUBSCRIPTION_ID
export user=$USER
export region1="eastus"
export region2="westus"
export region3="japaneast"
#
export dsvm1_region=$region1
export dsvm1_rg="cjoakimdsvm1"
export dsvm1_name="cjoakimdsvm1"
export dsvm1_publisher='microsoft-dsvm'
export dsvm1_offer='linux-data-science-vm-ubuntu'
export dsvm1_sku='linuxdsvmubuntu'
export dsvm1_version='20.01.02'
export dsvm1_image=""$dsvm1_publisher":"$dsvm1_offer":"$dsvm1_sku":"$dsvm1_version # Values from: az vm image list
export dsvm1_size="Standard_DS3_v2"  # Values from: az vm list-sizes, Default: Standard_DS1_v2
export dsvm1_datasizegb="1024"
#
export dsvm2_region=$region2
export dsvm2_rg="cjoakimdsvm2"
export dsvm2_name="cjoakimdsvm2"
export dsvm2_publisher='microsoft-dsvm'
export dsvm2_offer='linux-data-science-vm-ubuntu'
export dsvm2_sku='linuxdsvmubuntu'
export dsvm2_version='20.01.02'
export dsvm2_image=""$dsvm2_publisher":"$dsvm2_offer":"$dsvm2_sku":"$dsvm2_version # Values from: az vm image list
export dsvm2_size="Standard_DS3_v2"  # Values from: az vm list-sizes, Default: Standard_DS1_v2
export dsvm2_datasizegb="1024"
#
export dsvm3_region=$region3
export dsvm3_rg="cjoakimdsvm3"
export dsvm3_name="cjoakimdsvm3"
export dsvm3_publisher='microsoft-dsvm'
export dsvm3_offer='linux-data-science-vm-ubuntu'
export dsvm3_sku='linuxdsvmubuntu'
export dsvm3_version='20.01.02'
export dsvm3_image=""$dsvm3_publisher":"$dsvm3_offer":"$dsvm3_sku":"$dsvm3_version # Values from: az vm image list
export dsvm3_size="Standard_DS3_v2"  # Values from: az vm list-sizes, Default: Standard_DS1_v2
export dsvm3_datasizegb="1024"
