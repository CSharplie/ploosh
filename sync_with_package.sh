echo 'Syncing src/ploosh/connectors/connector_fabric_kql_spark.py to Lakehouse...'
cp /lakehouse/default/Files/ploosh_code/src/ploosh/connectors/connector_fabric_kql_spark.py /home/trusted-service-user/cluster-env/trident_env/lib/python3.11/site-packages/ploosh/connectors/connector_fabric_kql_spark.py
echo 'Syncing sync_with_lakehouse.sh to Lakehouse...'
cp /lakehouse/default/Files/ploosh_code/sync_with_lakehouse.sh /home/trusted-service-user/cluster-env/trident_env/lib/python3.11/site-packages/sync_with_lakehouse.sh
