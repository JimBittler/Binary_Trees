from __future__ import annotations
import functools as fn
import time
import numpy as np

class BT_Node():
    def __init__(self, val:float=None, parent:BT_Node=None):
        self.value = val
        self.parent = None
        self.left_child = None
        self.right_child = None

    def clear(self):
        self.__init__()

class BT_Tree():
    # Reference: https://stackoverflow.com/a/28864021
    # StackOverflow.com user djra, accessed May 01, 2025
    def __init__(self):
        self._root = None
        self._depth = 0
        self._node_count = 0
        self._search_depth = 0

    # Properties
    # --------------------------------
    @property
    def root(self):
        return self._root

    @property
    def depth(self):
        return self._depth

    @property
    def node_count(self):
        return self._node_count

    # Add node
    # --------------------------------
    # Public add method: begins at root of the tree
    def add(self, val:float=None):
        # If the tree has no root, assign input value
        if self._root is None:
            self._root = BT_Node(val)
            self._node_count += 1
            self._search_depth = 0
        # Else call private recursive add method
        else:
            self._add_recursive(val, self._root)

        # Update tree depth
        if self._search_depth > self._depth:
            self._depth = self._search_depth

        # Clear search depth
        self._search_depth = 0

    # Private add method: recursely search tree for parent node under which current value should be added as child
    def _add_recursive(self, val:float, parent_node:BT_Node):
        # Increment search depth
        self._search_depth += 1

        # Inspect left child
        if val < parent_node.value:
            # If there is no left child, add a node with input value
            if parent_node.left_child is None:
                parent_node.left_child = BT_Node(val=val, parent=parent_node)
                self._node_count += 1
            # Else continue recursive search
            else:
                self._add_recursive(val, parent_node.left_child)

        # Inspect right child
        else:
            # If there is no right child, add a node with input value
            if parent_node.right_child is None:
                parent_node.right_child = BT_Node(val=val, parent=parent_node)
                self._node_count += 1
            # Else continue recursive search
            else:
                self._add_recursive(val, parent_node.right_child)

    # Find Node
    # --------------------------------
    # Public search method, begins at the root of the tree
    def find(self, val:float=None):
        # If no value is passed, or tree has no root, return none
        if val is None or self.root is None:
            nearest_value = None
        # Else search the tree beginning at the root node
        else:
            nearest_value = self._find(val, self._root)

        # return solution
        return nearest_value

    # Private search method: recursely search tree for node with value val
    def _find(self, val:float, parent_node:BT_Node):
        # Check parent node value
        if val == parent_node.value:
            nearest_value = parent_node.value
        # Check left child value
        elif val < parent_node.value:
            # If no left child, return parent
            if parent_node.left_child is None:
                nearest_value = parent_node.value
            # Else, search left child
            else:
                nearest_value = self._find(val, parent_node.left_child)
        # Check right child value
        else:
            # If no right child, return parent
            if parent_node.right_child is None:
                nearest_value = parent_node.value
            # Else, search right child
            else:
                nearest_value = self._find(val, parent_node.right_child)

        # Check if parent node value is closer than child node
        if abs(parent_node.value - val) < abs(nearest_value - val):
            nearest_value = parent_node.value

        # Return nearest value
        return nearest_value

    # Print Tree
    # --------------------------------
    def print(self):
        printBTree(self.root, inverted=False)

    # Clear Tree
    # --------------------------------
    def clear(self):
        self.__init__()

# Print Binary Tree
def printBTree(node:BT_Node, inverted=False, _isTop=True):
    # Reference: https://stackoverflow.com/a/49844237
    # StackOverflow.com user Alan T., accessed May 04, 2025

    # node value string and sub nodes
    stringValue = str(node.value)
    leftNode = node.left_child
    rightNode = node.right_child
    # stringValue, leftNode, rightNode = nodeInfo(node)

    stringValueWidth  = len(stringValue)

    # recurse to sub nodes to obtain line blocks on left and right
    leftTextBlock     = [] if not leftNode else printBTree(node=leftNode, inverted=inverted, _isTop=False)

    rightTextBlock    = [] if not rightNode else printBTree(node=rightNode, inverted=inverted, _isTop=False)

    # count common and maximum number of sub node lines
    commonLines       = min(len(leftTextBlock),len(rightTextBlock))
    subLevelLines     = max(len(rightTextBlock),len(leftTextBlock))

    # extend lines on shallower side to get same number of lines on both sides
    leftSubLines      = leftTextBlock  + [""] *  (subLevelLines - len(leftTextBlock))
    rightSubLines     = rightTextBlock + [""] *  (subLevelLines - len(rightTextBlock))

    # compute location of value or link bar for all left and right sub nodes
    #   * left node's value ends at line's width
    #   * right node's value starts after initial spaces
    leftLineWidths    = [ len(line) for line in leftSubLines  ]
    rightLineIndents  = [ len(line)-len(line.lstrip(" ")) for line in rightSubLines ]

    # top line value locations, will be used to determine position of current node & link bars
    firstLeftWidth    = (leftLineWidths   + [0])[0]
    firstRightIndent  = (rightLineIndents + [0])[0]

    # width of sub node link under node value (i.e. with slashes if any)
    # aims to center link bars under the value if value is wide enough
    #
    # ValueLine:    v     vv    vvvvvv   vvvvv
    # LinkLine:    / \   /  \    /  \     / \
    #
    linkSpacing       = min(stringValueWidth, 2 - stringValueWidth % 2)
    leftLinkBar       = 1 if leftNode  else 0
    rightLinkBar      = 1 if rightNode else 0
    minLinkWidth      = leftLinkBar + linkSpacing + rightLinkBar
    valueOffset       = (stringValueWidth - linkSpacing) // 2

    # find optimal position for right side top node
    #   * must allow room for link bars above and between left and right top nodes
    #   * must not overlap lower level nodes on any given line (allow gap of minSpacing)
    #   * can be offset to the left if lower subNodes of right node
    #     have no overlap with subNodes of left node
    minSpacing        = 2
    rightNodePosition = fn.reduce(lambda r,i: max(r,i[0] + minSpacing + firstRightIndent - i[1]), \
                                 zip(leftLineWidths,rightLineIndents[0:commonLines]), \
                                 firstLeftWidth + minLinkWidth)

    # extend basic link bars (slashes) with underlines to reach left and right
    # top nodes.
    #
    #        vvvvv
    #       __/ \__
    #      L       R
    #
    linkExtraWidth    = max(0, rightNodePosition - firstLeftWidth - minLinkWidth )
    rightLinkExtra    = linkExtraWidth // 2
    leftLinkExtra     = linkExtraWidth - rightLinkExtra

    # build value line taking into account left indent and link bar extension (on left side)
    valueIndent       = max(0, firstLeftWidth + leftLinkExtra + leftLinkBar - valueOffset)
    valueLine         = " " * max(0,valueIndent) + stringValue
    slash             = "\\" if inverted else  "/"
    backslash         = "/" if inverted else  "\\"
    uLine             = "¯" if inverted else  "_"

    # build left side of link line
    leftLink          = "" if not leftNode else ( " " * firstLeftWidth + uLine * leftLinkExtra + slash)

    # build right side of link line (includes blank spaces under top node value)
    rightLinkOffset   = linkSpacing + valueOffset * (1 - leftLinkBar)
    rightLink         = "" if not rightNode else ( " " * rightLinkOffset + backslash + uLine * rightLinkExtra )

    # full link line (will be empty if there are no sub nodes)
    linkLine          = leftLink + rightLink

    # will need to offset left side lines if right side sub nodes extend beyond left margin
    # can happen if left subtree is shorter (in height) than right side subtree
    leftIndentWidth   = max(0,firstRightIndent - rightNodePosition)
    leftIndent        = " " * leftIndentWidth
    indentedLeftLines = [ (leftIndent if line else "") + line for line in leftSubLines ]

    # compute distance between left and right sublines based on their value position
    # can be negative if leading spaces need to be removed from right side
    mergeOffsets      = [ len(line) for line in indentedLeftLines ]
    mergeOffsets      = [ leftIndentWidth + rightNodePosition - firstRightIndent - w for w in mergeOffsets ]
    mergeOffsets      = [ p if rightSubLines[i] else 0 for i,p in enumerate(mergeOffsets) ]

    # combine left and right lines using computed offsets
    #   * indented left sub lines
    #   * spaces between left and right lines
    #   * right sub line with extra leading blanks removed.
    mergedSubLines    = zip(range(len(mergeOffsets)), mergeOffsets, indentedLeftLines)
    mergedSubLines    = [ (i,p,line + (" " * max(0,p)) )       for i,p,line in mergedSubLines ]
    mergedSubLines    = [ line + rightSubLines[i][max(0,-p):]  for i,p,line in mergedSubLines ]

    # Assemble final result combining
    #  * node value string
    #  * link line (if any)
    #  * merged lines from left and right sub trees (if any)
    treeLines = [leftIndent + valueLine] + ( [] if not linkLine else [leftIndent + linkLine] ) + mergedSubLines

    # invert final result if requested
    treeLines = reversed(treeLines) if inverted and _isTop else treeLines

    # return intermediate tree lines or print final result
    if _isTop : print("\n".join(treeLines))
    else     : return treeLines


def main():

    n = 2 ** 3
    s = 45
    seed = 0
    np.random.seed(seed)

    val = np.random.randint(low=0, high=10 * n, size=n)

    t = BT_Tree()
    for this_val in val:
        t.add(this_val)

    print(t.root.left_child.value)
    return

    nearest_s = val[np.argmin(np.abs(val - s))]

    print(f"node count: {t.node_count}")
    print(f"min depth: {int(np.ceil(np.log2(n)))}")
    print(f"actual depth: {t.depth}")
    print(f"nearest s = {s}: {nearest_s}")
    print(f"found nearest s = {s}: {t.find(s)}")

    t.print()

if __name__ == '__main__':
    main()