# Tree nodes that will print out the LaTeX code.
class LatexNode:
    # Template for node text.
    NODE_TEMPLATE = '{node}, edge label={{node[midway,fill=white,font=\\tiny] {{{edge}}}}}'

    def __init__(self, val='', right=None, left=None, is_leaf=False, edge_label='', left_side=True):
        """

        :type right: LatexNode
        :type left: LatexNode

        """
        self.val = val
        self.right = right
        self.left = left
        self.is_leaf = is_leaf
        self.edge_label = edge_label
        self.left_side = left_side

    # def render(self):
    #     # If node is leaf, prepare leaf text accordingly.
    #     if self.is_leaf:
    #         leaf = '[leaf] '
    #     else:
    #         leaf = ''
    #     print('child { ', end='')
    #     print('node {leaf}{{{val}}}'.format(leaf=leaf, val=self.val), end='')
    #     # Recursively render children if they exist.
    #     if self.left is not None:
    #         self.left.render()
    #     if self.right is not None:
    #         self.right.render()
    #     # Add closing bracket.
    #     print(' }', end='')
    #     pass

    def render_forest(self):
        #print('[ ', end='')
        global text
        text += '[ '
        # If this is a pruned node, do not put in any contents.
        if not 'null' == self.val:
            #print(LatexNode.NODE_TEMPLATE.format(node=self.val, edge=self.edge_label), end=' ')
            text += LatexNode.NODE_TEMPLATE.format(node=self.val, edge=self.edge_label)
        else:
            #print(', phantom', end=' ')
            text += ', phantom'
        # Recursively render children if they exist.
        if self.left is not None:
            self.left.render_forest()
        if self.right is not None:
            self.right.render_forest()
        # Add closing bracket.
        #print(' ]', end='')
        text += ' ]'
        pass


# Simple stack ADT.
class Stack:
    def __init__(self):
        # Use list as data container.
        self._data = list()
        # Number of elements.
        self._n = 0

    def __len__(self):
        return self._n

    # Push element to the stack.
    def push(self, elem):
        self._data.append(elem)
        self._n += 1

    # Pop an element from the stack (Assuming stack filled when called).
    def pop(self):
        self._n -= 1
        return self._data.pop()

    # Get element on top.
    def top(self):
        return self._data[-1]


# Lightweight queue ADT.
class Queue:
    # Node for linked queue implementation.
    class _Node:
        def __init__(self, elem, next_elem):
            self.elem = elem
            self.next_elem = next_elem

    def __init__(self):
        # Head, tail and size.
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    # Get first element of queue without removing, assuming queue not empty.
    def first(self):
        return self._head.elem

    # Dequeue an element, assuming queue is not empty.
    def dequeue(self):
        res = self._head.elem
        self._head = self._head.next_elem
        self._size -= 1
        # Make tail None if queue is empty.
        if self.is_empty():
            self._tail = None
        return res

    # Enqueue an element.
    def enqueue(self, e):
        new = self._Node(e, None)
        if self.is_empty():
            self._head = new
        else:
            self._tail._next = new
        self._tail = new
        self._size += 1


# For maintaining information regarding comparisons.
# TODO: possibly handle non-unique lists.
class Comparison:
    # Operator negations.
    NEGATIONS = {
        '>': '<',
        '<': '>',
        '==': '!='
    }

    def __init__(self, e1, op, e2):
        """

        :param e1: The first element
        :param op: The operator
        :param e2: The second element
        """
        self.e1 = e1
        self.op = op
        self.e2 = e2

    def __eq__(self, other):
        """
        Check if two comparisons are equivalent.

        Args:
            other (Comparison): The other comparison.

        Returns:
            True if equivalent, False if not.

        """
        # Other operator.
        other_op = other.op
        # If operators not equal, get the negation of one and check again.
        if self.op != other_op:
            other_op = Comparison.NEGATIONS[other_op]
            # If still not equal, comparisons cannot be equivalent.
            if self.op != other_op:
                return False
        # TODO: finish here.


    def negate(self):
        """
        Get and return the negation of this comparison.

        Returns:
            Negation of comparison.

        """
        opposite = Comparison.NEGATIONS[self.op]
        return Comparison(self.e1, opposite, self.e2)


# Information about the state of execution at a branch.
class State:
    def __init__(self, previous, decision, list_state, node):
        # The previous state.
        self.previous = previous
        # Decision made to get here from last state.
        self.decision = decision
        # State of list before making decision at this branch.
        self.list_state = list_state
        # LatexNode at this branch.
        self.node = node


# Main tree generation.
class TreeGenerator:
    def __init__(self):
        # The last state of this program.
        self.last_state = None
        # Whether the algorithm is in the process of restoring a state or not.
        self.restoring = False

    # Get a stack of decisions to get to a state.
    def get_decisions(self, state, decisions):
        """

        :type state: State
        :type decisions: Stack
        """
        # Stop when root state is reached.
        if state.decision is None:
            return decisions
        # Add state's decision to the stack and recur.
        decisions.push(state.decision)
        return self.get_decisions(state.previous, decisions)

    # Algorithm execution manager.
    def execution_manager(self):
        # Run the algorithm till it ends its execution.
        self.algorithm()
        # Get the last pushed state and get back to that branch point.
        last_state = self.decisions.pop()

    # Handle a comparison (branch).
    def comp(self, e1, op, e2):
        # State at
        pass

    # Algorithm method, overridden in inheritor.
    def algorithm(self):
        raise NotImplementedError('This method should be overridden with an algorithm implementation.')



















