#!/bin/bash
#------------------------------------------------------------
# Use this script for a new system build to:
#  - Install base packages
#  - Enable package paths for relavent users
#
# For more of an 'enterprise' solution, this stuff should really
#   got into an infrastructure-as-code system like Puppet or orchestration
#   tool like Ansible.  Let those tools deal packages and versions,
#   services, user settings, etc.  This is just easier than running these 
#   commands every server build. :)
#------------------------------------------------------------

# Setup dev variables for VIM
if [[ "$1" == "DEV" ]]; then 
  ENV=$1
  echo "Setting up VIM spacing for Python"
  cp .vimrc.dev /home/$(logname)/.vimrc
else
  ENV='PROD'
fi

#---------------------------------------
# START: package installs and enablement
#---------------------------------------

# Make sure CentOs software collections is in repos.d for newer packages
if /usr/bin/yum repolist | /usr/bin/grep -i -q 'centos-sclo'; then
  echo "CentOS Software Collections already installed"
else
  echo "Need to install CentOS Software Collections"
  yum install -y -q centos-release-scl
fi

# Install required packages
# - Python 3.5
# - PostgreSQL 9.6
# - Django 2.1.5
yum install -y -q rh-python35-python rh-python35-python-psycopg2 rh-python35-python-virtualenv rh-python35-scldevel.x86_64 rh-python35-python-devel.x86_64 rh-postgresql96-postgresql rh-postgresql96-postgresql-server gcc nginx
. /opt/rh/rh-python35/enable
. /opt/rh/rh-postgresql96/enable

echo "Upgrading pip..."
pip install --upgrade pip
echo "Installing python packages..."
pip install Django==2.1.5 uwsgi django-tinymce gunicorn

# Add paths to our user logged in user
if ! /usr/bin/grep '. /opt/rh/rh-python35/enable' /home/$(logname)/.bashrc; then
  echo 'Adding Python 3.5 to logged in user path'
  echo -e "\n. /opt/rh/rh-python35/enable" >> /home/$(logname)/.bashrc
fi

if ! /usr/bin/grep '. /opt/rh/rh-postgresql96/enable' /home/$(logname)/.bashrc; then
  echo 'Adding PostgreSQL 9.6 to logged in user path'
  echo -e "\n. /opt/rh/rh-postgresql96/enable" >> /home/$(logname)/.bashrc
fi

#---------------------------------------
# END: package installs and enablement
#---------------------------------------

#---------------------------------------
# START: DB setup
#---------------------------------------

DATA_PATH='/var/opt/rh/rh-postgresql96/lib/pgsql/data'
SERVICE=rh-postgresql96-postgresql
DB=webapp
DB_USER=webappuser

# Initialize the DB
if [[ -z "$(ls -A $DATA_PATH)" ]]; then
  echo "Welp, looks like you're going to need to get this DB set up."
  echo "Creating directory for the data:"
  mkdir -p $DATA_PATH
  chown -R postgres:postgres $DATA_PATH
  # Make sure to preserve your initdb path with the -m
  if ! su -m postgres -c "initdb -D $DATA_PATH -U postgres"; then
    echo "Something went wrong with postgres setup.  Check output above.  Exiting."
    exit
  fi
  systemctl start $SERVICE
  if [[ "$?" != "0" ]]; then
    echo "The service could not start"
    exit
  fi
  echo "** Heads up!"
  echo "What will the user password be?"
  read DB_USER_PW

  # Set up application user
  # There is most likely a better way to accomplish this via a template, but this works for now
  cd /tmp/
  su -m postgres -c "psql -c \"CREATE USER $DB_USER PASSWORD '$DB_USER_PW'\""
  su -m postgres -c "psql -c \"CREATE DATABASE $DB WITH OWNER $DB_USER\""

  # Allow for creating test databases
  su -m postgres -c "psql -c \"ALTER USER $DB_USER CREATEDB\""
  echo "Database initallized and started"
else
  echo "Good news, the DB is already initialized"
fi

systemctl enable rh-postgresql96-postgresql

