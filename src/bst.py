
"""The binary search tree data structure."""
import timeit

class Node(object):
    """I am a Node."""

    def __init__(self, value, parent=None):
        """Init for our nodes."""
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None


class Binary_Search_Tree(object):
    """I am a search tree."""

    def __init__(self, iterable=None):
        """Init for our BST."""
        if iterable:
            if type(iterable) in [list, tuple]:
                for i in iterable:
                    self.insert(i)
        self.root = None
        self.length = 0
        self.right_depth = 0
        self.left_depth = 0

    # def insert(self, val):
    #     """Insert a node for start and for right and left."""
    #     if type(val) not in [float, int]:
    #         raise TypeError('Numbers only >:(')
    #     if self.root is None:
    #         self.root = Node(val)
    #         self.length += 1
    #     else:
    #         if val > self.root.value:
    #             direction = 'right'
    #         else:
    #             direction = 'left'
    #         current = self.root
    #         depth = 0
    #         while current:
    #             depth += 1
    #             if val == current.value:
    #                 break
    #             if val > current.value:
    #                 if current.right is None:
    #                     current.right = Node(val, current)
    #                     if direction == 'right':
    #                         if depth > self.right_depth:
    #                             self.right_depth = depth
    #                     else:
    #                         if depth > self.left_depth:
    #                             self.left_depth = depth
    #                     self.length += 1
    #                     self.update_balance(current)
    #                     break
    #                 else:
    #                     current = current.right
    #             else:
    #                 if current.left is None:
    #                     current.left = Node(val, current)
    #                     if direction == 'right':
    #                         if depth > self.right_depth:
    #                             self.right_depth = depth
    #                     else:
    #                         if depth > self.left_depth:
    #                             self.left_depth = depth
    #                     self.length += 1
    #                     self.update_balance(current)
    #                     break
    #                 else:
    #                     current = current.left

    def insert(self, val):
        """Insert a node for start and for right and left."""
        if type(val) not in [float, int]:
            raise TypeError('Numbers only >:(')
        if self.root is None:
            self.root = Node(val)
        else:
            current = self.root
            while current:
                if val == current.value:
                    break
                if val > current.value:
                    if current.right is None:
                        current.right = Node(val, current)
                        self.update_balance(current)
                        break
                    else:
                        current = current.right
                else:
                    if current.left is None:
                        current.left = Node(val, current)
                        self.update_balance(current)
                        break
                    else:
                        current = current.left

    def search(self, val):
        """Search binary tree for values."""
        current = self.root
        try:
            while True:
                if val > current.value:
                    current = current.right
                elif val < current.value:
                    current = current.left
                elif val == current.value:
                    return current
        except AttributeError:
            return None

    def size(self):
        """Return length of size."""
        gen = self.breadth_first()
        array = []
        while True:
            array.append(next(gen))
            if array[-1] is None:
                break
        return len(array[:-1])

    def depth(self):
        """Return depth of left and right binary search tree."""
        return self._depth_of_branch(self.root)
        
    def contains(self, value):
        """Return True if value is there and False if not."""
        if self.search(value):
            return True
        else:
            return False

    def balance(self):
        """Return our balance for our binary search tree."""
        sides = self._check_right_left_depths(self.root)
        return sides[1] - sides[0]

    def breadth_first(self):
        current = self.root
        the_list = []
        while current:
            current.left and the_list.append(current.left)
            current.right and the_list.append(current.right)
            yield current.value
            try:
                current = the_list.pop(0)
            except IndexError:
                yield None

    def pre_order(self):
        current = self.root
        the_list = []
        while current:
            current.right and the_list.append(current.right)
            yield current.value
            if current.left:
                current = current.left
            else:
                current = the_list.pop()

    def post_order(self):
        current = self.root
        the_list = []
        seen_parents = []
        while current:
            if current.left is None and current.right is None or current in seen_parents:
                yield current.value
            else:
                the_list = [current.left, current.right, current] + the_list
                the_list[:3] = [x for x in the_list[:3] if x is not None]
                seen_parents.append(current)
            if len(the_list) > 0:
                current = the_list.pop(0)

    def in_order(self):
        """Get our bst back in order."""
        current = self.root
        the_list = []
        seen_parents = []
        while current:
            if current.left is None and current.right is None or current in seen_parents:
                yield current.value
            else:
                seen_parents.append(current)
                the_list = [current.left, current, current.right] + the_list
                the_list[:3] = [x for x in the_list[:3] if x is not None]
            if len(the_list) > 0:
                current = the_list.pop(0)

    def deletion(self, value):
        """Delete our nodes in our bst."""
        current = self.root
        if value > self.root.value:
            direction = 'right'
        else:
            direction = 'left'
        while True:
            try:
                if value > current.value:  # going down the right side of our tree
                    if value == current.right.value:  # case for just one node with no children
                        if current.right.right is None and current.right.left is None:
                            current.right = None
                            depth_node = current
                            break
                        elif current.right.left is None:  # case for just one child right not left
                            current.right = current.right.right
                            current.right.parent = current
                            depth_node = current
                            break
                        elif current.right.right is None:  # case for just one child left not right
                            current.right = current.right.left
                            current.right.parent = current
                            depth_node = current
                            break
                        else:  # case for two children left and then right most
                            parent = current
                            remove = parent.right
                            new = self._findmax(remove, remove.left)
                            if new[0] != remove:
                                new[0].right = None
                                if new[1].left:
                                    new[0].right = new[1].left
                                    new[0].right.parent = new[0]
                            parent.right = new[1]
                            new[1].parent = parent
                            new[1].right = remove.right
                            new[1].right.parent = new[1]
                            depth_node = current
                            break
                    current = current.right
                elif value < current.value:  # going down the left side of our tree
                    if value == current.left.value:
                        if current.left.left is None and current.left.right is None:
                            current.left = None
                            depth_node = current
                            break
                        elif current.left.left is None:
                            current.left = current.left.right
                            current.left.parent = current
                            depth_node = current
                            break
                        elif current.left.right is None:
                            current.left = current.left.left
                            current.left.parent = current 
                            depth_node = current
                            break
                        else:
                            parent = current
                            remove = parent.left
                            new = self._findmax(remove, remove.left)
                            if new[0] != remove:
                                new[0].right = None
                                if new[1].left:
                                    new[0].right = new[1].left
                                    new[0].right.parent = new[0]
                            parent.right = new[1]
                            parent.right = parent
                            new[1].left = remove.left
                            new[1].left.parent = new[1]
                            depth_node = current
                            break
                    current = current.left
                elif value == current.value:
                    if current.left is None and current.right is None:
                            self.root = None
                            depth_node = None
                            break
                    elif current.left is None:
                        self.root = current.right
                        self.root.parent = None 
                        depth_node = self.root
                    elif current.right is None:
                        self.root = current.left
                        self.root.parent = None
                        depth_node = self.root
                    else:
                        new = self._findmax(current, current.left)
                        if new[0] != current:
                            new[0].right = None
                            if new[1].left:
                                new[0].right = new[1].left
                        self.root = new[1]
                        self.root.left = current.left
                        self.root.left.parent = self.root
                        self.root.right = current.right
                        self.root.right.parent = self.root
                        self.root.parent = None
                        depth_node = self.root
                        break
            except AttributeError:
                break
        self.update_balance(depth_node)
        # new_depth = self._depth_of_node(depth_node) + self._depth_of_branch(depth_node)
        # if direction == 'right':
        #     self.right_depth = new_depth
        # else:
        #     self.left_depth = new_depth

    def _findmax(self, remove, child):
        """Finds the furthest right child of a node and returns it plus parent."""
        parent = remove
        current = child
        while current.right:
            parent = current
            current = current.right
        return [parent, current]

    def _depth_of_node(self, node):
        """Find the depth from top of tree to our node."""
        current = self.root
        depth = 0
        try:
            while True:
                if node.value > current.value:
                    current = current.right
                elif node.value < current.value:
                    current = current.left
                elif node.value == current.value:
                    return depth
                depth += 1
        except AttributeError:
            return None

    def _depth_of_branch(self, node):
        """Find depth of our branch from our found node."""
        current = [node, 0]
        the_list = []
        depth = 0
        while current:
            current[0].left and the_list.append([current[0].left, current[1] + 1])
            current[0].right and the_list.append([current[0].right, current[1] + 1])
            depth = current[1]
            try:
                current = the_list.pop(0)
            except IndexError:
                return depth

    def update_balance(self, node=None):
        """Updates our balance of the tree."""

        if node is None:
            node = self.root
        sides = self._check_right_left_depths(node)
        if sides[1] - sides[0] > 1:  # for right side being heavier
            child_sides = self._check_right_left_depths(node.right)
            if child_sides[1] - child_sides[0] < 0:
                node = self.double_rotate_right_left(node)

            else:
                node = self.left_rotation(node)

        elif sides[1] - sides[0] < -1:  # for the left side being heavier
            child_sides = self._check_right_left_depths(node.left)
            if child_sides[1] - child_sides[0] > 0:

                node = self.double_rotate_left_right(node)
            else:

                node = self.right_rotation(node)

        if node is not self.root:
            self.update_balance(node.parent)

    def _check_right_left_depths(self, node):
        left_side = 0
        right_side = 0
        if node.right:
            right_side = 1 + self._depth_of_branch(node.right)
        if node.left:
            left_side = 1 + self._depth_of_branch(node.left)
        return (left_side, right_side)

    def right_rotation(self, node):
        n2 = node
        k = n2.left
        n2.left = k.right
        if n2.left:
            n2.left.parent = n2
        k.parent = n2.parent
        if n2.parent is None:
            k.parent = None
            self.root = k
        elif n2.parent.left == n2:
            n2.parent.left = k
        else:
            n2.parent.right = k
        k.right = n2
        k.right.parent = k
        return k

    def left_rotation(self, node):
        n2 = node
        k = n2.right
        n2.right = k.left
        if n2.right:
            n2.right.parent = n2
        k.parent = n2.parent
        if n2.parent is None:
            k.parent = None
            self.root = k
        elif n2.parent.right == n2:
            n2.parent.right = k
        else:
            n2.parent.left = k          
        k.left = n2
        k.left.parent = k

        return k

    def double_rotate_left_right(self, node):
        node.left = self.left_rotation(node.left)
        k = self.right_rotation(node)
        return k

    def double_rotate_right_left(self, node):
        print(node.value)
        node.right = self.right_rotation(node.right)
        k = self.left_rotation(node)
        return k

    def print_tree(self):
        current = [self.root, 0]
        the_list = []
        depth = 0
        final = []
        temp = []
        lines = []
        while current:

            final.append([current[0].value, current[1]])
            current[0].left and the_list.append([current[0].left, current[1] + 1])
            current[0].right and the_list.append([current[0].right, current[1] + 1])
            depth = current[1]
            try:
                current = the_list.pop(0)
            except IndexError:
                tree = [[]]
                otherTree= []
                for i in range(depth):
                    tree.append([])
                for i in final:
                    tree[i[1]].append(i[0])
                    # print(i[1])
                longest = 0
                for i in tree:
                    print(i)
                    if len(i) > longest:
                        longest = len(i)
                string = ' ' * 2 * longest
                if longest % 2 == 0:
                    longest += 1
                midpoint = int(longest/2 + .5)
                print(midpoint)
                for i in range(longest*20):
                    otherTree.append(' ')
                curr = [self.root, 0, midpoint*8, 0]
                depth = 0
                current_level = midpoint
                the_list = []
                while curr:
                    print(curr[0].value, 'has children: ', curr[0].left and curr[0].left.value, curr[0].right and curr[0].right.value)
                    if otherTree[curr[2]].isspace():
                        curr[2] += curr[3]
                        curr[1] += 1
                    print(curr[2])
                    print('mid', midpoint)
                    if curr[2] == midpoint*8 and curr[3] < 0:
                        curr[2] += 1
                    elif curr[2] == midpoint*8 and curr[3] > 0:
                        curr[2] -= 1
                    if curr[0] == self.root:
                        otherTree[curr[2]] += '  ' * curr[1] + str(curr[0].value)
                    else:
                        otherTree[curr[2]] += '  ' * curr[1] + str(curr[0].parent.value) + '<' + str(curr[0].value)
                    if curr[0].left:
                        otherTree[curr[2] - 1] += ' ' * (len(otherTree[curr[2]]) - len(otherTree[curr[2]-1])) + '/' + (str(curr[0].left and curr[0].left.value))
                    if curr[0].right:
                        otherTree[curr[2] + 1] += ' ' * (len(otherTree[curr[2]]) - len(otherTree[curr[2]+1])) + '\\' + (str(curr[0].right and curr[0].right.value))
                    # if curr[3] == '/':
                    #     otherTree[curr[2] + 1] += ' ' * curr[1] + curr[3]
                    # else:
                    #     otherTree[curr[2] - 1] += ' ' * curr[1] + curr[3]

                    curr[0].left and the_list.append([curr[0].left, curr[1] + 1, curr[2] -2, -3])
                    curr[0].right and the_list.append([curr[0].right, curr[1] + 1, curr[2] + 2, 3])
                    try:
                        curr = the_list.pop(0)
                    except IndexError:
                        for i in otherTree:
                            print(i)
                        break
                break

def wrapper(func, *args, **kwargs):
    """Creates a value for a function with a specific arguement called to it."""
    def wrapped():
        return func(*args, **kwargs)
    return wrapped
    #code found at http://pythoncentral.io/time-a-python-function/

if __name__ == '__main__':
    Bullshit_tree = Binary_Search_Tree()
    import random
    # data = [10, 30, 20]
    # data = [75, 97, 40, 7, 48, 65, 83, 27, 38, 1, 101, 1001, 110, 111, 112, 114, 113, 16, 86, 87, 100, 47, 53, 55, 54]
    # data = [4, 2, 6, 5, 9, 1, 3, 8, 7]
    # data = [1, 2, 3, 4, 5, 6, 7]
    # print(data)
    # data = random.sample(range(1, 100), 50)
    data = [75, 97, 40, 7, 48, 65, 83, 27, 38, 1, 16, 86, 87, 100, 47, 53, 55, 54]
    # for i in range(len(data)):
    #     data.append(i)
    # print(data)
    for i in data:
        Bullshit_tree.insert(i)
    Bullshit_tree.print_tree()
    print('depth is ', Bullshit_tree.depth())
    print('balance is ', Bullshit_tree.balance())
    print('size is ', Bullshit_tree.size())
    Bullshit_tree.deletion(48)
    Bullshit_tree.print_tree()

    gen = Bullshit_tree.in_order()
    array = []
    while len(array) < len(data):
        array.append(next(gen))
    print(array)

    # wrapped1 = wrapper(Bullshit_tree.search, data[0])
    # wrapped2 = wrapper(Bullshit_tree.search, data[-1])
    # print(Bullshit_tree.size())
    # print(Bullshit_tree.depth())
    # print(Bullshit_tree.balance())
    # print(Bullshit_tree.right_depth)
    # print(Bullshit_tree.left_depth)
    # print(Bullshit_tree.root.value)
    # print(Bullshit_tree.root.right.value)
    # print(Bullshit_tree.root.right.left.value)
    # print(timeit.timeit(wrapped1))
    # print(timeit.timeit(wrapped2))
    # Bullshit_tree.deletion(65)
    # gen = Bullshit_tree.breadth_first()
    # array = []
    # while len(array) < len(data):
    #     array.append(next(gen))
    # print(array)
    # print(Bullshit_tree._check_right_left_depths(Bullshit_tree.root))
    # print(array)
    # print('update', Bullshit_tree.update_balance())
    # print(Bullshit_tree._check_right_left_depths(Bullshit_tree.root))
    # Bullshit_tree.update_balance()
    # print(Bullshit_tree.print_tree())
    # Bullshit_tree.update_balance()
    # Bullshit_tree.left_rotation(Bullshit_tree.root.right)
    # print(Bullshit_tree.print_tree())
    # print(Bullshit_tree.depth())
    # print(Bullshit_tree.size())

    # print(Bullshit_tree.search(data[-1]))

