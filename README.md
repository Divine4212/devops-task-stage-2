# devops-task-stage-2
## Messaging System with RabbitMQ/Celery and Python Application behind Nginx

# DevOps Project

## Overview

This project demonstrates a DevOps setup involving a python application (`app.py`), a Celery worker (`mails.py`) for background tasks, Nginx as a reverse proxy, and Ngrok for exposing the local server to the internet. The project will be run using an Amazon EC2 instance.

## Features

- **Backend**: Python application (`app.py`).
- **Background Tasks**: Celery worker (`mails.py`) for asynchronous processing.
- **Nginx**: Reverse proxy configuration.
- **Ngrok**: Securely expose local services.

## Prerequisites

- Python 3.12+ installed.
- Ngrok account with authentication token.
- Nginx installed
- pip installed
- venv installed
- rabbitmq-server

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Divine4212/devops-task-stage-2.git
cd devops-task-stage-2

### Incase the prerequisites aren't installed

sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv rabbitmq-server -y
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

cd /home/ubuntu/your-project
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

celery -A tasks worker --loglevel=info

python app.py
```

### Configure Nginx:

Create an Nginx configuration file in /etc/nginx/sites-available/your_project with your Flask app settings.

```bash
server {
    listen 80;
    server_name your-domain.com; # use a domain or the IP address or the EC2

    location / {
        proxy_pass http://127.0.0.1:5000; # change the http://127.0.0.1 to the IP address of the instance
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the Nginx Configuration:

```bash
sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Install Ngrok

```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok

ngrok config add-authtoken "AUTH TOKEN" # this can be gotten from the dashboard
```

### Create a systemd from app.py, mails.py and ngrok

```bash
for flaskapp.service

1. create service

sudo nano /etc/systemd/system/myflaskapp.service

3. A configuration
 
[Unit]
Description=Flask App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/massage
ExecStart=/home/ubuntu/massage/myenv/bin/python /home/ubuntu/massage/app.py # Adjust WorkingDirectory and ExecStart paths to match the location of your app.py and virtual environment.
Restart=always
Environment="PATH=/home/ubuntu/massage/myenv/bin"

[Install]
WantedBy=multi-user.target

4. Reload Systemd and Start the Service:

sudo systemctl daemon-reload
sudo systemctl start myflaskapp
sudo systemctl enable myflaskapp

for celery (mail.py)

same as the flask.service, service will be created and configuration made, afterwards reload of systemd and start the service.

sudo nano /etc/systemd/system/celery.service

[Unit]
Description=Celery Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/massage
ExecStart=/home/ubuntu/massage/myenv/bin/celery -A mails worker --loglevel=info
Restart=always
Environment="PATH=/home/ubuntu/massage/myenv/bin"

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl start celery
sudo systemctl enable celery

for Ngrok

sudo nano /etc/systemd/system/ngrok.service

[Unit]
Description=Ngrok Tunnel
After=network.target

[Service]
User=ubuntu
Group=ubuntu
ExecStart=/usr/local/bin/ngrok http 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl start ngrok
sudo systemctl enable ngrok

Check services status:

sudo systemctl status myflaskapp
sudo systemctl status celery
sudo systemctl status ngrok
```

### Test the Endpoint:

```bash
http://<your-ec2-public-ip>:5000/?sendmail=someone@example.com
http://<your-ec2-public-ip>:5000/?talktome=true

use Ngrok endpoint to test endpoints:

sudo journalctl -u ngrok.service # to get the ngrok url if you used systemd

http://<ngrok-url>/?sendmail=someone@example.com
http://<ngrok-url>/?talktome=true
```

### Contributing

To contribute to this project, fork the repository and submit a pull request with your changes.

Feel free to adjust the details as needed to better fit your specific setup and project requirements.

```sh
Replace placeholders such as `YOUR_NGROK_AUTH_TOKEN`, `your_domain_or_ip`, and `your-email@example.com` with actual values relevant to your project. Adjust the Nginx configuration and any additional details as necessary.
