build:
	docker-compose build --no-cache

up:
	docker-compose up

database:
	sudo docker exec -it fuzzy_trader_db psql -U postgres

pep8:
	sudo docker exec -it fuzzy_trader_api pep8 src/ --show-source