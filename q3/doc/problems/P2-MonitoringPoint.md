# wrong monitoring point

# after implementing external ram/rom it occured that monitoring function was put in wrong place 

The problem was that after implementing rom as external component signals were read on not fized state (ie CPU ordered 'read' but it was not done yet)

- changed to solution with some delay (=5 video2.py/monCalcFun) to let the sim stabilize
