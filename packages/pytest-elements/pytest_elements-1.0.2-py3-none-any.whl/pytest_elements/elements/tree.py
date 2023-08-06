"""
Description: A tree of PageElement instances with some additional tricks.
"""
from pytest_elements.elements.null_element import NullElement
from collections import deque


class Tree:
    """
    A tree of PageElement instances.
    """

    def __init__(self, root=None):
        self.root = root if root else NullElement()

    def grow(self, *new_leaves, from_node=None):
        """
        Adds a new layer of leaves to the tree.
        """
        # new_leaves is a list of 'leaf groups',
        # 1 group for each leaf currently on the tree.
        leaves = self.get_leaves(from_node=from_node)
        if not len(new_leaves) == len(leaves):
            raise ValueError(
                f"Incorrect number of leaf groups.\n" f"Expected: {len(leaves)}\n" f"Got: {len(new_leaves)}"
            )
        else:
            # Add each leaf group as the children of the existing 'leaf'
            for leaf_group, old_leaf in zip(new_leaves, leaves):
                old_leaf.next_set = leaf_group
                for new_leaf in leaf_group:
                    new_leaf.prev_node = old_leaf

    def walk(self, from_node=None):
        """
        Returns each node of a tree,
        starting at the specified node, or root if unspecified.
        """
        elements = []
        walk_queue = deque([from_node if from_node else self.root])
        while walk_queue:
            element = walk_queue.popleft()
            elements.append(element)
            walk_queue.extend(element.next_set)
        return elements

    def get_leaves(self, from_node=None):
        """
        Returns the leaf nodes of the tree, starting at the specified node, or root if unspecified.
        """
        return [node for node in self.walk(from_node=from_node) if not node.next_set]
