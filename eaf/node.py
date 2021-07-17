"""Scene graph implementation."""

from __future__ import annotations

from collections import deque
from typing import List, Optional, Union


class OnNodeMixin:
    """Callback interface for nodes.

    Methods are called by the Tree object on particular node actions.
    """

    def on_node_add(self):
        """Node add callback.

        Called when node is added to the tree.
        """

    def on_node_remove(self):
        """Node remove callback.

        Called when node is removed from the tree.
        """

    def on_node_reparent(self, new_parent: Node):
        """Node reparent callback.

        Called when node is reparented to the other node.
        """

    def on_node_tag(self, tag):
        """Node tag callback.

        Called when node is tagged.
        """

    def on_node_untag(self, tag):
        """Node untag callback.

        Called when node tag is removed.
        """


class TreeDelegateMixin:

    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, tree):
        self._root = tree

    @property
    def parent(self) -> Optional[Node]:
        """Node's parent getter.

        Root node has parent `None`.
        """

        if self.root is None:
            return

        return self.root.parent_for(self)

    @parent.setter
    def parent(self, parent: Node):
        """Node's parent setter."""

        if self.root is None:
            return

        self.root.reparent(self, parent=parent)

    @property
    def children(self) -> List[Node]:
        """List of node's children."""

        if self.root is None:
            return

        return self.root.children_for(self)

    def add(self, children: Union[Node, List[Node]]):
        """Add node or list of nodes as children of this node instance."""

        nodes = children if isinstance(children, list) else [children]

        for sub in nodes:
            self.root.add(sub, parent=self)

    def remove(self, node: Union[Node, List[Node]]):
        """Remove node from the tree.

        Search is done via BFS comparing Node.id properties.

        :param node: tree node or list of nodes
        """

        if isinstance(node, list):
            node_ids = {item.id for item in node}
        else:
            node_ids = {node.id}

        for sub in self.traverse_breadth():
            if sub.id in node_ids:
                sub.parent.children.remove(sub)
                sub.parent = None
                del sub


class Node(OnNodeMixin, TreeDelegateMixin):
    """Tree node data structure.

    Supports OnNodeMixin interface allowing to setup own code to be called
    on certain actions.

    Each node has non-unique name attached, you can override naming behavior
    using `default_name_template` class variable and `generate_new_name`
    classmethod.

    For now nodes use behavior that kinda smells: on node insertion three that
    owns that node assigns itself to `__root__` variable. Thus node can delegate
    operations to the tree.
    """

    default_name_template = "Node"

    def __init__(self, name: Optional[str] = None):
        super().__init__()

        # This link will be set after node insertion
        self.__root__: Optional[Tree] = None

        self._name = name if name is not None else self.generate_new_name()

        self._tags = set()

    @property
    def id(self):
        """Identificator, used for searching and deleting."""

        return id(self)

    @property
    def name(self):
        """Name attached to node.

        Name is non-unique string identifier, serving as simple description.
        """

        return self._name

    @name.setter
    def name(self, value):
        """Node's name setter."""

        self._name = value

    @property
    def tags(self):
        """Copy of node's tag set."""

        return self._tags.copy()

    def traverse_breadth(self, with_root=False):
        """BFS (Breadth First Search) algorithm.

        Traverses nodes layer by layer.
        NOTE: Root node is not included.

        :param bool with_root: include root as first element
        """

        # self is the root node
        visited = {self}
        queue = deque([self])

        if with_root:
            yield self

        while queue:
            node = queue.popleft()
            for sub in node.children:
                if sub not in visited:
                    visited.add(sub)
                    queue.append(sub)
                    yield sub

    # TODO: implement lazy version
    def traverse_depth(self, with_root=False):
        """DFS (Depth First Search) algorithm.

        Traverses nodes branch by branch.
        NOTE: Root node is not included.

        :param bool with_root: include root as first element
        """

        visited = set()
        queue = []
        if with_root:
            queue.append(self)

        def collect_rec(node):
            if not node.children:
                pass
            else:
                for sub in node.children:
                    if sub not in visited:
                        visited.add(sub)
                        queue.append(sub)
                        collect_rec(sub)

        collect_rec(self)
        return queue

    def tag(self, node_tag: str):
        """Add tag to node's tag set.

        You can search by tags.
        """

        self._tags.add(node_tag)

    def untag(self, node_tag: str):
        """Remove tag from node's tag set."""

        self._tags.remove(node_tag)

    # TODO: ???
    def find(self, node):
        for sub in self.traverse_depth():
            if node is sub:
                return sub

    def find_one_by_name(self, name, required: bool = False):
        """Find single node by name.

        :param bool required: raises exception if True
        """

        for node in self.traverse_breadth():
            if node.name == name:
                return node

        if required:
            raise Exception(f"Node with name {name} not found")

    def find_many_by_name(self, name):
        for node in self.traverse_breadth():
            if node.name == name:
                yield node

    def find_by_tag(self, tag):
        for node in self.traverse_breadth():
            if tag in node.tags:
                yield node

    @classmethod
    def generate_new_name(cls):
        """Default name generator for the new node instance.

        You can override this behavior for adding numbers for non-unique names.
        """

        return cls.default_name_template

    def __str__(self):
        return f"{self.__class__.__name__}[{self.name}]"

    __repr__ = __str__


# class TreeView:

#     def __init__(self):
#         pass

#     def update(self):
#         pass


class Tree:
    """Acyclic graph which provides nodes tree structure and querying interface.

    Acyclic means that node can have only one relation.
    Tree supports adding, removing, tagging and querying nodes.
    """

    __id__ = "__tree_level_nodes__"

    def __init__(self):
        self._storage = {}
        self._graph = {}

    @property
    def id(self):
        return self.__id__

    def iterate_nodes(self):

        return self._storage.values()

    def add(self, node: Node, parent: Node = None):
        """Insert node into the tree.

        If parent is provided then all needed relations will be added too.
        Inserting node with already registered ID has no any effects.

        If you want to reparent already inserted node use `reparent` method.

        :param node: node to insert
        :param parent: parent node, must have `.id` property
        """

        if node.id in self._storage:
            return

        self._storage[node.id] = node

        if parent is None:
            parent = self

        self._graph.setdefault(parent.id, []).append(node.id)

        node.on_node_add()

    def remove(self, node: Node):
        """Remove node from the tree and cleanup it's relations.

        All nodes that have `node` as parent will be deleted too.
        Removing node which ID is not registered has no any effects.
        """

        if node.id not in self._storage:
            return

        self._storage.pop(node.id)
        sub_ids = self._graph.pop(node.id, None)
        #for self._graph

        node.on_node_remove()

    def parent_for(self, node: Node, required=True) -> Node:
        """Return parent node for the given one."""

        for parent_id, child_ids in self._graph.items():
            if node.id in child_ids:
                return self._storage[parent_id]

        if required:
            raise ValueError(f"No node with ID '{node.id}' was found")

    def children_for(self, node: Node, required=True):

        children_ids = self._graph.get(node.id, [])
        if required and not children_ids:
            raise ValueError(f"Node '{node.id}' has no children.")

        return [self._storage[child_id] for child_id in children_ids]

    def traverse_breadth(self):
        """BFS (Breadth First Search) algorithm.

        Traverses nodes layer by layer.
        """

        # self is the root node
        visited = {self}
        queue = deque([self])

        while queue:
            node = queue.popleft()
            for sub_id in self._graph.get(node.id, []):
                sub = self._storage[sub_id]
                if sub not in visited:
                    visited.add(sub)
                    queue.append(sub)
                    yield sub

    # TODO: implement lazy version
    def traverse_depth(self):
        """DFS (Depth First Search) algorithm.

        Traverses nodes branch by branch.
        """

        visited = set()
        queue = []

        def collect_rec(node):
            if not node.children:
                pass
            else:
                for sub in node.children:
                    if sub not in visited:
                        visited.add(sub)
                        queue.append(sub)
                        collect_rec(sub)

        collect_rec(self)
        return queue
