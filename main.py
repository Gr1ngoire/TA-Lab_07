# BTREE OF ORDER 5
from UserData import UserData
from MyBTree import MyBtree

btree = MyBtree()

for i in range(1, 24):
    if i == 17:
        printing = UserData()
        btree.print_tree(printing)
        print(printing.result)
    if i == 20:
        printing = UserData()
        btree.print_tree(printing)
        print(printing.result)
    if i == 23:
        printing = UserData()
        btree.print_tree(printing)
        print(printing.result)
    btree.insert(i)

# print(btree.contains(49))

printing = UserData()
btree.print_tree(printing)
print(printing.result)
# print(btree.root.unit_nodes[0].left.print_tree_node())
# print(btree.root.unit_nodes[0].right.print_tree_node())




