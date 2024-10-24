# user-information-app-rds
This is a application which collects user information and stores this in RDS and also retrieves this and fetches endpoint,username and password from aws parameter store.

create RDS_ENDPOINT, RDS_USERNAME and RDS_PASSWORD in aws parameter store and use RDS_PASSWORD as secure string.

#Add postgres REPO
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-$(uname -m)/pgdg-redhat-repo-latest.noarch.rpm

If the above cmd is not woking use below cmd to install postgres client version 15

#sudo dnf install postgresql15

#Disable Amazon Linux’s Default PostgreSQL (if necessary):
sudo yum remove postgresql
#Install PostgreSQL Client Version 13
sudo yum install -y postgresql13
#Check the Installed Version
psql --version
#Connect to psql DB
psql -h pydb.cvcu6ymskoeq.us-east-1.rds.amazonaws.com  -U postgres -p 5432

=========App==========
Clone the repo
go to template folder

cd /root/aws-rds/db-app/templates

requiremnts.txt must have below versions.

Flask==2.0.1
PyMySQL==1.0.2
Werkzeug==2.0
psycopg2-binary
boto3==1.18.0

pip3 install -r requirements.txt


cd

python3 app.py


Please run docker image and push to docker repo.
create a cluster and create a task defination file. create a task execution role that provides access to aws parameter store. run the task and verify it. 
