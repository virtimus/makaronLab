
from .ModuleImplElement import ModuleImplElement

#inputs/outputs of open graph
class ModuleImplIO(ModuleImplElement):
    def __init__(self, **kwargs):
        super(ModuleImplIO, self).__init__(**kwargs)