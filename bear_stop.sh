docker-compose stop
docker stop $(docker ps -q --filter "name=p0larbear")
docker rm $(docker ps -q --filter "name=p0larbear")
docker rm $(docker ps -a -q)