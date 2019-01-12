"""
Holds extra libraries needed by the main tree generator.

"""


class Comparison:
    """
    For maintaining information regarding comparisons.
    TODO: possibly handle non-unique lists.

    Attributes:
        e1: First comparison element.
        op: The operator.
        e2: Second comparison element.

    """
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
        """
        Format comparison in a standard format.

        Returns: Formatted comparison.

        """
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
            # If comparison equal to negation, check cross equivalence.
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


class State:
    """
    Information about the state of execution at a branch.

    Attributes:
        last_decision (bool): Last decision made at this state.
        node: LatexNode at this branch.
        comp (Comparison): Comparison made at this node.

    """

    def __init__(self, node, comp):
        self.last_decision = True
        self.node = node
        self.comp = comp
