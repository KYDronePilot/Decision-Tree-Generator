# Decision-Tree-Generator
A Python script for generating LaTeX code for decision trees of simple algorithms

![Bubble Sort Decision Tree](bubble_sort_example.png)

## Overview
This project originated with the idea of being able to generate a pruned, valid decision tree for any simple algorithm 
that performs operations on a small list of data. Above is an example of such a tree for the bubble sort algorithm with
the list of elements [a, b, c].

## Usage
When run, the program generates complete Latex code to form a pruned, valid decision tree for the algorithm entered.

The main Python script provides a class `TreeGenerator` which should be inherited, with the `algorithm` method 
overrided. In the algorithm method, an algorithm should be entered that performs operations on the `self.data` list.
Whenever a comparison of records is to be made, substitute the comparison with the following syntax:
```python
self.comp(<first record>, <comparison operator>, <second record>)
```

This function will manage how the algorithm runs, in order to generate the decision tree.