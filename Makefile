build:
	docker-compose build

build-yarn:
	docker-compose -f docker-compose.yarn.yml build

build-yarn-nc:
	docker-compose -f docker-compose.yarn.yml build --no-cache

build-nc:
	docker-compose build --no-cache

build-progress:
	docker-compose build --no-cache --progress=plain

down:
	docker-compose down --volumes --remove-orphans

down-yarn:
	docker-compose -f docker-compose.yarn.yml down --volumes --remove-orphans

run:
	make down && docker-compose up

run-scaled:
	make down && docker-compose up --scale spark-worker=2

run-d:
	make down && docker-compose up -d

run-yarn:
	make down-yarn && docker-compose -f docker-compose.yarn.yml up

run-yarn-scaled:
	make down-yarn && docker-compose -f docker-compose.yarn.yml up --scale spark-yarn-worker=2

stop:
	docker-compose stop

stop-yarn:
	docker-compose -f docker-compose.yarn.yml stop


submit:
	docker exec da-spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)

submit-da-book:
	make submit app=data_analysis_book/$(app)

submit-yarn-test:
	docker exec da-spark-yarn-master spark-submit --master yarn --deploy-mode cluster ./examples/src/main/python/pi.py

submit-yarn-cluster:
	docker exec da-spark-yarn-master spark-submit --master yarn --deploy-mode cluster ./apps/$(app)

rm-results:
	rm -r book_data/results/*


#yarn application -kill application_1704383676367_0001    
#./bin/spark-submit --master yarn --deploy-mode cluster --driver-memory 1g --executor-memory 1g --num-executors 1 --executor-cores 1 --conf spark.dynamicAllocation.enabled=false apps/test2.py

# docker exec -it ded8a4ebda57 cqlsh
# USE coinhub_2;
# DESCRIBE TABLES;
# select * from tweet_trending