.DEFAULT_GOAL := help

## GENERAL ##
OWNER               = saenz-corps
SERVICE_NAME        = condo
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
DEPLOY_REGION       ?= us-east-1

## RESULT VARS ##
PROJECT_NAME        = ${OWNER}-${ENV}-${SERVICE_NAME}
CONTAINER_NAME      = ${PROJECT_NAME}_backend
IMAGE_CLI           = ${PROJECT_NAME}:${TAG_CLI}
IMAGE_DEV           = ${PROJECT_NAME}:${TAG_DEV}

## CUSTOM ##
COMMAND             ?= pip install -r ./requirements.txt
PROJECT_DOMAIN      = condo.test


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
	docker-compose -p ${SERVICE_NAME} up -d backend
	@make status
	@make add_local_domain HOST_NAME=${PROJECT_DOMAIN}

stop: ## stop the container
	@make verify_network &> /dev/null
	@IMAGE_DEV=${IMAGE_DEV} \
	CONTAINER_NAME=${CONTAINER_NAME} \
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
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
	aws s3 sync s3://${CYBORG_BUCKET}/config/lambda/${OWNER}/${ENV}/${SERVICE_NAME}/ src/.chalice/

push-config:
	@if [ -f src/.chalice/config.json ]; then \
		aws s3 sync src/.chalice s3://${CYBORG_BUCKET}/config/lambda/${OWNER}/${ENV}/${SERVICE_NAME}/ --exclude="*" --include="config.json"; \
		echo "src/.chalice/config.json uploaded successfully."; \
	else \
		echo "src/.chalice/config.json does not exist, skipping upload."; \
	fi
	@if [ -f src/.chalice/policy.json ]; then \
		aws s3 sync src/.chalice s3://${CYBORG_BUCKET}/config/lambda/${OWNER}/${ENV}/${SERVICE_NAME}/ --exclude="*" --include="policy.json"; \
		echo "src/.chalice/policy.json uploaded successfully."; \
	else \
		echo "src/.chalice/policy.json does not exist, skipping upload."; \
	fi
	@if [ -f src/.env ]; then \
		aws s3 sync src/.chalice s3://${CYBORG_BUCKET}/config/lambda/${OWNER}/${ENV}/${SERVICE_NAME}/ --exclude="*" --include=".env"; \
		echo "src/.env uploaded successfully."; \
	else \
		echo "src/.env does not exist, skipping upload."; \
	fi
install:
	@make build

publish:
	@make command COMMAND="chalice deploy --stage=${ENV}"

deploy:
	@make sync-config install publish

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
