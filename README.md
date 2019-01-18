# website
Dynamic personal website.

## Setup

1. Run the setup script as root
```
sudo ./setup.sh
```
2. Update `personalpage/personalpage/secrets.txt` using the hints in `personalpage/personalpage/secrest.txt.format`
3. If running on port 8000 to the outside world, be sure to open up the firewall ports:
```
sudo firewall-cmd --add-port=8000/tcp
```
4. Be sure to update "ALLOWED_HOSTS" in `settings.py` to have this server's proper IP address:
5. Make sure your Python path is set using the software collections enable script.  This should only need to be run once
   because the script takes care of it for you in .bashrc
```
. /opt/rh/rh-python35/enable
```
6. Run any lingering DB migrations then kick off the server!
```
cd personalpage
python manage.py migrate
python manage.py runserver 0:8000
```
