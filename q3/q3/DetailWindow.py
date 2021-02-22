from q3.Element import Element

class DetailWindow(Element):
    def __init__(self,*args, **kwargs):
        tparent = self._initHandleArg('parent',
            kwargs = kwargs,
            default = None,
            desc = 'Optional parent if nested/embeded ?'
            )
        self._event = None
        super(DetailWindow, self).__init__(tparent)

    def setEvent(self, event):
        self._event = event

    def show(self):
        self.q3D().doDetailWindow_Show()

    