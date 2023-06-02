build:
	touch services/web/config/.env
	chmod 666 services/web/config/.env
	chmod -R 777 services/web/logs
	docker-compose up --build -d

run:
	docker attach web
