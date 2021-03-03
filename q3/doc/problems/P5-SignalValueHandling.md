I've implemented signal monitoring with modifications and it revealed some problems with signal value handling

- first is size is not validated (handy for development but to be fixed)
- None value probably not handled well (I think it should not be propagated - thats how 3rd state should be implemented ?)
- switching via double click on an output converts to boolean(minor)
