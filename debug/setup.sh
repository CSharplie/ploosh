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
docker run --name ploosh_mysql \
    -e MYSQL_ROOT_PASSWORD=$db_password \
    -e MYSQL_PASSWORD=$db_password \
    -e MYSQL_DATABASE=ploosh \
    -e MYSQL_USER=ploosh \
    -p 3306:3306 \
    -d mysql

docker run --name ploosh_postgresql \
    -e POSTGRES_USER=ploosh \
    -e POSTGRES_PASSWORD=$db_password \
    -e POSTGRES_DB=ploosh \
    -p 5432:5432 \
    -d postgres

docker run --name ploosh_mssql \
    -e "ACCEPT_EULA=Y" \
    -e "MSSQL_SA_PASSWORD=$db_password" \
    --hostname ploosh \
    -p 1433:1433 \
    -d \
    mcr.microsoft.com/mssql/server:2022-latest
