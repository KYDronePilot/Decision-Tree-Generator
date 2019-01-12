# Base Latex code.
LATEX_BASE = """\
\\documentclass[tikz, border=5pt]{{standalone}}
\\usepackage{{forest}}

\\begin{{document}}
{content}
\\end{{document}}
"""
# Base forest code.
FOREST_BASE = """\
\\begin{{forest}}
  for tree={{
    edge label = {{font=\scriptsize}},
    circle,
    draw,
    if n children=0{{
      rectangle, draw
    }}{{}}
  }}
{tree_code}
\\end{{forest}}
"""


class LatexTree:
    """
    Code for rendering a Latex decision tree.

    Attributes:
        tree_code (str): Code for building the tree.
        root (LatexNode): Root node of the tree.

    """
    def __init__(self):
        self.tree_code = ''
        self.root = None

    def render(self):
        """
        Render the tree code.

        Returns: Valid Latex code for a tikz forest tree.

        """
        self.tree_code = ''
        self.root.render_forest(self, '  ')
        # Format into valid Latex code.
        forest_code = FOREST_BASE.format(tree_code=self.tree_code[:-1])
        return LATEX_BASE.format(content=forest_code)


class LatexNode:
    """
    Tree nodes that will print out the LaTeX code.

    Attributes:
        val (str): The value to be printed in the node.
        right (LatexNode): Right Latex node.
        left (LatexNode): Left Latex node.
        is_leaf (bool): Whether the node is a leaf.
        is_left (bool): Whether the node is a left branch of its parent.
        edge_label (str): Label on edge from parent to self.

    """
    # Template for node text.
    NODE_TEMPLATE = '{node}, edge label={{node[midway,fill=white,font=\\tiny] {{{edge}}}}}{newline}'
    # Tab padding space count.
    TAB_PAD = 2

    def __init__(self, val='', right=None, left=None, is_leaf=False, is_left=True, root=False):
        """

        :type right: LatexNode
        :type left: LatexNode

        """
        self.val = val if is_leaf else '${0}$'.format(val)
        self.right = right
        self.left = left
        self.is_leaf = is_leaf
        self.is_left = is_left
        # Determine edge label.
        if root:
            self.edge_label = ''
        else:
            self.edge_label = 'Yes' if is_left else 'No'

    def render_forest(self, tree, pad):
        """
        Render the LaTeX tree code in proper format for the forest package.

        Args:
            tree (LatexTree): The overarching tree object.
            pad (str): Space pad to place before each line of this subtree code.

        """
        # Start new subtree plus pad.
        tree.tree_code += pad + '[ '
        # Extra newline if node is not a leaf.
        newline = '\n' if not self.is_leaf else ''
        # If not a pruned node, format normally; else leave blank.
        if not self.val == 'null':
            tree.tree_code += LatexNode.NODE_TEMPLATE.format(
                node=self.val,
                edge=self.edge_label,
                newline=newline
            )
        else:
            tree.tree_code += ', phantom'
        # Recursively render children if they exist.
        new_pad = LatexNode.TAB_PAD * ' ' + pad
        if self.left is not None:
            self.left.render_forest(tree, new_pad)
        if self.right is not None:
            self.right.render_forest(tree, new_pad)
        # Add closing bracket.
        if not self.is_leaf:
            tree.tree_code += pad + ']' + '\n'
        else:
            tree.tree_code += ' ]' + '\n'
