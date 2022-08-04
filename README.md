# Site

## Setup

1. Install `gcloud` cli.
2. Setup `gcloud auth login`
3. `gcloud auth configure-docker`

### Build Container

```
docker build -t super-magazine:latest .
```

### Run container locally

```
docker run -it -p 5002:5002 super-magazine:latest
```

### Tag container for push

```
docker tag super-magazine:latest gcr.io/super-magazine/deployment/site:latest
```

### Show all local containers

```
docker container ls -a
```

### Push container to Container Registry

```
docker push gcr.io/super-magazine/deployment/site:latest
```