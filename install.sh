#!/bin/bash

SERVICE_FILE="sas-bot.service"
SERVICE_NAME="sas-bot"

echo "Creating service file at /etc/systemd/system/${SERVICE_FILE}"

cat << EOF > /etc/systemd/system/${SERVICE_FILE}
[Unit]
Description=VK Bot
After=network.target

[Service]
Type=simple
User=$(if [ "$(systemd-detect-virt)" == "none" ]; then echo $USER; else echo "root"; fi)
WorkingDirectory=/home/django/django_venv/src/django_project/
ExecStart=/usr/bin/python3 /home/django/django_venv/src/django_project/bot_start.py

Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
EOF

echo "Enabling and starting service ${SERVICE_NAME}"

sudo systemctl enable ${SERVICE_NAME}
sudo systemctl start ${SERVICE_NAME}

echo "Service installed and started successfully!"
