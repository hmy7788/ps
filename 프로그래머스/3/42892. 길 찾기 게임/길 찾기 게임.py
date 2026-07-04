import sys

sys.setrecursionlimit(10**6)

class Node:
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx
        self.left = None
        self.right = None
        
def insert(root, node):
    cur = root
    while True:
        if node.x < cur.x:
            if cur.left is None:
                cur.left = node
                return
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = node
                return
            cur = cur.right
            
def preorder(root, out):
    if root is None: return
    out.append(root.idx)
    preorder(root.left, out)
    preorder(root.right, out)

def postorder(root, out):
    if root is None: return
    postorder(root.left, out)
    postorder(root.right, out)
    out.append(root.idx)

def solution(nodeinfo):
    nodes = [Node(x, y, i+1) for i, (x, y) in enumerate(nodeinfo)]
    nodes.sort(key = lambda n : (-n.y, n.x))
    root = nodes[0]
    
    for node in nodes[1:]:
        insert(root, node)
    
    pre, post = [], []
    preorder(root, pre)
    postorder(root, post)
    return [pre, post]