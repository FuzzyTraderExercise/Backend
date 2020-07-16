build:
	docker-compose build --no-cache

up:
	docker-compose up

database:
	sudo docker exec -it fuzzy_trader_db psql -U postgres