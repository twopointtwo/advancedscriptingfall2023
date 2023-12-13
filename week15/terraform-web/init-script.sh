#!/bin/bash
sudo yum update -y
sudo yum install httpd -y
sudo systemctl start httpd
sudo systemctl enable httpd
echo "HAENE SAFAVI - Week 15 Complete!" > /var/www/html/index.html
