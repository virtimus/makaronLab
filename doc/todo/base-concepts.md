Spaghetti is great but I don't like the model structure for simulation - especially:

1. Inputs on left ouputs on righ on separate vectors
I think it should be one list of "pins" containing inside some info is it input/output or maybe dynamic and current role ?

2. Connections and signal multiplication/redundancy
Currently there are some (I think) redundancy in design.
Node (Sockets)input/output -> Element -> (IOSockets)input/output -> source id -> connection -> target id -> (IOSockets)input/output -> Element -> Node -> (Sockets)input/output 

Maybe for serialisation it's ok but in memory there shoud be something more simple and effective.
I think much simpler (and faster) would be two layer graph something like:

Model Layer Graph:
GSignal(value, vector of pins references, one pin reference as signal source) -> n -> GItem(+pins with signals references)
- simple vector of values (boolean and/or composite) as "single source of true". Items, pins and signals as groups of references to this vector.
- simple state storage (just seqence of values) 
- memory effective
- more advanced algorithm od calculation 

View Layer Graph 
GVItem(containing reference to GItem) as Node -> collection of edges (with reference to GSignal) as connections
- MLG/VLG could be processed using some graph db (like Neo4j or OrientDB)
- better separated simulation (model) and presentation (view) levels