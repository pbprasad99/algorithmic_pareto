# Properties and Terms


## Types of Nodes

The nodes in a tree can be classified into different types based on their properties :

* Root Node : Has no parent.
* Child Node : Is linked to a parent.
* Leaf node : Has No children.
* Parent Node : Has at least one child.
* Sibling Nodes : Nodes that share a parent.

## What is an edge? 

An edge represents the relationship between two nodes/vertices. It can be directed or undirected. A directed edge constrains traversal to only one direction as opposed to an undirected edge. In rooted tree an edge represents a parent child relationship between two nodes by virtue of the traversal being constrained from parent to child.


## What is a Path?

Do not confuse a path with a **SET** of nodes. There is a notion of ordering in a path. It is a sequence of nodes which are connected by edges. 


A path in a graph is a sequence of edges, where the endpoint of each edge is the starting point of the next edge.  We can have undirected paths in an undirected graph or directed paths in a directed graph. [Ref. 5]

In a rooted tree an edge is always directed from parent to child. ***(This is the subtle reason why backtracking to the root node is necessary in depth first tree traversals to visit the right subtree after having visited the left subtree)***

## Properties: 

* Depth (of a node): The number of edges between the node and the root. Root node has a depth of 0.
* Level (of a node): Same as depth, but conventionally we start counting levels from 1. Root node is at level 1. Used more in the context of level order traversals.
* Height (of a tree or subtree): The length of the path between the root node (of a tree or subtree) and the deepest descendant of the root node. Height of a node is simply the height of the subtree rooted at that node. The height of a tree is the height of the root node.
* Length (of a path) :  Number of edges in a path
* Degree (of a node) : Total number of children of a node.
