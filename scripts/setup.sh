curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
chmod a+rx /usr/local/bin/youtube-dl
# install pip 
# https://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/
apt-get install python3 python3-pip python-dev build-essential -y
#pip install --upgrade pip 
# update youtube-dl
pip install --upgrade youtube-dl
