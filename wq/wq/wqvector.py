
#WqVector is a king of a list which can be consifered as sequence of elements with unchangable id
#The list have some additional features like adding indexes and search by them
class WqVector:
    def __init__(self, cls=None):
        self._cls = cls
        self._list = {}
        self._indexes = {}
        self._nextId = 0
        pass

    def __iter__(self):
        return self._list.__iter__()

    def __next__(self):
        return self._list.__next__()

    #count of list elements
    def count(self):
        return len(self._list)
    
    def size(self):
        return self.count()
    
    def __len__(self):
        return self.count()
    
    def raiseExc(self, a0):
        raise Exception(a0)

    def _validateCls(self, element):
        if self._cls == None:
            return
        if not isinstance(element,self._cls):
            self.raiseExc('[WqVector] element given of wrong class')

    def _getattr(self, el, attr:str):
        tval = getattr(el,attr)
        if callable(tval):
            tval = tval()
        return tval

    def _buildIndex(self, attr:str):        
        nIndex = {}
        for e in self._list:
            el = self._list[e]
            if el != None:
                tkey = self._getattr(el,attr)
                if tkey != None:            
                    nIndex[tkey]=el #currently index always unique - elements with same attr value override
        self._indexes[attr]= nIndex
    
    def _rebuildIndexes(self):
        for ik in self._indexes:
            self._buildIndex(ik)
    
    def _updateIndexes(self, el):
        for attr in self._indexes:
            ind = self._indexes[attr]
            tkey = self._getattr(el,attr)
            if tkey != None:
                ind[tkey]=el

    def _updateNextId(self, lid:int):
        if self._nextId<lid:
            self._nextId=lid

    def by(self, attr:str, value=None):
        if not attr in self._indexes: #we don't have index - build it
            self._buildIndex(attr)  
        result = self._indexes[attr]
        if value == None:
            return result
        result = result[value] if value in result else None
        return result

    def filterBy(self, attr:str, value):
        result = WqVector(self._cls)
        for lid in self._list:
            el = self._list[lid]
            if el != None:
                tval = self._getattr(el,attr)
                if (tval == value):
                    result.append(lid,el)
        return result
    
    def clearBy(self, attr:str, value):
        for lid in self._list:
            el = self._list[lid]
            if el != None:
                tval = self._getattr(el,attr)
                if (tval == value):
                    self._list[lid]=None



    def byLid(self, lid:int):
        result = self._list[lid] if lid in self._list else None
        return result #self.by('id',lid)

    def byId(self,id:int):
        result = self.by('id',id)
        return result

    # append element to the list if there is no element with given id
    # else - raise exception
    def append(self, lid:int, element):
        self._validateCls(element)
        if lid  in self._list and self._list[lid] != None:
            self.raiseExc('[WqVector] append failed - element with id({id}) already in list')
        else:
            self._list[lid]=element
            self._updateNextId(lid+1)
            self._updateIndexes(element) 

    def push_back(self, element):
        self._validateCls(element)
        self._list[self._nextId] = element
        result = self._nextId
        self._updateNextId(self._nextId+1)
        self._updateIndexes(element)
        return result

    def remove(self, element,**kwargs):
        result = None
        indexUpdate = not kwargs['noIndexUpdate'] if 'noIndexUpdate' in kwargs else True
        for lid in self._list:
            if (element == self._list[lid]):
                result = self._list[lid]
                self._list[lid] = None
        if (result != None and indexUpdate):
            self._rebuildIndexes()
        return result

    def removeByLid(self, lid:int,**kwargs):
        el = self.byLid(lid)
        if el != None:
            el = self.remove(el,**kwargs)
            if (el == None):
                self.raiseExc('Problem with removing element from vector')
        return el


    def last(self):
        result = list(self._list.keys())[-1] if len(self._list.keys())>0 else None
        result = self._list[result] if result != None else None
        return result
        
    def first(self):
        result = list(self._list.keys())[0] if len(self._list.keys())>0 else None
        result = self._list[result] if result != None else None
        return result   

    #return easy iterable list of values without empty slots as default
    def values(self):
        result = list(filter(None, self._list.values()))
        return result







