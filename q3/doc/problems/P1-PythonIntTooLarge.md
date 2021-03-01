## Got:

Exception in thread Thread-3:
OverflowError: Python int too large to convert to C long

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.6/threading.py", line 864, in run
    self._target(*self._args, **self._kwargs)
  File "/src/makaronLab/q3/q3/drivers/sim/ModuleImplGraph.py", line 257, in dispatchThreadFunction
    self.calculate()
  File "/src/makaronLab/q3/q3/drivers/sim/ModuleImplGraph.py", line 194, in calculate
    element.calculate()
  File "/src/makaronLab/q3/q3/Module.py", line 595, in calculate
    calc()
  File "/src/makaronLab/q3/q3/Q3Chips/ModuleImpl6522.py", line 232, in calc
    'iv':self._opened['iv']
SystemError: <built-in function c6522> returned a result with an error set

## research

Definitely kind of overflow. Did I used wrong types on c side ? Let's check

Problem occured in call
 q3c.c6522({'command':'calc',

after mounting monitor fun to 6522 (video2.md) got this trace:

 monFun6522:0x3c0000000001
monFun6522:0x3c000100000d
monFun6522:0x3c000100000c
monFun6522:0x3c000100000b
monFun6522:0x3d0000ea000e
monFun6522:0x3d0004ea000f
monFun6522:0x3d0004ea000a
monFun6522:0x80003d0004ea000b

looks like last value is big (8 bytes) but not too big for 64 bit - wrong type in C?


## Solution:

Well, I've just reached system limit sys.maxsize (which is on my 64bit machine 2^63-1 I think)

9223372036854775807

it's lower than max 64 bit (unsigned) value of 2^64-1

18446744073709551615

(because of sign bit probably)


So - the simplest solution seems to be to introduce a divider/bitshifter...

Well or maybe converting to string - seems to be nicer - don't know if faster ...


https://www.cs.brandeis.edu/~gim/Papers/fast_d2b.pdf

but simpler to implement - I'm lazy man :)

So - let's do it ! got code from sample above, changed to handle 64 bits and direct string conversion (char array + asci offset) - b2d.c

 currently little endian bit string - 'lebin' passed instead of 'pins'
 maybe lehex would be nicer ... but nevertheless it's transport-only repr - so = no matter ..


