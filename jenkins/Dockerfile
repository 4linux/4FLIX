FROM jenkins:latest
USER root
RUN apt-get update && apt-get install -y mongodb-clients  libltdl7 && rm -rf /var/lib/apt/lists/*
USER jenkins
COPY plugins.txt /usr/share/jenkins/ref/
RUN /usr/local/bin/plugins.sh /usr/share/jenkins/ref/plugins.txt
COPY aliflix.jmx /var/jenkins_home/
USER root
RUN wget http://mirror.nbtelecom.com.br/apache//jmeter/binaries/apache-jmeter-4.0.tgz
RUN cd /root && tar xvfz apache-jmeter-4.0.tgz
