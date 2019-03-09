#!/bin/bash
#------------------------------------------------------------
# Use this script to check and deploy the project
#  - Creates relavent directories
#  - Sets up gunicorn and nginx configs
#
# Django Documentation (https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/)
#   suggests addressing the following items:
# - SECRETE_KEY is indeed secret; do not store in version control 
# - DEBUG = False in prod
#
# For more of an 'enterprise' solution, this stuff should really
#   got into an infrastructure-as-code system like Puppet or orchestration
#   tool like Ansible.  Let those tools deal packages and versions,
#   services, user settings, etc.  This is just easier than running these 
#   commands every server build. :)
#------------------------------------------------------------

# Create a django user for actually running this project and copy files over
DEPLOY_PATH=/opt/django
PROJECT=personalpage
PROC_ID=django
useradd $PROC_ID

echo "Enabling python"
. /opt/rh/rh-python35/enable

# Add paths to our user logged in user
if ! /usr/bin/grep '. /opt/rh/rh-python35/enable' /home/$PROC_ID/.bashrc; then
  echo 'Adding Python 3.5 to logged in user path'
  echo -e "\n. /opt/rh/rh-python35/enable" >> /home/$PROC_ID/.bashrc
fi

if ! /usr/bin/grep '. /opt/rh/rh-postgresql96/enable' /home/$PROC_ID/.bashrc; then
  echo 'Adding PostgreSQL 9.6 to logged in user path'
  echo -e "\n. /opt/rh/rh-postgresql96/enable" >> /home/$PROC_ID/.bashrc
fi

echo "create deployment dir..."
mkdir $DEPLOY_PATH
chmod 710 $DEPLOY_PATH

echo "Creating, chowning, and chmodding deploy dirs..."
cp -R personalpage $DEPLOY_PATH/
chown -R django:nginx $DEPLOY_PATH
chmod 744 $DEPLOY_PATH/$PROJECT/gunicorn.sh 
mkdir -p /usr/share/nginx/html/django/static
chown -R django:nginx /usr/share/nginx/html/django

echo "Cleaning up settings.py"
sed -i 's/DEBUG = True/DEBUG = False/g' $DEPLOY_PATH/$PROJECT/$PROJECT/settings.py
sed -i "s/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = ['127.0.0.1']/g" $DEPLOY_PATH/$PROJECT/$PROJECT/settings.py 

# Enable gunicorn and NGINX services
echo "getting configs into place..."
cp gunicorn.service /etc/systemd/system/gunicorn.service
cp nginx.conf /etc/nginx/nginx.conf

systemctl deamon-reload 

echo "Setting up SSL with Let's Encrypt"
yum -y install yum-utils
yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional
yum -y install certbot python2-certbot-nginx

echo "requesting certificate"
certbot --nginx certonly --dry-run --domains respectablehack.com,www.respectablehack.com

sudo crontab -u root renew.crontab

echo "Enabling and starting services!"
systemctl restart gunicorn.service
systemctl enable  gunicorn.service
systemctl restart nginx.service 
systemctl enable  nginx.service

# Allow nginx to be in django's group
echo "updating nginx user"
usermod -a -G django nginx

echo "Setting up database tables"
cd $DEPLOY_PATH/$PROJECT
su -m django -c "python manage.py migrate"

echo "'collectstatic' running"
su -m django -c "python manage.py collectstatic"

echo "setting SELinux permissions"
semanage fcontext -a -t httpd_var_run_t /opt/django/personalpage/personalpage.sock
restorecon /opt/django/personalpage/personalpage.sock

echo "Establishing upload permissions"
semanage fcontext -a -t httpd_sys_rw_content_t /usr/share/nginx/html/django/static/blog/uploads
restorecon /usr/share/nginx/html/django/static/blog/uploads

echo "Should be all set!"
