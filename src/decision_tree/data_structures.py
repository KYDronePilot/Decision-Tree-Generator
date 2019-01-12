class Stack:
    """
    Simple stack ADT.

    Attributes:
        _data (list): Container for stack elements.
        _n (int): Size of the stack.

    """
    def __init__(self):
        self._data = list()
        self._n = 0

    def __len__(self):
        """
        Get size of stack.

        Returns: Size of stack.

        """
        return self._n

    def is_empty(self):
        """
        Check if stack is empty.

        Returns: True if empty, False if not.

        """
        return self._n == 0

    def push(self, elem):
        """
        Push element to the stack.

        Args:
            elem: Element to be pushed.

        """
        self._data.append(elem)
        self._n += 1

    def top(self):
        """
        Get element on top.

        Returns: Top element.

        """
        return self._data[-1]

    def pop(self):
        """
        Pop an element from the stack (Assuming stack not empty when called).

        Returns: Popped element.

        """
        self._n -= 1
        return self._data.pop()

    def __getitem__(self, item):
        """
        Slicer for the main data object.

        Args:
            item (slice): The slice.

        Returns: Sliced data list.

        """
        return self._data[item]


class Queue:
    """
    Lightweight queue ADT.
    
    Attributes:
        _head (Queue._Node): Head node.
        _tail (Queue._Node): Tail node.
        _size (int): The size of the queue.
    
    """
    class _Node:
        """
        Node for linked queue implementation.
        
        Attributes:
            elem: Then element being stored.
            next_node: The next node in the linked queue.
        
        """
        def __init__(self, elem, next_node):
            self.elem = elem
            self.next_node = next_node

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """
        Get size of queue.

        Returns: size of queue.

        """
        return self._size

    def is_empty(self):
        """
        Is queue empty.

        Returns: True if empty, False if not.

        """
        return self._size == 0

    def first(self):
        """
        Get first element of queue without removing, assuming queue not empty.

        Returns: Element at head node of queue.

        """
        return self._head.elem

    def dequeue(self):
        """
        Dequeue an element, assuming queue is not empty.

        Returns: Dequeued element.

        """
        res = self._head.elem
        self._head = self._head.next_node
        self._size -= 1
        # Make tail None if queue is empty.
        if self.is_empty():
            self._tail = None
        return res

    def enqueue(self, e):
        """
        Enqueue an element.

        Args:
            e: Element to enqueue.

        """
        new = self._Node(e, None)
        if self.is_empty():
            self._head = new
        else:
            self._tail.next_node = new
        self._tail = new
        self._size += 1
