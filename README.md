## There were few reasons for this project.

First is wonderfull series of videos from Ben Eater on building 8bit cumputer from scratch.

https://eater.net/8bit

It was an inspiration for me to try and do the same using some simulation.

Trying to simulate Ben's series I haven't found anything that would be really usable.

Closest was wonderful simulator "Spaghetti" by  Artur Wyszyński (aljen) 

https://github.com/aljen/spaghetti

I had to tune it a little bit, add some additional features and to prepare a library of specialised components to simulate CPU.

[Other reasons](doc/reasons.md)

Here are some screenshots from my build and detailed description of steps I've took.

[Bens SAP-1 build using simulation](doc/Bens8bit.md)

![cpu-EI-part8](../packages/cpu-EI-part8.png)

## Getting started

Currently makaronLab is Linux based - I think that in the era of docker this is no longer any problem.

If You're stucked with Windows (like I was for many years ...) it really a good occasion to leave the cave ... 

### You can simply run it using docker image containing Linux Mint Desktop and makaronLab (release version) preinstalled:
```
sudo docker run -d -p 6389:3389 --rm --name mlab-usr virtimus/mlab-usr
```
Running container "mlab-usr" can be accesses by standard rdp client (like mstsc under Windows)

Default user/password is "ths/pass"

### If You prefer to go deeper - compile it Yourself under Ubuntu 18.04 or Linux Mint - it is as simple as:
```
mkdir -p /src && cd /src && git clone http://github.com/virtimus/makaronLab && cd makaronLab/install && ./bootstrap-dev.sh
```
### You can also use standarised development environment available as Docker container:
```
sudo docker run -d -p 5389:3389 --rm --name mlab-usr virtimus/mlab-dev
```
it is ok to make a volume at /src and clone fresh sources from github
