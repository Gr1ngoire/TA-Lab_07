import math

from utils import Utils


class MyUnitNode:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.data)


class MyBtreeNode:

    def __init__(self, parent):
        self.unit_nodes = []
        self.parent = parent
        self.isRoot = False
        self.ORDER = 5

    def is_overfilled(self):
        return len(self.unit_nodes) > self.ORDER - 1

    def children(self):
        counter = 0
        for i in range(len(self.unit_nodes)):
            if not (self.unit_nodes[i].left is None):
                counter += 1
            if i == len(self.unit_nodes) - 1 and not (self.unit_nodes[i].right is None):
                counter += 1
        return counter

    def print_tree_node(self):
        res = ""
        for i in range(len(self.unit_nodes)):
            res += f"{self.unit_nodes[i].__str__()}; "

        return res


class MyBtree:

    def __init__(self):
        self.util = Utils()
        self.root = None

    def __atomic_insertion(self, node, new_unit_node):
        node.unit_nodes.append(new_unit_node)
        self.util.insertion_sort(node.unit_nodes)

    def __atomic_split(self, tree_node):
        mid_index = math.ceil(len(tree_node.unit_nodes) / 2) - 1
        new_unit_node = MyUnitNode(tree_node.unit_nodes[mid_index].data)

        nodes_list_left = tree_node.unit_nodes.copy()
        nodes_list_right = tree_node.unit_nodes.copy()
        new_unit_node.left = MyBtreeNode(tree_node.parent)
        new_unit_node.left.unit_nodes = nodes_list_left[:mid_index]
        new_unit_node.right = MyBtreeNode(tree_node.parent)
        new_unit_node.right.unit_nodes = nodes_list_right[mid_index + 1:]

        return new_unit_node

    def __split_insert(self, tree_node):

        if tree_node.isRoot:
            mid_index = math.ceil(len(tree_node.unit_nodes) / 2) - 1
            new_root = MyBtreeNode(None)
            new_root.isRoot = True
            self.root = new_root
            new_single_node = MyUnitNode(tree_node.unit_nodes[mid_index].data)


            nodes_list_left = tree_node.unit_nodes.copy()
            nodes_list_right = tree_node.unit_nodes.copy()
            new_single_node.left = MyBtreeNode(new_root)
            new_single_node.left.unit_nodes = nodes_list_left[:mid_index]
            new_single_node.right = MyBtreeNode(new_root)
            new_single_node.right.unit_nodes = nodes_list_right[mid_index + 1:]
            new_root.unit_nodes.append(new_single_node)


        else:
            new_unit_node = self.__atomic_split(tree_node)
            self.__atomic_insertion(tree_node.parent, new_unit_node)
            if tree_node.parent.unit_nodes.index(new_unit_node) == 0:
                tree_node.parent.unit_nodes[1].left = new_unit_node.right
            elif 0 < tree_node.parent.unit_nodes.index(new_unit_node) < len(tree_node.parent.unit_nodes) - 1:
                tree_node.parent.unit_nodes[tree_node.parent.unit_nodes.index(new_unit_node) - 1].right = new_unit_node.left
                tree_node.parent.unit_nodes[tree_node.parent.unit_nodes.index(new_unit_node) + 1].left = new_unit_node.right
            elif tree_node.parent.unit_nodes.index(new_unit_node) == len(tree_node.parent.unit_nodes) - 1:
                tree_node.parent.unit_nodes[len(tree_node.parent.unit_nodes) - 2].right = new_unit_node.left

            if tree_node.parent.is_overfilled():
                print(tree_node.print_tree_node())
                print(tree_node.parent.print_tree_node())
                self.__split_insert(tree_node.parent)

    def __insertion(self, data, node):

        if node.children() != 0:
            for i in range(len(node.unit_nodes)):
                if data < node.unit_nodes[i].data:
                    if i != 0 and data < node.unit_nodes[i - 1].data:
                        continue
                    elif (i != 0 and data > node.unit_nodes[i - 1].data) or i == 0:
                        self.__insertion(data, node.unit_nodes[i].left)
                elif data == node.unit_nodes[i].data:
                    raise Exception("Already exists, can not insert")
                elif data > node.unit_nodes[i].data:
                    if i + 1 < len(node.unit_nodes) and data > node.unit_nodes[i + 1].data:
                        continue
                    elif (i + 1 < len(node.unit_nodes) and data < node.unit_nodes[i - 1].data) or i + 1 == len(node.unit_nodes):
                        self.__insertion(data, node.unit_nodes[i].right)

        else:
            new_data = MyUnitNode(data)
            self.__atomic_insertion(node, new_data)
            if node.unit_nodes.index(new_data) == 0:
                new_data.right = node.unit_nodes[1].left
            elif 0 < node.unit_nodes.index(new_data) < len(node.unit_nodes) - 1:
                new_data.left = node.unit_nodes[node.unit_nodes.index(new_data) - 1].right
                new_data.right = node.unit_nodes[node.unit_nodes.index(new_data) + 1].left
            elif node.unit_nodes.index(new_data) == len(node.unit_nodes) - 1:
                new_data.left = node.unit_nodes[len(node.unit_nodes) - 2].right

            if node.is_overfilled():
                self.__split_insert(node)

    def __recursive_tree_print(self, start, user_data):

        user_data.result += f" |{start.print_tree_node()}| "
        if start.children() != 0:
            for i in range(len(start.unit_nodes)):
                if not (start.unit_nodes[i].left is None):
                    self.__recursive_tree_print(start.unit_nodes[i].left, user_data)
                if i == len(start.unit_nodes) - 1 and not (start.unit_nodes[i].right is None):
                    self.__recursive_tree_print(start.unit_nodes[i].right, user_data)

        return user_data.result

    def __recursive_search(self, start, data):

        if start.children() != 0:
            for i in range(len(start.unit_nodes)):
                if data < start.unit_nodes[i].data:
                    if i != 0 and data < start.unit_nodes[i - 1].data:
                        continue
                    elif (i != 0 and data > start.unit_nodes[i - 1].data) or i == 0:
                        return self.__recursive_search(start.unit_nodes[i].left, data)
                elif data == start.unit_nodes[i].data:
                    return True
                elif data > start.unit_nodes[i].data:
                    if i + 1 < len(start.unit_nodes) and data > start.unit_nodes[i + 1].data:
                        continue
                    elif (i + 1 < len(start.unit_nodes) and data < start.unit_nodes[i - 1].data) or i + 1 == len(start.unit_nodes):
                        return self.__recursive_search(start.unit_nodes[i].right, data)

        else:
            for i in range(len(start.unit_nodes)):
                if start.unit_nodes[i].data == data:
                    return True

        return False

    def print_tree(self, user_data):
        if self.root is None:
            return

        return self.__recursive_tree_print(self.root, user_data)

    def contains(self, data):
        if self.root is None:
            return False

        return self.__recursive_search(self.root, data)

    def insert(self, data):
        if self.root is None:
            new_root = MyBtreeNode(None)
            new_root.isRoot = True
            new_root.unit_nodes = [MyUnitNode(data)]
            self.root = new_root
            return

        self.__insertion(data, self.root)

