FROM centos:7
RUN yum install -y wget gcc openssl-devel cairo cairo-devel cairomm-devel  python-devel libxslt-devel libffi-devel gcc-c++ kernel-devel python-gobject gobject-introspection-devel cairo-gobject cairo-gobject-devel 
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-14.noarch.rpm
RUN yum install -y python-pip
COPY requirements.txt /srv/
RUN cd /srv/ && pip2.7 install -r requirements.txt
RUN yum remove gcc kernel-devel gcc-c++ -y
RUN yum clean all
RUN rm -rf /var/cache/yum
COPY app.py /srv/
CMD ["python2.7", "/srv/app.py"]
