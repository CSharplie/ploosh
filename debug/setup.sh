# Configuration
db_password=ThePasswordIs9293709B13?

# Setup dev envrionnement 
conda create -n ".ploosh" python=3.12.8 ipython
conda activate .ploosh

pip install -r ./src/requirements.txt

# install connectors clients
sudo apt-get update

sudo apt-get install -y postgresql-client
sudo apt-get install -y mysql-client
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev

# install connectors servers 
docker run --name ploosh-mysql \
    -e MYSQL_ROOT_PASSWORD=$db_password \
    -e MYSQL_PASSWORD=$db_password \
    -e MYSQL_DATABASE=ploosh \
    -e MYSQL_USER=ploosh \
    -p 3306:3306 \
    -d mysql

docker run --name ploosh-postgresql \
    -e POSTGRES_USER=ploosh \
    -e POSTGRES_PASSWORD=$db_password \
    -e POSTGRES_DB=ploosh \
    -p 5432:5432 \
    -d postgres

docker run --name ploosh-mssql \
    -e "ACCEPT_EULA=Y" \
    -e "MSSQL_SA_PASSWORD=$db_password" \
    --hostname ploosh \
    -p 1433:1433 \
    -d \
    mcr.microsoft.com/mssql/server:2022-latest

docker run -d --name ploosh-spark-master \
  -e SPARK_MODE=master \
  -e SPARK_MASTER_HOST=ploosh-spark-master \
  -p 7077:7077 -p 8081:8080 \
  -v $(pwd)/tests/.data:$(pwd)/tests/.data \
  --hostname ploosh-spark-master \
  bitnami/spark
  
docker run -d --name ploosh-spark-worker \
  -e SPARK_MODE=worker \
  -e SPARK_MASTER_URL=spark://ploosh-spark-master:7077 \
  -v $(pwd)/tests/.data:$(pwd)/tests/.data \
  --link ploosh-spark-master:ploosh-spark-master \
  bitnami/spark

mysql -h 127.0.0.1 -u ploosh -p$db_password < tests/.env/mysql/setup.sql

export PGPASSWORD=$db_password;
psql -h 127.0.0.1 -U ploosh -d ploosh -f tests/.env/postgresql/setup.sql

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $db_password -i tests/.env/mssql/setup.sql
