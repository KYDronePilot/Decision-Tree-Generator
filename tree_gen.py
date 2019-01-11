from src.data_structures import Stack, Queue
from src.latex import LatexTree, LatexNode


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

        Args:
            e1: The first element.
            op: The operator.
            e2: The second element.
        """
        self.e1 = e1
        self.op = op
        self.e2 = e2

    def __str__(self):
        return '{0} {1} {2}'.format(
            self.e1,
            self.op,
            self.e2
        )

    def __eq__(self, other):
        """
        Check if two comparisons are equivalent.

        Args:
            other (Comparison): The other comparison.

        Returns:
            True if equivalent, False if not.

        """
        # If operators not equal, get the negation of one and check again.
        if self.op != other.op:
            other_op = Comparison.NEGATIONS[other.op]
            # If still not equal, comparisons cannot be equivalent.
            if self.op != other_op:
                return False
            # If comparison equal to negation, check cross elements.
            return self.e1 == other.e2 and self.e2 == other.e1
        # If operators are equal, then equivalence is based on elements.
        return self.e1 == other.e1 and self.e2 == other.e2

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
    def __init__(self, node, comp):
        # The previous state.
        #self.previous = previous
        # Last decision made at this state.
        self.last_decision = True
        # LatexNode at this branch.
        self.node = node
        # Comparison made at this node.
        self.comp = comp


# Main tree generation.
class TreeGenerator:
    def __init__(self, base_data):
        # The last state of this program.
        self.last_state = None
        # Whether the algorithm is in the process of restoring a state or not.
        self.restoring = False
        # Whether the algorithm is in the process of running out its course.
        self.lame_duck = False
        # Decisions to get back to a state.
        self.restoring_decisions = Queue()
        # First decision to make after a restoration.
        self.first_decision = True
        # States to get to the current execution point.
        self.states = Stack()
        # The list being manipulated.
        self.data = []
        # The root LatexNode.
        self.root_latex = None
        # Base data set being worked with.
        self.base_data = base_data
        # Latex tree.
        self.latex_tree = LatexTree()

    def render(self):
        """
        Render the Latex tree code.

        Returns: Complete Latex code for displaying the tree.

        """
        return self.latex_tree.render()

    def get_restoring_decisions(self):
        """
        Get decisions to restore and start down left branch of state in question.

        Returns: TODO: Nothing?

        """
        # Enqueue each decision into restoring decisions.
        for state in self.states[:-1]:
            self.restoring_decisions.enqueue(state.last_decision)
        # Start exploring right branch of state, as last of restoration decisions.
        self.restoring_decisions.enqueue(False)

    # Algorithm execution manager.
    def execution_manager(self):
        # Initialize data list.
        self.data = self.base_data.copy()
        # Execute algorithm until every possible path has been taken.
        while True:
            # Run algorithm.
            self.algorithm()
            # Terminate with blank node if last comparison is invalid.
            self.check_valid()
            # If algorithm was not already terminated, add leaf.
            if not self.lame_duck:
                self.terminate_path(is_blank=False)
            # Find the next branch to analyze.
            self.find_branch()
            # Exit once all paths taken.
            if self.states.is_empty():
                break
            # Get decisions to be made to get to that branch.
            self.get_restoring_decisions()
        # Point Latex tree to root node.
        self.latex_tree.root = self.root_latex

    def find_branch(self):
        """
        Pop states until a state who's right path has not been explored is found.

        Returns:

        """
        while not self.states.is_empty() and not self.states.top().last_decision:
            self.states.pop()
        # If all states have been popped, exit.
        if self.states.is_empty():
            return
        # Put in restoring mode and out of lame duck mode.
        self.restoring = True
        self.lame_duck = False
        # Get the state in question.
        state = self.states.top()
        # Update the last decision made and the comparison outcome at this state.
        new_comp = state.comp.negate()
        state.last_decision = False
        state.comp = new_comp
        # Change data back to the initial base data.
        self.data = self.base_data.copy()
        # TODO: change 'comp' to something like 'truth'.

    def add_node(self, new_comp):
        """
        Add a node to the execution path.

        Args:
            new_comp (Comparison): Comparison made at this node.

        Returns:

        """
        # Get latest state.
        latest_state = self.states.top()
        # Create new LatexNode.
        text = str(new_comp)
        is_left = latest_state.last_decision
        new_node = LatexNode(
            val=text,
            is_leaf=False,
            is_left=is_left
        )
        # Link node at latest state to this new node.
        latest_node = latest_state.node
        if is_left:
            latest_node.left = new_node
        else:
            latest_node.right = new_node
        # Get a new state and push to states.
        new_state = State(new_node, new_comp)
        self.states.push(new_state)

    def terminate_path(self, is_blank):
        """
        Terminate an execution path.

        Args:
            is_blank (bool): Whether or not the node is blank.

        Returns:

        """
        # Get latest state.
        latest_state = self.states.top()
        # Get a leaf LatexNode.
        is_left = latest_state.last_decision
        # TODO: change formatting.
        text = 'null' if is_blank else ' '.join(self.data)
        new_node = LatexNode(
            val=text,
            is_leaf=True,
            is_left=is_left
        )
        # Link node at latest state to this new node.
        latest_node = latest_state.node
        if is_left:
            latest_node.left = new_node
        else:
            latest_node.right = new_node
        # Let algorithm run its course.
        self.lame_duck = True

    def first_comp(self, new_comp):
        """
        Handle the first comparison (special case).

        Args:
            new_comp (Comparison): The comparison made at root.

        Returns:

        """
        # Create root LatexNode.
        text = str(new_comp)
        new_node = LatexNode(
            val=text,
            root=True
        )
        # Get a new state and push to states.
        new_state = State(new_node, new_comp)
        self.states.push(new_state)
        # Set the root LatexNode.
        self.root_latex = new_node

    def check_valid(self):
        """
        Check if current point is valid.

        Returns: True if valid, False if not.

        """
        # Get last comparison.
        last_comp = self.states.top().comp
        # Check if negation was a previous comparison and terminate if so.
        if last_comp.negate() in (x.comp for x in self.states[:-1]):
            self.terminate_path(is_blank=True)
            return False
        return True

    def comp(self, e1, op, e2):
        """
        Handle a comparison (branch).

        Args:
            e1: First element.
            op: Operator.
            e2: Second element.

        Returns: TODO: Nothing?

        """
        # If algorithm is running its course, always return True.
        if self.lame_duck:
            return True
        # If restoring to execution state, make next required decision.
        if self.restoring:
            decision = self.restoring_decisions.dequeue()
            # If no more decisions left, end restoring mode.
            if self.restoring_decisions.is_empty():
                self.restoring = False
            return decision
        # Comparison being made.
        comp = Comparison(e1, op, e2)
        # Handle first comparison special case and branch left.
        if self.states.is_empty():
            self.first_comp(comp)
            return True
        # Get latest state.
        latest_state = self.states.top()
        # Terminate path if last comparison was invalid.
        if not self.check_valid():
            return True
        # Add new node to the execution path.
        self.add_node(comp)
        # Continue down left branch.
        return True

    # Algorithm method, overridden in inheritor.
    def algorithm(self):
        raise NotImplementedError('This method should be overridden with an algorithm implementation.')


# Example Bubble Sort algorithm.
class BubbleSort(TreeGenerator):
    def algorithm(self):
        for i in range(len(self.data) - 2, -1, -1):
            for j in range(i + 1):
                if self.comp(self.data[j], '>', self.data[j + 1]):
                    tmp = self.data[j]
                    self.data[j] = self.data[j + 1]
                    self.data[j + 1] = tmp


class InsertionSort(TreeGenerator):
    def algorithm(self):
        for i in range(1, len(self.data)):
            elem = self.data[i]
            j = i - 1
            while j >= 0 and self.comp(self.data[j], '>', elem):
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = elem


class ShellSort(TreeGenerator):
    def algorithm(self):
        gap = len(self.data) // 2
        while gap > 0:
            for i in range(gap, len(self.data)):
                temp = self.data[i]
                j = i
                # Sort the sub list for this gap
                while j >= gap and self.comp(self.data[j - gap], '>', temp):
                    self.data[j] = self.data[j - gap]
                    j = j - gap
                self.data[j] = temp
            # Reduce the gap for the next element
            gap = gap // 2


if __name__ == '__main__':
    tree_gen = ShellSort(['a', 'b', 'c', 'd', 'e'])
    tree_gen.execution_manager()
    print(tree_gen.render())
