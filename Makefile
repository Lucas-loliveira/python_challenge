build up celery:
	docker-compose up --build -d
	docker-compose exec app bash -c "cd src/ && celery -A tasks worker --loglevel=info"


up celery:
	docker-compose up -d
	docker-compose exec app bash -c "cd src/ && celery -A tasks worker --loglevel=info"


celery:
	docker-compose exec app bash -c "cd src/ && celery -A tasks worker --loglevel=info"


script:
	docker-compose exec app bash -c "python src/main.py"


test:
	docker-compose exec app bash -c "pytest"

down:
	docker-compose down 