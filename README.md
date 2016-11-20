## INFO

Rest API to post and consume reviews

## SETUP

You need docker, get it here: [docker](https://www.docker.com/)

### Build the containers

```docker-compose build web```

### Run the migrations

```docker-compose run web sh /code/migrate```


### Run the tests

```docker-compose run web sh /code/test```

### Run the project

```docker-compose up web```
