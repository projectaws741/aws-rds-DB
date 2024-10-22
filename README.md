# user-information-app-rds
This is a application which collects user information and stores this in RDS and also retrieves this 

#Add postgres REPO
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-$(uname -m)/pgdg-redhat-repo-latest.noarch.rpm
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

pip3 install -r requirements.txt

cd

python3 app.py
 
