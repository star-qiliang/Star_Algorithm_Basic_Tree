import random
# random.seed(42)

class Node:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

    def pop_left(self):
        node = self.left
        self.left = None
        return node

    def pop_right(self):
        node = self.right
        self.right = None
        return node

    def random_add_node(self, node):
        if type(node)!= Node:
            node = Node(node)

        if (not self.left) and (not self.right):
            if random.randint(0,1):
                self.left = node
            else:
                self.right = node

        elif not self.left:
            self.left = node

        elif not self.right:
            self.right = node

        else:
            if random.randint(0,1):
                self.left.random_add_node(node)
            else:
                self.right.random_add_node(node)

    def binrach_search_add_node(self, node):
        if type(node)!= Node:
            node = Node(node)

        if node.val > self.val:
            if not self.right:
                self.right = node
            else:
                self.right.binrach_search_add_node(node)
        else:
            if not self.left:
                self.left = node
            else:
                self.left.binrach_search_add_node(node)

    def search(self, val):
        node = self
        if node.val==val:
            return node
        elif val < node.val:
            if not node.left:
                return None
            else:
                res = node.left.search(val)
                return res
        else:
            if not node.right:
                return None
            else:
                res = node.right.search(val)
                return res
            
    def pop_left_most(self, node):
        if not node:
            return None

        parent = node
        cur = node.left
        if not cur:
            return cur

        while cur.left:
            parent = cur
            cur = cur.left

        parent.pop_left()

        if cur.right:
            parent.left = cur.right

        return cur


    def pop_right_most(self, node):
        if not node:
            return None

        parent = node
        cur = node.right
        if not cur:
            return cur

        while cur.right:
            parent = cur
            cur = cur.right

        parent.pop_right()

        if cur.left:
            parent.right = cur.left

        return cur
                        
    def search_and_pop(self, val):
        node = self
        if val == node.val:
            target_node = node
            sub_left = target_node.pop_left()
            sub_right = target_node.pop_right()

            if (not sub_left) and (not sub_right):
                return target_node, None
            

            elif sub_left and sub_right:
                if random.randint(0,1):
                    new_root = self.pop_left_most(sub_right)
                    if new_root:
                        new_root.left = sub_left
                        new_root.right = sub_right
                    else:
                        new_root = sub_right 
                        new_root.left = sub_left

                else:
                    new_root = self.pop_right_most(sub_left)
                    if new_root:
                        new_root.left = sub_left
                        new_root.right = sub_right
                    else:
                        new_root = sub_left
                        new_root.right = sub_right

            elif sub_left:
                new_root = self.pop_right_most(sub_left)
                if new_root:
                    new_root.left = sub_left
                else:
                    new_root = sub_left # ???

            else:
                new_root = self.pop_left_most(sub_right)
                if new_root:
                    new_root.right = sub_right
                else:
                    new_root = sub_right # ???

            return target_node, new_root # new root

        elif val < node.val:
            if not node.left:
                return None, node
            else:
                target_node, new_root = node.left.search_and_pop(val)

                if not target_node:
                    return None, node
                else:
                    if target_node is node.left:
                        node.pop_left()

                    node.left = new_root

                    return target_node, new_root
            
        else:
            if not node.right:
                return None, node
            else:
                target_node, new_root = node.right.search_and_pop(val)

                if not target_node:
                    return None, node
                else:
                    if target_node is node.right:
                        node.pop_right()

                    node.right = new_root

                    return target_node, new_root



class BinarySearchTree:
    def __init__(self):
        self.head = None

    def add_value(self, node):
        if type(node)!= Node:
            node = Node(node)

        if not self.head:
            self.head = node
        else:
            self.head.binrach_search_add_node(node)


    def search(self, val):
        res = self.head.search(val)
        return res
    

    def search_and_pop(self, val):
        target_node, new_root = self.head.search_and_pop(val)
        self.head = new_root
        return target_node



    def pop_bottom(self): # for pop_head()
        cur = self.head

        if not cur:
            return None
                
        if (not cur.left) and (not cur.right):
            self.head = None
            return cur

        parent = None
        left_or_right = ''
        while cur:
            if cur.left and cur.right:
                if random.randint(0,1):
                    left_or_right = 'left'
                    parent = cur
                    cur = cur.left
                else:
                    left_or_right = 'right'
                    parent = cur
                    cur = cur.right
            elif cur.left:
                left_or_right = 'left'
                parent = cur
                cur = cur.left
            
            elif cur.right:
                left_or_right = 'right'
                parent = cur
                cur = cur.right
            else:
                if left_or_right=='left':
                    res = parent.pop_left()
                else:
                    res = parent.pop_right()

                return res


    def pop_head(self):
        cur = self.head

        if not cur:
            return None
        
        if (not cur.left) and (not cur.right):
            self.head = None
            return cur
        
        bottom = self.pop_bottom()
        bottom.left = cur.pop_left()
        bottom.right = cur.pop_right()

        return bottom

    def parse_by_layer(self):

        if not self.head:
            return

        max_layer = 1
        current_layer_index = 0
        layer_dict = {}

        layer_dict[current_layer_index] = [self.head]

        while current_layer_index in layer_dict:
            cur_layer_list = layer_dict[current_layer_index]
            next_layer_index = current_layer_index + 1
            next_layer_list = []
            for node in cur_layer_list:
                if node.left:
                    next_layer_list.append(node.left)
                if node.right:
                    next_layer_list.append(node.right)
            
            if next_layer_list:
                layer_dict[next_layer_index] = next_layer_list
                current_layer_index = next_layer_index
                max_layer +=1
            else:
                break
        
        total_num = 0
        for i in range(max_layer):
            cur_layer_list = layer_dict[i]
            print(i, [node.val for node in cur_layer_list])
            total_num += len(cur_layer_list)
            # print(i, len([node.val for node in cur_layer_list]))
        print("#:", total_num)

        return layer_dict
    


def main():
    node_list = [1, 2, 86, 18, 5, 9, 20, 10, 21, 236, 0, 7, 904, 1006, 709, 57, 357, 48, 100, 478, 2093, 1238]
    # N = 100000
    # node_list = [float(round(random.randint(0, 10*N)/N, 3)) for _ in range(N)]

    print("\n#:",len(node_list))
    # print(node_list)

    tree = BinarySearchTree()
    for node in node_list:
        tree.add_value(node)

    tree.parse_by_layer()

    target_val = 2093
    target_node = tree.search(target_val)
    print("\ntarget_val:", target_val)
    res = target_node.val if target_node else None
    print("target_node:", res)


    target_val = 2093
    # target_val = 2
    target_node = tree.search_and_pop(target_val)
    print("\ntarget_val:", target_val)
    res = target_node.val if target_node else None
    print("target_node:", res)
    tree.parse_by_layer()


    # head = tree.pop_head()
    # print("\nhead:", head.val)
    # tree.parse_by_layer()


    return


if __name__=="__main__":
    main()
    print("\nDone!\n")

