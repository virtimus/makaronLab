## There were few reasons for this project.

First is wonderfull series of videos from Ben Eater on building 8bit cumputer from scratch.
https://eater.net/8bit
It was an inspiration for me to try and do the same using some simulation.
Trying to simulate Ben's series I haven't found anything that would be really usable.
Closest was wonderful simulator "Spaghetti" by  Artur Wyszyński (aljen) 
https://github.com/aljen/spaghetti
I had to tune it a little bit, add some additional features and to prepare a library of specialised components to simulate CPU.

Second is a sad fact, that (I think) we're stucked in 70'ties if it concerns cpu architecture.
https://www.youtube.com/watch?v=sK-49uz3lGg
Neither is it Harvard or Neuman or different modifications - the base concepts are still the same.
We still use alu, registers, centralised synchronic "busses" and clock based processing in sequence (with a bunch of additional optmisation techniques like caches or out of order processing)
Is it CISC or RISC - all this is just deviations from one common aproach.
My thought was - it is miserable. Is it all that can be achived ?
Or we're just in hands of few monopolistic companies ? 
Some hope is new RISC-V open source processor movement.
It is very nice fresh design - but it is still just opensourcing classical aproach.

Can't it be that there are other aproaches possible ?
IE distributed one with easy scalable subcomponents calculating one simple thing ?
Or: clockless one - working with smooth speed not in a rythm of "Paradeschritt" ?
Or: neural network like ?
Or: hierarchical one organized like LISP - to take over subsequent layers of compilation ? 
Or: non-binary one - based on chips with more states/voltage than just 2 ?
Or ... ? Who knows what's yet in there ?
Why we are sitting still in the cave ? Just because of tons of code and systems writen ?
Could we recompile them to new hardware ?

RISC-V opened possibility of producing custom cpus using classicach architecture,
I think it is not enough. There is a need to give people easy start for designing and simulating completely new aproaches.

makaronLab is (or rather I woud say may be) a tool to achieve this.


## Getting started

Currently makaronLab is Linux based - but in the era of docker this no longer any problem.

You can simply run it using docker image containing Linux Mint Desktop and makaronLab preinstalled:


If You prefer to go deeper - compile it Yourself - it is as simple as:
mkdir -p /src && cd /src && git clone http://github.com/virtimus/makaronLab && cd makaronLab/install && ./bootstrap-dev.sh


You can also use standarised development environment available as Docker container:
