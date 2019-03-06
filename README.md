# website
Dynamic personal website.
* Django
* gunicorn
* NGINX
* Bulma CSS
* TinyMCE plugin

## Setup

1. Run the setup script as root
```
sudo ./setup.sh
```
2. Update `personalpage/personalpage/secrets.txt` using the hints in `personalpage/personalpage/secrest.txt.format`
3. Make sure your Python path is set using the software collections enable script.  This should only need to be run once because the script takes care of it for you in .bashrc
```
. /opt/rh/rh-python35/enable
```
4. Kick off the deploy script to startup `NGINX` and `gunicorn`:
```
sudo ./deploy.sh
```
5. Use pg_dump to export data from old server an import into new server.
