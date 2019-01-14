from .data_structures import Stack, Queue
from .extra import Comparison, State
from .latex import LatexTree, LatexNode


class TreeGenerator:
    """
    Main tree generation.

    Attributes:
        restoring (bool): Whether algorithm is restoring a state.
        lame_duck (bool): Whether algorithm is running out its course.
        restoring_decisions (Queue): Decisions to get back to a state.
        states (Stack): States to get to the current execution point.
        data (list): The list being manipulated.
        root_latex (LatexNode): Root LatexNode.
        base_data (list): Base data list being manipulated (unchanging).
        latex_tree (LatexTree): Latex tree.

    """
    def __init__(self, base_data):
        self.restoring = False
        self.lame_duck = False
        self.restoring_decisions = Queue()
        self.states = Stack()
        self.data = []
        self.root_latex = None
        self.base_data = base_data
        self.latex_tree = LatexTree()

    def render(self):
        """
        Render the Latex tree code.

        Returns: Complete Latex code for displaying the tree.

        """
        return self.latex_tree.render()

    def get_restoring_decisions(self):
        """
        Get decisions to restore a state and begin down right path (False).

        """
        # Enqueue each decision into restoring decisions.
        for state in self.states[:-1]:
            self.restoring_decisions.enqueue(state.last_decision)
        # Start exploring right branch of state, as last of restoration decisions.
        self.restoring_decisions.enqueue(False)

    def execute(self):
        """
        Algorithm execution manager.

        """
        # Initialize mutable data list.
        self.data = self.base_data.copy()
        # Execute algorithm until every possible path has been taken.
        while True:
            # Run algorithm.
            self.algorithm()
            # Terminate with blank node if last comparison is invalid.
            self.terminate_if_invalid()
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
        Pop states until a state who's right path has not been taken is found.

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

    def add_node(self, new_comp):
        """
        Add a state and node to the execution path.

        Args:
            new_comp (src.extra.Comparison): Comparison made at this node.

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
            new_comp (src.extra.Comparison): The comparison made at root.

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

    def terminate_if_invalid(self):
        """
        Check if last comparison is valid, terminating if not.

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

        Returns: True if algorithm should branch left, False if it should branch right.

        """
        # If algorithm is running its course, always return False.
        if self.lame_duck:
            return False
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
        # Terminate path if last comparison was invalid.
        if not self.terminate_if_invalid():
            return False
        # Add new node to the execution path.
        self.add_node(comp)
        # Continue down left branch.
        return True

    # Algorithm method, overridden in inheritor.
    def algorithm(self):
        raise NotImplementedError('This method should be overridden with an algorithm implementation.')
