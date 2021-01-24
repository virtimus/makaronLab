
#WqVector is a king of a list which can be consifered as sequence of elements with unchangable id
#The list have some additional features like adding indexes and search by them
class WqVector:
    def __init__(self):
        self._list = {}
        self._indexes = {}
        pass

    def __iter__(self):
        return self._list.__iter__()

    def __next__(self):
        return self._list.__next__()

    #count of list elements
    def count(self):
        return len(self._list)
    
    def __len__(self):
        return self.count()
    
    def raiseExc(self, a0):
        raise Exception(a0)

    def _buildIndex(self, attr:str):        
        nIndex = {}
        for e in self._list:
            el = self._list[e]
            tkey = getattr(el,attr)
            if callable(tkey):
                tkey = tkey()            
            nIndex[tkey]=el #currently index always unique - elements with same attr value override
        self._indexes[attr]= nIndex
    
    def _updateIndexes(self, el):
        for attr in self._indexes:
            ind = self._indexes[attr]
            tkey = getattr(el,attr)
            if callable(tkey):
                tkey = tkey()
            ind[tkey]=el

    def by(self, attr:str, value=None):
        if not attr in self._indexes: #we don't have index - build it
            self._buildIndex(attr)  
        result = self._indexes[attr]
        if value == None:
            return result
        result = result[value] if value in result else None
        return result

    def byId(self, lid:int):
        return self.by('id',lid)

    # append element to the list if there is no element with given id
    # else - raise exception
    def append(self, lid:int, element):
        if lid < len(self._list) and self._list[lid] != None:
            self.raiseExc('[WqVector] append failed - element with id({id}) already in list')
        else:
            self._list[lid]=element
            self._updateIndexes(element) 




