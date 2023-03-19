# Makefile for Andrew BBS
THIS_FILE := $(lastword $(MAKEFILE_LIST))

.PHONY: build run stop migrate manage shell 

build:
	@echo "==> Building Andrew BBS"
	docker-compose build
run:
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
	docker-compose exec app python manage.py migrate
test:
	@echo "==> Test Andrew BBS"
	docker-compose exec app python manage.py test -v 2
manage:
	@echo "==> Executing manage.py $(c) in Andrew BBS"
	docker-compose exec app python manage.py $(filter-out $@,$(MAKECMDGOALS))
