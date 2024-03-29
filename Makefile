# Makefile for Andrew BBS
THIS_FILE := $(lastword $(MAKEFILE_LIST))

.PHONY: build run stop migrate test manage shell up

# build the image, make and run migrations, and run the container
run: build migrate up

build:
	@echo "==> Building Andrew BBS"
	docker-compose build
up:
	@echo "==> Running Andrew BBS"
	docker-compose up
stop:
	@echo "==> Stopping Andrew BBS"
	docker-compose down
shell:
	@echo "==> Executing shell in Andrew BBS"
	docker-compose exec app bash
migrate:
	@echo "==> Migrating Andrew BBS"
	docker-compose run --rm app python manage.py makemigrations
	docker-compose run --rm app python manage.py migrate
test:
	@echo "==> Test Andrew BBS"
	docker-compose exec app python manage.py test $(TEST) -v 2
manage:
	@echo "==> Executing manage.py $(c) in Andrew BBS"
	docker-compose exec app python manage.py $(filter-out $@,$(MAKECMDGOALS))
format:
	@echo "==> Formatting Andrew BBS code with black"
	docker-compose exec app black . --exclude /andrewbbs/migrations/
