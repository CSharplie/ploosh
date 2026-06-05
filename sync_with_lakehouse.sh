#!/bin/bash
lakehouse_name="eu_dev_lkh_dhb_ploosh_testing"
workspace_name="[SNDAI] EU-DEV-PLOOSH-TESTING_CHARLIE"
target_folder="ploosh_code"
files_to_sync=($(git status -s | awk '{print $2}'))

fabric_sync_script="sync_with_package.sh"

rm -f $fabric_sync_script

for file in ${(f)"$(git status -s | awk '{print $2}')"}; do
    folder=$(dirname "$file")

    fab cp "$file" "/${workspace_name}.Workspace/${lakehouse_name}.Lakehouse/Files/${target_folder}/${file}" -f &

    fabric_source_path="/lakehouse/default/Files/${target_folder}/${file}"
    fabric_destination_path="/home/trusted-service-user/cluster-env/trident_env/lib/python3.11/site-packages/${file/src\//}"

    echo "echo 'Syncing ${file} to Lakehouse...'" >> $fabric_sync_script
    echo "cp ${fabric_source_path} ${fabric_destination_path}" >> $fabric_sync_script
done

# Upload the sync script to the Lakehouse
fab cp $fabric_sync_script "/${workspace_name}.Workspace/${lakehouse_name}.Lakehouse/Files//${fabric_sync_script}"