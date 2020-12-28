## To build && test devEnv:
```
cd /src/makaronLab/dockerfiles/mlab-dev && sudo docker build -t mlab-dev .
sudo docker run -d -p 5389:3389 --rm --name mlab-dev mlab-dev

sudo docker exec -u ths mlab-dev /bin/bash -c 'cd /tmp/makaronLab/install; echo "pass\n" | sudo ./bootstrap-dev.sh'
```

## To build && test userEnv:

cd /src/makaronLab/dockerfiles/mlab-usr && sudo docker build -t mlab-usr .
sudo docker run -d -p 6389:3389 --rm --name mlab-usr mlab-usr

sudo docker exec -u ths mlab-usr /bin/bash -c 'cd /tmp/makaronLab; ./setup.sh'
(this will display something like "Could not connect to any X display")


sudo docker stop mlab-usr



