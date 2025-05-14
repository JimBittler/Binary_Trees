from __future__ import annotations  # needed to allow argument typing for BT_Node, specifically allow input parameter to BT_Node to be of type BT_Node

"""
This module contains binary tree node class and an sorted, unbalanced binary tree class.
BT_Node: node with contains a key-value pair, where nodes are expected to be sorted by keys.
BT_Tree: Sorted, unbalanced binary tree with methods including:
    • add and delete nodes
    • find nodes by key or index
    • print ascii representation of the binary tree or a specific branch
"""

"""
TODO:
1) Comments and docstrings:
    1.a) ✓ BT_Node
    1.b) ✓ BT_Tree
        1.b.i)      ✓ add
        1.b.ii)     ✓ add_recursive
        1.b.iii)    ✓ find
        1.b.iv)     ✓ find_recursive
        1.b.v)      ✓ find_kth
        1.b.vi)     ✓ find_kth_recursive
        1.b.vii)    ✓ print
        1.b.viii)   ✓ clear
        1.b.ix)     ✓ print_branch
    1.c) ✓ This module
2) ✓ add print_from_this_node(...)
    2.a) ✓ find should return a node or None
    2.b) ✓ find_kth should return a node or None
    2.c) ✓ I don't know if this is even useful.
3) Red-Black
    3.a) add color properties
    3.b) rotate function
    3.c) balance logic
4) ✓ Move test function to new file
5) Node clear method should cause:
    5.a) tree height recalculate
    5.b) node count recalculation
        5.b.i) parent.node_count -= self.node_count
        5.c.ii) apply recursively up to root
"""

class BT_Node():
    def __init__(self, key:float=None, value:any=None, parent:BT_Node=None, left_child:BT_Node=None, right_child:BT_Node=None, node_count:int=1):
        """
        Binary Tree Node object
        :param key: Numeric which dictates location of the node when added to an ordered binary tree. Does not need to be unique.
        :param value: Data stored in the node.
        :param parent: Parent node
        :param left_child: Left child node
        :param right_child: Right Child node
        :param node_count: Total number of nodes and child nodes. A node with no children is considered 1 node
        """
        self.key = key
        self.value = value
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.node_count = node_count

    def clear(self) -> None:
        """
        Clear all values from node. All child nodes will be cleared automatically by Python's Garbage Collection.
        :return: None
        """
        self.__init__()

class BT_Tree():
    def __init__(self, _root:BT_Node=None, _height:int=0):
        """
        Sorted, unbalanced, binary tree composed of BT_Node objects
        `Reference <https://stackoverflow.com/a/28864021>`__, StackOverflow.com user djra, accessed May 01, 2025
        :param _root: private parameter, root node of tree
        :param _height: private parameter, number of edges between root and deepest node
        """
        self._root = _root
        self._height = _height

    # Properties
    # --------------------------------
    @property
    def root(self) -> BT_Node:
        return self._root

    @property
    def height(self) -> int:
        return self._height

    @property
    def node_count(self) -> int:
        return self.root.node_count

    # Add node
    # --------------------------------
    def add(self, key:float=None, value:any=None) -> None:
        """
        Add node to the binary tree, sorted by its key.
        :param key: Numeric value which dictates location of the node when added to an ordered binary tree. Does not need to be unique.
        :param value: Data stored in the node.
        :return: None
        """
        # If the tree has no root, create one
        if self._root is None:
            self._root = BT_Node(key=key, value=value)
            self._root.node_count = 1 # root node now exists but has no children (is a leaf, or external)
            new_node_depth = 0

        # Else call private recursive add method
        else:
            new_node_depth = self._add_recursive(key=key, value=value, parent_node=self._root, new_node_depth=0)

        # Update tree height
        if new_node_depth > self._height:
            self._height = new_node_depth

    def _add_recursive(self, key:float, value:any, parent_node:BT_Node=None, new_node_depth:int=0) -> int:
        """
        Private method which adds a node to a sorted binary tree, sorted by its key. The correct location at which to
        add the node of found by calling this function recursively.
        :param key: Numeric which dictates location of the node when added to an ordered binary tree. Does not need to be unique.
        :param value: Data stored in the node.
        :param parent_node: parent node under which the new node will be added
        :param new_node_depth: depth of the new node (edges between node and root)
        :return: updated depth of the new node
        """
        # Increment search depth and parent node count
        new_node_depth +=1
        parent_node.node_count += 1

        # Inspect left child
        if key < parent_node.key:
            # If there is no left child, add a node with input key and value
            if parent_node.left_child is None:
                parent_node.left_child = BT_Node(key=key, value=value, parent=parent_node)
            # Else continue recursive search
            else:
                new_node_depth = self._add_recursive(key=key, value=value, parent_node=parent_node.left_child,
                                                     new_node_depth=new_node_depth)

        # else inspect right child
        else:
            # If there is no right child, add a node with input key
            if parent_node.right_child is None:
                parent_node.right_child = BT_Node(key=key, value=value, parent=parent_node)
            # Else continue recursive search
            else:
                new_node_depth = self._add_recursive(key=key, value=value, parent_node=parent_node.right_child,
                                                     new_node_depth=new_node_depth)

        # Return depth at which the new node was added
        return new_node_depth

    # Find Node By Key
    # --------------------------------
    def find_node(self, key:float=None, nearest:bool=False) -> BT_Node | None:
        """
        Find node whose key matches the input key.
        :param key: Numeric key to find in the binary tree.
        :param nearest: Flag, if true and the tree does not contain a node with the input key, the node with the
        nearest key will be returned, else None will be returned.
        :return: Node whose key matches the input key, or None if there is no match.
        """
        # If no key is passed, or tree has no root, return none
        if key is None or self.root is None:
            nearest_node = None
        # Else recursively search the tree beginning at the root node
        else:
            nearest_node = self._find_node(key=key, parent_node=self._root, nearest=nearest)

        # return nearest node
        return nearest_node

    def _find_node(self, key:float, parent_node:BT_Node=None, nearest:bool=False):
        """
        Private recursive search method to find node whose key matches the input key.
        :param key: Numeric value to find in the binary tree
        :param parent_node: Node being checked for matching key value
        :param nearest: Flag, if true and the tree does not contain a node with the input key, the node with the
        nearest key will be returned, else None will be returned.
        :return: Node whose key matches the input key, or None if there is no match.
        """
        # Check parent node key
        if key == parent_node.key:
            nearest_node = parent_node
        # Check left child key
        elif key < parent_node.key:
            # If no left child, return parent
            if parent_node.left_child is None:
                if nearest:
                    nearest_node = parent_node
                else:
                    nearest_node = None
            # Else, search left child recursively
            else:
                nearest_node = self._find_node(key=key, parent_node=parent_node.left_child, nearest=nearest)
        # Check right child key
        else:
            # If no right child, return parent
            if parent_node.right_child is None:
                if nearest:
                    nearest_node = parent_node
                else:
                    nearest_node = None
            # Else, search right child recursively
            else:
                nearest_node = self._find_node(key=key, parent_node=parent_node.right_child, nearest=nearest)

        # Check if parent node key is closer than child node
        if nearest and abs(parent_node.key - key) < abs(nearest_node.key - key):
            nearest_node = parent_node

        # Return nearest node
        return nearest_node

    # Find kth Node
    # --------------------------------
    def find_kth(self, kth:int=0) -> BT_Node | None:
        """
        Find the node with the kth index, when nodes are sorted in ascending order by key value.
        :param kth: position
        :return: node with the kth index, or None if tree is empty.
        """
        # Ensure kth is valid
        if kth > (self.node_count - 1) or kth < -self.node_count:
            raise IndexError("search index out of range")
        # Handle negative indices; i.e. negative indicates index from right, as is standard.
        elif kth<0:
            kth += (self.node_count + 1)

        # If no key is passed, or tree has no root, return none
        if self.root is None:
            kth_node = None
        # Root is the only node
        elif self.node_count == 1:
            kth_node = self.root
        # Recursively search tree
        else:
            kth_node = self._find_kth(kth=kth, parent_node=self.root)

        # Return node
        return kth_node

    def _find_kth(self, kth:int=0, parent_node:BT_Node=None) -> BT_Node:
        """
        Private recursive search method to Find the node with the kth index, when nodes are sorted in ascending order
        by key value.
        :param kth: position which is always valid due to preprocessing
        :param parent_node: Node being checked for matching key value
        :return: node with the kth index
        """
        # If there is a left child
        if parent_node.left_child is not None:
            # By definition, all nodes in the left branch have a key less than the parent. Therefore, if the left branch
            # has k nodes, the parent is in the kth position (not (k+1)th because zero indexing)
            if kth == parent_node.left_child.node_count:
                kth_node = parent_node
            # else if kth is less than the number of nodes in the left branch, the left branch must contain the kth node
            elif kth < parent_node.left_child.node_count:
                # Recursively call _find_kth(...) on the left branch
                kth_node = self._find_kth(kth=kth, parent_node=parent_node.left_child)
            # else, the right child must exist and kth must be in the right branch
            else:
                # Recursively call _find_kth(...) on the right branch, but reduce kth by the number of nodes in the left
                # branch plus one (due to the parent node)
                kth_node = self._find_kth(kth=(kth - parent_node.left_child.node_count - 1), parent_node=parent_node.right_child)

        # If there is no left child, and kth is zero, the parent node must be the kth node
        elif kth == 0:
            kth_node = parent_node
        # Else the right child must exist and contain the kth node
        else:
            # Recursively call _find_kth(...) on the right branch, but reduce kth by 1
            kth_node = self._find_kth(kth=(kth - 1), parent_node=parent_node.right_child)

        # Return the kth_node
        return kth_node

    # Print Tree
    # --------------------------------
    def print(self, print_key:bool=False, print_val:bool=True, max_print_height:int=4, inverted:bool=False, _node:BT_Node=None, _depth:int=0) -> list[str] | None:
        """
        Print the contents of the binary tree to console. Minor modification made to code authored by:
        `Reference <https://stackoverflow.com/a/49844237>`__, StackOverflow.com user Alan T., accessed May 04, 2025
        :param print_key: Flag, if true, node key will be included in output of tree
        :param print_val: Flag, if true, node value will be included in output of tree
        :param max_print_height: maximum height of the printed tree. If set to -1, entire tree will print.
        :param inverted: Flag, if true, invert display of tree, e.g. as would be appropriate for a family tree
        :param _node: Private parameter, current node from which key and value are extracted
        :param _depth: Private parameter, integer indicating depth of current node
        :return: None
        """
        # Get root if first call to function
        if _node is None:
            node=self.root
        else:
            node=_node

        # Extract data which is to be printed
        if print_key and not print_val:
            stringValue = str(node.key)
        elif not print_key and print_val:
            stringValue = str(node.value)
        elif print_key and print_val:
            stringValue = str(node.key) + ": " + str(node.value)
        else:
            stringValue = "•"

        # Print height
        if max_print_height < -self._height:
            max_print_height = 0
        elif max_print_height < 0:
            max_print_height = self._height + max_print_height + 1

        # Children
        leftNode = node.left_child
        rightNode = node.right_child

        stringValueWidth = len(stringValue)

        # recurse to sub nodes to obtain line blocks on left and right
        if leftNode is not None and _depth < max_print_height:
            leftTextBlock = self.print(print_key=print_key, print_val=print_val, max_print_height=max_print_height,
                                       inverted=inverted, _node=leftNode, _depth=_depth+1)
        else:
            leftTextBlock = []

        if rightNode is not None and _depth < max_print_height:
            rightTextBlock = self.print(print_key=print_key, print_val=print_val, max_print_height=max_print_height,
                                        inverted=inverted, _node=rightNode, _depth=_depth+1)
        else:
            rightTextBlock = []

        # count common and maximum number of sub node lines
        commonLines = min(len(leftTextBlock), len(rightTextBlock))
        subLevelLines = max(len(rightTextBlock), len(leftTextBlock))

        # extend lines on shallower side to get same number of lines on both sides
        leftSubLines = leftTextBlock + [""] * (subLevelLines - len(leftTextBlock))
        rightSubLines = rightTextBlock + [""] * (subLevelLines - len(rightTextBlock))

        # compute location of key or link bar for all left and right sub nodes
        #   * left node's key ends at line's width
        #   * right node's key starts after initial spaces
        leftLineWidths = [len(line) for line in leftSubLines]
        rightLineIndents = [len(line) - len(line.lstrip(" ")) for line in rightSubLines]

        # top line key locations, will be used to determine position of current node & link bars
        firstLeftWidth = (leftLineWidths + [0])[0]
        firstRightIndent = (rightLineIndents + [0])[0]

        # width of sub node link under node key (i.e. with slashes if any)
        # aims to center link bars under the key if key is wide enough
        #
        # ValueLine:    v     vv    vvvvvv   vvvvv
        # LinkLine:    / \   /  \    /  \     / \
        #
        linkSpacing = min(stringValueWidth, 2 - stringValueWidth % 2)
        leftLinkBar = 1 if leftNode and _depth <= max_print_height else 0
        rightLinkBar = 1 if rightNode and _depth <= max_print_height else 0
        minLinkWidth = leftLinkBar + linkSpacing + rightLinkBar
        valueOffset = (stringValueWidth - linkSpacing) // 2

        # find optimal position for right side top node
        #   * must allow room for link bars above and between left and right top nodes
        #   * must not overlap lower level nodes on any given line (allow gap of minSpacing)
        #   * can be offset to the left if lower subNodes of right node
        #     have no overlap with subNodes of left node
        minSpacing = 4

        # Revised to improve readability; I am pretty sure this produces output identical to original code commented out below
        rightNodePosition = firstLeftWidth + minLinkWidth
        for LLW, RLI in zip(leftLineWidths, rightLineIndents[0:commonLines]):
            rightNodePosition = max(rightNodePosition, LLW + minSpacing + firstRightIndent - RLI)

        # # Original rightNodePosition calculation using fn.reduce(...) and lambda function
        # rightNodePosition = fn.reduce(lambda r, i: max(r, i[0] + minSpacing + firstRightIndent - i[1]), \
        #                               zip(leftLineWidths, rightLineIndents[0:commonLines]), \
        #                               firstLeftWidth + minLinkWidth)

        # extend basic link bars (slashes) with underlines to reach left and right
        # top nodes.
        #
        #        vvvvv
        #       __/ \__
        #      L       R
        #
        linkExtraWidth = max(0, rightNodePosition - firstLeftWidth - minLinkWidth)
        rightLinkExtra = linkExtraWidth // 2
        leftLinkExtra = linkExtraWidth - rightLinkExtra

        # build key line taking into account left indent and link bar extension (on left side)
        valueIndent = max(0, firstLeftWidth + leftLinkExtra + leftLinkBar - valueOffset)
        valueLine = " " * max(0, valueIndent) + stringValue
        slash = "\\" if inverted else "/"
        backslash = "/" if inverted else "\\"
        uLine = "¯" if inverted else "_"

        # build left side of link line
        leftLink = "" if not leftNode or _depth >= max_print_height else (" " * firstLeftWidth + uLine * leftLinkExtra + slash)

        # build right side of link line (includes blank spaces under top node key)
        rightLinkOffset = linkSpacing + valueOffset * (1 - leftLinkBar)
        rightLink = "" if not rightNode or _depth >= max_print_height else (" " * rightLinkOffset + backslash + uLine * rightLinkExtra)

        # full link line (will be empty if there are no sub nodes)
        linkLine = leftLink + rightLink

        # will need to offset left side lines if right side sub nodes extend beyond left margin
        # can happen if left subtree is shorter (in height) than right side subtree
        leftIndentWidth = max(0, firstRightIndent - rightNodePosition)
        leftIndent = " " * leftIndentWidth
        indentedLeftLines = [(leftIndent if line else "") + line for line in leftSubLines]

        # compute distance between left and right sublines based on their key position
        # can be negative if leading spaces need to be removed from right side
        mergeOffsets = [len(line) for line in indentedLeftLines]
        mergeOffsets = [leftIndentWidth + rightNodePosition - firstRightIndent - w for w in mergeOffsets]
        mergeOffsets = [p if rightSubLines[i] else 0 for i, p in enumerate(mergeOffsets)]

        # combine left and right lines using computed offsets
        #   * indented left sub lines
        #   * spaces between left and right lines
        #   * right sub line with extra leading blanks removed.
        mergedSubLines = zip(range(len(mergeOffsets)), mergeOffsets, indentedLeftLines)
        mergedSubLines = [(i, p, line + (" " * max(0, p))) for i, p, line in mergedSubLines]
        mergedSubLines = [line + rightSubLines[i][max(0, -p):] for i, p, line in mergedSubLines]

        # Assemble final result combining
        #  * node key string
        #  * link line (if any)
        #  * merged lines from left and right sub trees (if any)
        treeLines = [leftIndent + valueLine] + ([] if not linkLine else [leftIndent + linkLine]) + mergedSubLines

        # invert final result if requested
        treeLines = reversed(treeLines) if inverted and not _depth else treeLines

        # return intermediate tree lines or print final result
        if not _depth:
            print("\n".join(treeLines))
            if max_print_height > self._height:
                print(f"\n Binary tree height, {self._height}, exceeds maximum printable height, {max_print_height}. Increase max_print_height to print more of the tree.")
        else:
            return treeLines

    def print_branch(self, branch_root:BT_Node=None, print_key:bool=False, print_val:bool=True, inverted:bool=False) -> None:
        """
        Print the contents of the branch of the binary tree beginning at a specified node to console.
        :param branch_root: Node with is the root of the branch to be printed
        :param print_key: Flag, if true, node key will be included in output of tree
        :param print_val: Flag, if true, node value will be included in output of tree
        :param inverted: Flag, if true, invert display of tree, e.g. as would be appropriate for a family tree
        :return: None
        """
        # Call print method beginning at the specified node as opposed to root
        self.print(print_key=print_key, print_val=print_val, max_print_height=-1, inverted=inverted, _node=branch_root)

    # Clear Tree
    # --------------------------------
    def clear(self) -> None:
        """
        Clear all values from tree. All child nodes will be cleared automatically by Python's Garbage Collection.
        :return: None
        """
        self.__init__()
