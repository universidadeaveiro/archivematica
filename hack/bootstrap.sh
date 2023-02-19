sudo sysctl -w vm.max_map_count=262144

make create-volumes
./build.sh -a
docker-compose up -d

until ./wait-for-it.sh localhost:80; do sleep 1; done
until ./wait-for-it.sh localhost:8000; do sleep 1; done

until sudo make bootstrap-all; do sleep 1; done

docker-compose down