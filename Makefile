docker_compose := docker compose
docker_compose_exec := $(docker_compose) exec web

#Pip params
PIP_CMD ?= list
pip:
	$(docker_compose_exec) pip $(PIP_CMD)

runserver:
	docker exec -it omni-fastapi-time-off-policy-web-1 uvicorn app.main:app --host 0.0.0.0 --port 9002 --reload