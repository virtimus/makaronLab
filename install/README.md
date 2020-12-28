

cd /src/makaronLab/dockerfiles/mlab-usr && sudo docker build -t mlab-usr .
sudo docker run -d --rm --name mlab-usr mlab-usr