# BEGIN

docker pull postgres
docker run --name taipan-db -e POSTGRES_PASSWORD=mysecretpassword -d postgres
docker exec taipan-db runuser -l postgres -c 'psql'

# END
