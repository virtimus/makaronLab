#import check_pypi_name
#import check_pypi_name
#check_pypi_name.check_pypi_name('wqc')


from pypi_name import pypiName

print(pypiName('wqs')) # False
print(pypiName('q3')) # True 
print(pypiName('q3c')) # True



print(pypiName('ws')) # False
print(pypiName('ws')) # True 
print(pypiName('vs')) # False
print(pypiName('ps')) # True 
print(pypiName('ml')) # False
print(pypiName('mlab')) # True 
