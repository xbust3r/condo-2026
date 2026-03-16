.DEFAULT_GOAL := help

## GENERAL ##
OWNER               = backend-corps
SERVICE_NAME        = condo-py
USERNAME_LOCAL      ?= "$(shell whoami)"
UID_LOCAL           ?= "$(shell id -u)"
GID_LOCAL           ?= "$(shell id -g)"

## DEV ##
DOCKER_NETWORK      = services_network
TAG_CLI             = cli
TAG_DEV             = dev

## DEPLOY ##
ENV                 ?= dev
CYBORG_BUCKET       ?= project-cyborg.${ENV}
DEPLOY_REGION       ?= sa-east-1

## RESULT VARS ##
PROJECT_NAME        = ${OWNER}-${ENV}-${SERVICE_NAME}
CONTAINER_NAME      = ${PROJECT_NAME}_backend
IMAGE_CLI           = ${PROJECT_NAME}:${TAG_CLI}
IMAGE_DEV           = ${PROJECT_NAME}:${TAG_DEV}

## CUSTOM ##
COMMAND             ?= pip install -r ./requirements.txt
PROJECT_DOMAIN      = condopy.test

BALANCER_CONTAINER  = balancer
BALANCER_IP         = "$(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${BALANCER_CONTAINER})"


build: ## make build
	@tee docker/latest/resources/requirements.txt docker/cli/resources/requirements.txt < src/requirements.txt

	docker build -f docker/cli/Dockerfile \
						--build-arg USERNAME_LOCAL=$(USERNAME_LOCAL) \
						--build-arg UID_LOCAL=$(UID_LOCAL) \
						--build-arg GID_LOCAL=$(GID_LOCAL) \
						-t ${IMAGE_CLI} docker/cli

	docker build -f docker/latest/Dockerfile \
						--build-arg IMAGE_CLI=${IMAGE_CLI} \
						-t ${IMAGE_DEV} docker/latest

	@rm -f docker/latest/resources/requirements.txt docker/cli/resources/requirements.txt

up: ## start up the container
	@make verify_network &> /dev/null
	@IMAGE_DEV=${IMAGE_DEV} \
	CONTAINER_NAME=${CONTAINER_NAME} \
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	BALANCER_IP=${BALANCER_IP} \
	AWS_REGION=${DEPLOY_REGION} \
	docker-compose -p ${SERVICE_NAME} up -d backend
	@make status
	@make add_local_domain HOST_NAME=${PROJECT_DOMAIN}

stop: ## stop the container
	@make verify_network &> /dev/null
	@IMAGE_DEV=${IMAGE_DEV} \
	CONTAINER_NAME=${CONTAINER_NAME} \
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	BALANCER_IP=${BALANCER_IP} \
	AWS_REGION=${DEPLOY_REGION} \
	docker-compose -p ${SERVICE_NAME} stop
	@make status

command: ## run command
	docker run --rm -u ${UID_LOCAL}:${GID_LOCAL} -t \
				--net $(DOCKER_NETWORK) \
				-v $$PWD/src:/app \
				-v $$HOME/.ssh:/home/${USERNAME_LOCAL}/.ssh \
				-v $$HOME/.aws:/home/${USERNAME_LOCAL}/.aws \
				-e AWS_DEFAULT_REGION=${DEPLOY_REGION} \
				${IMAGE_CLI} ${COMMAND}

alembic: ## run alembic command (e.g., make alembic COMMAND="upgrade head")
	@docker run --rm -u ${UID_LOCAL}:${GID_LOCAL} -t \
				--net $(DOCKER_NETWORK) \
				-v $$PWD:/app \
				-w /app \
				-e AWS_DEFAULT_REGION=${DEPLOY_REGION} \
				${IMAGE_CLI} ${COMMAND}

ssh: ## bash
	DOCKER_NETWORK=${DOCKER_NETWORK} \
    	docker exec -it ${CONTAINER_NAME} bash

logs:
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	docker-compose -p ${SERVICE_NAME} logs -f

status:
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	docker-compose -p ${SERVICE_NAME} ps

## Deploy ##
sync-config:
	aws s3 cp s3://${CYBORG_BUCKET}/config/app/${OWNER}/${ENV}/${SERVICE_NAME}/.env src/

push-config:
	aws s3 cp src/.env s3://${CYBORG_BUCKET}/config/app/${OWNER}/${ENV}/${SERVICE_NAME}/

sync-env2yml:
	aws s3 cp s3://${CYBORG_BUCKET}/env2yml.py ./

sam-build:
	sam build \
	--template-file ./sam/template.yml

publish:
	sam deploy \
		--stack-name "${SERVICE_NAME}-${ENV}" \
		--s3-bucket ${CYBORG_BUCKET} \
		--s3-prefix "stacks/${SERVICE_NAME}-${ENV}" \
		--region ${DEPLOY_REGION} \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides ServiceName="${SERVICE_NAME}-${ENV}" \
		--no-fail-on-empty-changeset

add_local_domain:
	@if [ -z "${HOST_NAME}" ]; then (echo "Please set the ip in to 'HOST_NAME' variable. e.g. HOST_NAME=local.sample.test" && exit 1); fi
	$(eval ETC_HOSTS := /etc/hosts)
	$(eval IP := 127.0.0.1)
	$(eval HOSTS_LINE := '$(IP)\t$(HOST_NAME)')
	@if [ -n "$$(grep $(HOST_NAME) /etc/hosts)" ]; \
		then \
			echo "$(HOST_NAME) already exists : $$(grep $(HOST_NAME) $(ETC_HOSTS))"; \
		else \
			echo "Adding $(HOST_NAME) to your $(ETC_HOSTS)"; \
			sudo -- sh -c -e "echo $(HOSTS_LINE) >> /etc/hosts"; \
			if [ -n "$$(grep $(HOST_NAME) /etc/hosts)" ];\
				then \
					echo "$(HOST_NAME) was added succesfully \n $$(grep $(HOST_NAME) /etc/hosts)"; \
				else \
					echo "Failed to Add $(HOST_NAME), Try again!"; \
			fi \
	fi

verify_network:
	@if [ -z $$(docker network ls | grep ${DOCKER_NETWORK} | awk '{print $$2}') ]; then\
	    (docker network create ${DOCKER_NETWORK});\
	fi

help:
	@printf "\033[31m%-16s %-59s %s\033[0m\n" "Target" "Help" "Usage"; \
	printf "\033[31m%-16s %-59s %s\033[0m\n" "------" "----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-16s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
