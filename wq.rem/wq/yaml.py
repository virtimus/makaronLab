import yaml

from collections import OrderedDict

from .dict import UnsortableOrderedDict
'''
class _CustomAnchor(yaml.Dumper):
  anchor_tags = {}
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.new_anchors = {}
    self.anchor_next = None
  def anchor_node(self, node):
    if self.anchor_next is not None:
      self.new_anchors[node] = self.anchor_next
      self.anchor_next = None
    if isinstance(node.value, str) and node.value in self.anchor_tags:
      self.anchor_next = self.anchor_tags[node.value]

    super().anchor_node(node)

    if self.new_anchors:
      self.anchors.update(self.new_anchors)
      self.new_anchors.clear()

def CustomAnchor(tags):
  return type('CustomAnchor', (_CustomAnchor,), {'anchor_tags': tags})

#print(yaml.dump(foo, Dumper=CustomAnchor({'a': 'a_name'})))

'''
#not working
#yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(OrderedDict, represent_ordereddict)

def dump(subj,stream,**kwargs):
    #kwargs['Dumper'] = CustomAnchor({'modules': 'a_module'})
    yaml.dump(subj,stream,**kwargs)