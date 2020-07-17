build:
	docker-compose build --no-cache

up:
	docker-compose up

database:
	docker exec -it fuzzy_trader_db psql -U postgres

pep8:
	docker exec -it fuzzy_trader_api pep8 src/ --show-source

tests:
	docker exec -it fuzzy_trader_api python -m py.test test/