#!/bin/bash
dnf update -y
systemctl enable nginx
systemctl start nginx
systemctl enable flaskapp
systemctl start flaskapp