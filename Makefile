DOCKER_TAG=reverentengineer/nginx-ldap-interface

build:
	docker build -t $(DOCKER_TAG) .

deploy:
	docker push $(DOCKER_TAG)
