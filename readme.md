# Leddeo Backend

The backend server for leddeo application, this manages:

- User authentication with jwt and google
- Automatic transcription generation
- Automatic translation
- Integration with stripe and subscriptions management
- Frequent asked questions
- Apply transcription to video file

## Server setup

### Required directory

Just create the app folder in the home directory of the remote server.

### Download docker

- sudo apt-get update -y
- curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
- sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
- sudo apt-get update -y
- sudo apt-get install docker-ce docker-ce-cli containerd.io -y
- sudo docker version

### Download and setup nginx

from this [LINK](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04-es):

- ssh to remote server
- sudo apt install nginx
- check if nginx server is running
- run sudo nano /etc/nginx/nginx.conf
- fill with this content:
  http {
  client_max_body_size 1000M;
  server {
  listen 80;
  server_name example.com;
  location / {
  proxy_pass http://localhost:8000;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_connect_timeout 3600s;
  proxy_send_timeout 3600s;
  proxy_read_timeout 3600s;
  send_timeout 3600s;
  }
  }
  }
- Add DNS records in domain provider to point to the remote server url
- Must add the A and AAA records
- Follow instructions to install certbot [instalar certbot en ubuntu](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal)
