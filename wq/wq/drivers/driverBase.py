

class WqDriverBase:
    def __init__(self,_self,parent,impl):
        #self._wqImpl = wqImpl
        self._object = impl
        self._impl = impl
        self._parent = parent
        self._self = _self

    def s(self):
        return self._self
    
    def impl(self):
        return self._impl

    def pimpl(self):
        return self._parent.impl()
    
    def p(self):
        return self._parent

    def callAfterInit(self, tImpl):
        if hasattr(tImpl,'__afterInit__'):
            ai = getattr(tImpl,'__afterInit__')
            if callable(ai):
                ai(self)
