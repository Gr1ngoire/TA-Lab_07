class Utils:

    def __init__(self):
        pass

    def insertion_sort(self, btree_array):

        for i in range(len(btree_array)):
            index_to_insert = i
            element = btree_array[i]

            while index_to_insert > 0 and element.data < btree_array[index_to_insert - 1].data:
                btree_array[index_to_insert] = btree_array[index_to_insert - 1]
                index_to_insert -= 1

            if index_to_insert != i:
                btree_array[index_to_insert] = element
