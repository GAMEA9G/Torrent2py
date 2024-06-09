# Description:
This is web app you can search Movies and download Movies easily by clicking on a link
Easy and fast way to download torrents
### How it works:
it get magnet links from https://torrentz2.nz/ site and when clicked it will download with magnet links with Qbittorrent 
# Installation:
clone this repository
## install dependences by typing this command:
pip install -r requirements.txt
## install qbittorrent
install qbittorent through this link https://www.qbittorrent.org/download 
if you already have that you can skip this step
## Enable Web UI
Open qbittorrent > Settings > Web UI  Enable Web User Interface Set password to adminadmin
Usename must be admin
# How to use
use this command
```bash
python app.py
```
and go to http://127.0.0.1:5000/
