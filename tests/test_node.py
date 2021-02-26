from eaf.node import Node


def test_node():
    node = Node()
    assert node.parent is None
    assert node.nodes == []

    sub1 = Node()
    sub12 = Node()
    sub22 = Node()

    sub1.add([sub12, sub22])
    assert sub1.nodes == [sub12, sub22]
    assert sub12.parent is sub1
    assert sub22.parent is sub1

    node.add(sub1)
    assert sub1.parent is node
    assert node.nodes == [sub1]


def test_node_traversal():
    """

    root
      sub1
        sub11
        sub12
      sub2
      sub3
        sub31
        sub32
          sub321
    """
    node = Node("root")
    sub1 = Node("sub1")
    sub11 = Node("sub11")
    sub12 = Node("sub12")
    sub1.add([sub11, sub12])
    node.add(sub1)
    sub2 = Node("sub2")
    sub3 = Node("sub3")
    sub31 = Node("sub31")
    sub32 = Node("sub32")
    sub321 = Node("sub321")
    sub32.add(sub321)
    sub3.add([sub31, sub32])
    node.add([sub2, sub3])

    subnodes_breadth = [sub1, sub2, sub3, sub11, sub12, sub31, sub32, sub321]
    subnodes_depth = [sub1, sub11, sub12, sub2, sub3, sub31, sub32, sub321]

    assert list(node.traverse_breadth()) == subnodes_breadth
    assert list(node.traverse_breadth(with_root=True)) == [node] + subnodes_breadth

    assert node.traverse_depth() == subnodes_depth
    assert node.traverse_depth(with_root=True) == [node] + subnodes_depth


def test_node_tagging():
    node = Node("the-node")

    assert node.tags == set()

    node.tag("tag1")
    node.tag("tag2")

    assert node.tags == {"tag1", "tag2"}

    node.untag("tag1")
    assert node.tags == {"tag2"}
