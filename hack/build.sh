sudo sysctl -w vm.max_map_count=262144

make create-volumes
make build
docker-compose up -d

until ./wait-for-it.sh localhost:80; do sleep 1; done
until ./wait-for-it.sh localhost:8080; do sleep 1; done

until make bootstrap; do sleep 1; done

docker-compose down