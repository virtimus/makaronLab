## To build && test docker devEnv:
```
cd /src/makaronLab/dockerfiles/mlab-dev && sudo docker build -t mlab-dev .
sudo docker run -d -p 5389:3389 --rm --name mlab-dev mlab-dev

sudo docker exec -it -u ths mlab-dev /bin/bash -c 'curl -sSL https://raw.githubusercontent.com/virtimus/makaronLab/master/install/bootstrap-dev.sh | sudo MLAB_BS_SKIP_SRC=1 bash'
sudo docker exec -u root mlab-dev /bin/bash -c 'cp -R /home /home.backup; chown -R ths /home.backup/ths'
sudo docker exec -u root mlab-dev /bin/bash -c 'echo "[ ! -e /home/ths ] && cp -R /home.backup/* /home; chown -R ths /home/ths" >> /run-startup.sh'

sudo docker commit mlab-dev  mlab-dev
sudo docker stop mlab-dev
docker tag mlab-dev virtimus/mlab-dev
docker push virtimus/mlab-dev

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
sudo docker exec -u root mlab-usr /bin/bash -c '[ ! -e /home/ths ] && echo "cp -R /home.backup/* /home; chown -R ths /home/ths" > /i3c/i3c/run-startup-after.sh'

(app should be available inside container)

sudo docker commit mlab-usr  mlab-usr
 
sudo docker stop mlab-usr
docker tag mlab-usr virtimus/mlab-usr
docker push virtimus/mlab-usr


