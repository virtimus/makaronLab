
# wxWidget

import wx

class Q3Driver:
    def __init__(self,_self,parent,impl):
        self._impl = impl
        self._parent = parent
        self._self = _self

    def doApp_Init(self):
        result = wx.App()
        return result

    def doMainWindow_Init(self):
        result = wx.Frame(None,title=title)
        return result

    def doMainWindow_Show(self):
        result = self.impl().Show()   
        return result                 

    def _Menu_Append(self, a0, a1=None, a2=None):
        if (a1 == None):
            return self._self._menu.Append(a0)
        else:
            return self._self._menu.Append(a0, a1, a2)

    def doMenu_Init(self):
        if self._impl == None:    
            self._self._wxMenu = wx.Menu()
            self._self._menu = self._self._wxMenu
            #parent.implObject().Append(self._wxMenu)
        else:
            self._self._menu = self._impl
        return  self._self._menu  


    def doMenu_AddSeparator(self):
        result = self._self.implObject().AppendSeparator() 
        return result  

    def doMenu_addAction(self, label,id,helpStr,onClick):
        if id == None:
            id = -1
        result = self._Menu_Append(id,label, helpStr)
        self._self.implObject().Bind(wx.EVT_MENU, onClick, result)
        return result  

    def doMdiPanel_Init(self):      
        result = wx.Panel(self._parent.implObject())
        return result  

    def doTabPanel_Init(self):        
        self._self.raiseNoImpl('pyqt5.Q3Driver','doTabPanel_Init -> noImpl')

    def doTab_Init(self):        
        self._self.raiseNoImpl('pyqt5.Q3Driver','doTab_Init -> noImpl')

    def doMenuBar_Init(self):        
        result = wx.MenuBar()
        self.pimpl().SetMenuBar(result)
        return result
    
    def doLayout_Init(self):
        orient = self.s()._kwargs['orient'] if 'orient' in self.s()._kwargs else orientation.HORIZONTAL
        result = wx.BoxSizer(orient)
        self.pimpl().SetSizer(result) 

    def doLabel_GetFont(self):
        result = self.impl().GetFont()
        return result
    
    def doLabel_SetFont(self, font):    
        result = self.impl().SetFont(font)
        return result
