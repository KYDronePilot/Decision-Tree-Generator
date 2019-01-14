"""
Some example algorithms to generate decision trees for.

"""
from decision_tree import TreeGenerator


class BubbleSort(TreeGenerator):
    """
    Simple Bubble Sort algorithm.

    """
    def algorithm(self):
        for i in range(len(self.data) - 2, -1, -1):
            for j in range(i + 1):
                if self.comp(self.data[j], '>', self.data[j + 1]):
                    tmp = self.data[j]
                    self.data[j] = self.data[j + 1]
                    self.data[j + 1] = tmp


class InsertionSort(TreeGenerator):
    """
    Insertion Sort algorithm.

    """
    def algorithm(self):
        for i in range(1, len(self.data)):
            elem = self.data[i]
            j = i - 1
            while j >= 0 and self.comp(self.data[j], '>', elem):
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = elem


class ShellSort(TreeGenerator):
    """
    Shell Sort algorithm (not written by me, KYDronePilot).

    """
    def algorithm(self):
        gap = len(self.data) // 2
        while gap > 0:
            for i in range(gap, len(self.data)):
                temp = self.data[i]
                j = i
                while j >= gap and self.comp(self.data[j - gap], '>', temp):
                    self.data[j] = self.data[j - gap]
                    j = j - gap
                self.data[j] = temp
            gap = gap // 2


if __name__ == '__main__':
    # Pass elements you want manipulated to the algorithm class's constructor as a list of chars.
    bubble = BubbleSort(['a', 'b', 'c', 'd'])
    insertion = InsertionSort(['x', 'y', 'z', 'a'])
    shell = ShellSort(['w', 'a', 's', 'd'])
    # Run the execute method to generate the tree structure.
    # Change name to try other algorithms.
    shell.execute()
    # Run the render method to render and return the Latex code for the tree structure.
    code = shell.render()
    print(code)
