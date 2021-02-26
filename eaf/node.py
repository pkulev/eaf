"""Scene graph implementation."""

from __future__ import annotations

from collections import deque
from typing import List, Optional, Union


class Node:
    """Tree data structure.

    Allows to pass any data via kwargs.
    """

    def __init__(self, name: Optional[str] = None):
        self._parent = None
        self._nodes = []
        self._name = name if name is not None else self._default_name()

        self._tags = set()

    @property
    def id(self):
        """Identificator, used for searching and deleting."""

        return id(self)

    @property
    def parent(self) -> Optional[Node]:
        """Node's parent getter.

        Root node has parent `None`.
        """

        return self._parent

    @parent.setter
    def parent(self, parent: Node):
        """Node's parent setter."""

        self._parent = parent

    @property
    def nodes(self) -> List[Node]:
        """List of node-level children (subnodes)."""

        return self._nodes

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

    def add(self, node: Union[Node, List[Node]]):
        """Add node or list of nodes to the tree."""

        nodes = list(node) if isinstance(node, list) else [node]

        for sub in nodes:
            sub.parent = self
            self.nodes.append(sub)

    # TODO:
    def remove(self, node):
        for sub in self.traverse_breadth():
            if sub.id == node.id:
                sub.parent.nodes.remove(sub)
                sub.parent = None
                del sub

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
            for sub in node.nodes:
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
            if not node.nodes:
                pass
            else:
                for sub in node.nodes:
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
    def _default_name(cls):
        """Default name for node instantiation."""

        return cls.__name__

    def __str__(self):
        return f"{self.__class__.__name__}[{self.name}]"

    __repr__ = __str__
