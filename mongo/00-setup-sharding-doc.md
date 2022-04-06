## Set up Sharding using Docker Containers
docker volume prune
docker network create lab-4

### Config servers
Start config servers (3 member replica set)
```
docker-compose -f config-server/docker-compose.yaml up -d

docker ps

docker volume ls
```
Initiate replica set
```
login to one machine
docker network inspect lab-2
docker exec -it cfgsvr1 bash
mongosh
```
```
rs.initiate(
  {
    _id: "cfgrs",
    configsvr: true,
    members: [
      { _id : 0, host : "172.18.0.2:27017" },
      { _id : 1, host : "172.18.0.3:27017" },
      { _id : 2, host : "172.18.0.4:27017" }
    ]
  }
)

rs.status()
mongo mongodb://172.18.0.2,172.18.0.3,172.18.0.4/\?replicaSet=cfgrs
```

### Shard 1 servers
Start shard 1 servers (3 member replicas set)
```
docker-compose -f shard1/docker-compose.yaml up -d
```
Initiate replica set
```
docker exec -it shardsvr1 bash
mongosh
```
```
rs.initiate(
  {
    _id: "shard1rs",
    members: [
      { _id : 0, host : "172.18.0.8:27017" },
      { _id : 1, host : "172.18.0.6:27017" },
      { _id : 2, host : "172.18.0.7:27017" }
    ]
  }
)

rs.status()
mongo mongodb://172.19.0.2,172.19.0.3,172.19.0.4/\?replicaSet=shard1rs
```

### Mongos Router
Start mongos query router
```
docker run -d -p 35000:27017 -v data:\data\db --network="lab-4" mongo
mongos --configdb cfgrs/172.18.0.2:27017,172.18.0.3:27017,172.18.0.4:27017 --port 27011

docker-compose -f mongos/docker-compose.yaml up -d
```

### Add shard to the cluster
Connect to mongos
```
docker exec -it {mongos} bash
mongsh localhost:27011 // to connect to mongosh
```
Add shard
```
mongos> sh.addShard("shard1rs/172.18.0.8:27017,172.18.0.6:27017,172.18.0.7:27017")
mongos> sh.status()
```
## Adding another shard
### Shard 2 servers
Start shard 2 servers (3 member replicas set)
```
docker-compose -f shard2/docker-compose.yaml up -d --force-recreate
```
Initiate replica set
```
docker exec -it shard2svr1 bash
```
```
rs.initiate(
  {
    _id: "shard2rs",
    members: [
      { _id : 0, host : "172.18.0.9:27017" },
      { _id : 1, host : "172.18.0.10:27017" },
      { _id : 2, host : "172.18.0.11:27017" }
    ]
  }
)

rs.status()
```
### Add shard to the cluster
Connect to mongos
```
mongosh localhost:27011 // to connect to mongosh
```
Add shard
```
mongos> sh.addShard("shard2rs/172.18.0.9:27017,172.18.0.10:27017,172.18.0.11:27017")
mongos> sh.status()
```




##Sharding a collection

use sharddemo // create a database
db.sharddemo.createCollection("seng468")
db.sharddemo.createCollection("seng468t")

sh.enableSharding("sharddemo")
sh.shardCollection("sharddemo.seng468", {"name":"hashed"})
db.seng468.getShardDistribution()


### Lets insert some data
exit
for i in {1..50}; do echo -e "use sharddemo \n db.seng468.insertOne({\"name\": \"test $i\", \"language\": \"english\"})" | mongo mongodb://localhost:27011; done

mongosh localhost:27011
db.seng468.getShardDistribution()


### What if DB already has documents?
for i in {1..50}; do echo -e "use sharddemo \n db.seng468t.insertOne({\"name\": \"test $i\", \"language\": \"english\"})" | mongo mongodb://localhost:27011; done
Index has to be created with the proposed shard key to shard.

db.seng468t.createIndex({"name": 1})