FROM ubuntu:bionic 
RUN apt-get update && apt-get install -y apache2 && apt-get -y clean
ADD frontend.tar.gz /var/www/html/
ADD mod_status /tmp/
RUN cat /tmp/mod_status > /etc/apache2/mods-enabled/status.conf
EXPOSE 80
CMD apachectl -D FOREGROUND
