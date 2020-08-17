Esse projeto tem como objetivo construir e testar o Aliflix com o Jenkins+Jmeter

É necessario possuir o docker instalado e rodando no sistema operacional

Todo o processo é feito automaticamente pelo Jenkins, só precisamos dar build no jenkins.



Construindo o jenkins

```
docker build -t jenkins_local jenkins/Dockerfile
```

Agora podemos executar o Jenkins

```
docker run -d --name=jenkins -v /var/run/docker.sock:/var/run/docker.sock \
                -v $(which docker):/usr/bin/docker -p 8080:8080 jenkins_local
```

Após executar o Jekins temos que acessar a console web

http://localhost:8080

Instale os plugins recomendados pelo jenkins e configure o acesso

Após logar no Jenkins iremos copiar o arquivo config.xml para o diretorio /var/jenkins_home/jobs/Aliflix/

```
docker cp jenkins/config.xml jenkins:/var/jenkins_home/jobs/Aliflix/
```

Iremos parar e iniciar o container para carregar o job

```
docker stop jenkins
```

```
docker start jenkins
```

