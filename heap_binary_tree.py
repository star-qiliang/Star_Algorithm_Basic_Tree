import random
# random.seed(42)

class Node:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

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


    def heap_add_node(self, node):
        if type(node)!= Node:
            node = Node(node)

        if node.val>=self.val:

            if self.left and self.right:
                node.left = self.pop_left()
                node.right = self.pop_right()

                if random.randint(0,1):
                    res = node.left.heap_add_node(self)
                    node.left = res
                else:
                    res = node.right.heap_add_node(self)
                    node.right = res            

            elif self.left:
                node.left = self.pop_left()
                node.right = self
            elif self.right:
                node.right = self.pop_right()
                node.left = self
            else:
                node.random_add_node(self)

            return node
        
        else:
            if self.left and self.right:
                if random.randint(0,1):
                    res = self.left.heap_add_node(node)
                    self.left = res
                else:
                    res = self.right.heap_add_node(node)
                    self.right = res      
            else:
                self.random_add_node(node)

            return self

    def pop_left(self):
        node = self.left
        self.left = None
        return node

    def pop_right(self):
        node = self.right
        self.right = None
        return node



class HeapBinaryTree:
    def __init__(self):
        self.head = None

    def add_value(self, node):
        if type(node)!= Node:
            node = Node(node)

        if not self.head:
            self.head = node
        else:
            res = self.head.heap_add_node(node)
            self.head = res


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


    def get_balance(self, node):
        if node.left and node.right:
            if (node.val >= node.left.val) and (node.val >= node.right.val):
                return node
            
            elif (node.val >= node.left.val) and (node.val < node.right.val):
                cur = node.pop_right()
                
                tmp_left = cur.pop_left()
                tmp_right = cur.pop_right()

                cur.left = node.pop_left()

                node.left = tmp_left
                node.right = tmp_right

                res = self.get_balance(node)
                cur.right = res
                return cur
            
            elif (node.val < node.left.val) and (node.val >= node.right.val):
                cur = node.pop_left()

                tmp_left = cur.pop_left()
                tmp_right = cur.pop_right()

                cur.right = node.pop_right()

                node.left = tmp_left
                node.right = tmp_right

                res = self.get_balance(node)
                cur.left = res
                return cur
            

            else:
                if node.left.val >= node.right.val:
                    cur = node.pop_left()

                    tmp_left = cur.pop_left()
                    tmp_right = cur.pop_right()

                    cur.right = node.pop_right()

                    node.left = tmp_left
                    node.right = tmp_right

                    res = self.get_balance(node)
                    cur.left = res
                    return cur
                
                else:

                    cur = node.pop_right()
                    
                    tmp_left = cur.pop_left()
                    tmp_right = cur.pop_right()

                    cur.left = node.pop_left()

                    node.left = tmp_left
                    node.right = tmp_right

                    res = self.get_balance(node)
                    cur.right = res
                    return cur


        elif node.left:
            if  node.val >= node.left.val:
                return node
            else:
                cur = node.pop_left()
                res = cur.heap_add_node(node)
                return res

        elif node.right:
            if node.val >= node.right.val:
                return node
            else:
                cur = node.pop_right()
                res = cur.heap_add_node(node)
                return res
        else:
            return node




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

        res = self.get_balance(bottom)
        self.head = res

        return cur


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
    # N = 100
    # node_list = [int(round(random.randint(0, 10*N)/N, 0)) for _ in range(N)]

    print("\n#:",len(node_list))
    # print(node_list)

    tree = HeapBinaryTree()
    for node in node_list:
        tree.add_value(node)

    tree.parse_by_layer()



    head = tree.pop_head()
    print("\nhead:", head.val)
    tree.parse_by_layer()

    head = tree.pop_head()
    print("\nhead:", head.val)
    tree.parse_by_layer()

    head = tree.pop_head()
    print("\nhead:", head.val)
    tree.parse_by_layer()

    head = tree.pop_head()
    print("\nhead:", head.val)
    tree.parse_by_layer()

    head = tree.pop_head()
    print("\nhead:", head.val)
    tree.parse_by_layer()

    head = tree.pop_head()
    print("\nhead:", head.val)
    tree.parse_by_layer()


    return


if __name__=="__main__":
    main()
    print("\nDone!\n")

