# Makefile for vulnerable-app Docker container

# Variables
IMAGE_NAME = vulnerable-app
CONTAINER_NAME = vulnerable-app
PORT = 50005
TAG = febraban
REPOSITORY_NAME = krol

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build    - Build the Docker image"
	@echo "  run      - Run the container (detached)"
	@echo "  run-fg   - Run the container in foreground"
	@echo "  stop     - Stop the running container"
	@echo "  clean    - Stop and remove container"
	@echo "  logs     - Show container logs"
	@echo "  shell    - Open shell in running container"
	@echo "  rebuild  - Clean, build, and run"

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Run container in foreground
.PHONY: run-fg
run-fg:
	docker run --rm --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME):$(TAG)
	@echo "Container started at http://localhost:$(PORT)"

# Stop the container
.PHONY: stop
stop:
	docker stop $(CONTAINER_NAME) || true

# Clean up - stop and remove container
.PHONY: clean
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Show container logs
.PHONY: logs
logs:
	docker logs -f $(CONTAINER_NAME)

# Open shell in running container
.PHONY: shell
shell:
	docker exec -it $(CONTAINER_NAME) /bin/sh

# Remove image completely
.PHONY: clean-all
clean-all: clean
	docker rmi $(IMAGE_NAME):$(TAG) || true

push: 
	docker tag $(IMAGE_NAME):$(TAG) $(REPOSITORY_NAME)/$(IMAGE_NAME):$(TAG)
	docker push $(REPOSITORY_NAME)/$(IMAGE_NAME):$(TAG) || true