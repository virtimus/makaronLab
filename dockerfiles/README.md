## To build && test docker devEnv:
```
cd /src/makaronLab/dockerfiles/mlab-dev && sudo docker build -t mlab-dev .
sudo docker run -d -p 5389:3389 --rm --name mlab-dev mlab-dev

sudo docker exec -it -u ths mlab-dev /bin/bash -c 'cd /src/makaronLab/install; sudo ./bootstrap-dev.sh'
```
(default password of ths user is "pass")

Building distribution package:
```
cd /src/makaronLab/install && ./build-dist.sh
```



## To build && test docker userEnv:

cd /src/makaronLab/dockerfiles/mlab-usr && sudo docker build -t mlab-usr .
sudo docker run -d -p 6389:3389 --rm --name mlab-usr mlab-usr

sudo docker exec -u ths mlab-usr /bin/bash -c 'cd /tmp/makaronLab; ./setup.sh'

(this will display something like "Could not connect to any X display")

sudo docker exec -u root mlab-usr /bin/bash -c 'cp -R /home /home.backup; chown -R ths /home.backup/ths'
sudo docker exec -u root mlab-usr /bin/bash -c 'echo "cp -R /home.backup/* /home; chown -R ths /home/ths" > /i3c/i3c/run-startup-after.sh'

(app should be available inside container)

sudo docker commit mlab-usr  mlab-usr
 
sudo docker stop mlab-usr
docker tag mlab-usr virtimus/mlab-usr
docker push virtimus/mlab-usr


