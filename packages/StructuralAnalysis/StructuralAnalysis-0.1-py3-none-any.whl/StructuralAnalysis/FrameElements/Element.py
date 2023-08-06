"""
This class is an abstract class.
attributes:
    self.start_node: node object initialized by user
    self.end_node: other node object initialized by user
    self.section: section object initialized by user
    self.material: material object initialized by user
    abstract methods and properties:
    self._local_matrix: stiffness matrix of the element in its local axis
    self._degrees_of_freedom: degrees of freedom of the element in global axis
    self._transformation_matrix
    self._matrix: stiffness matrix of the element in global axis
"""


from StructuralAnalysis.Node import Node
from math import sqrt
from numpy import *
from abc import abstractmethod, ABC
from StructuralAnalysis.DegreeOfFreedom import DegreeOfFreedom
from StructuralAnalysis.Section import Section
from StructuralAnalysis.Material import Material


class Element(ABC):
    id = 1

    def __init__(self, start_node: Node, end_node: Node, section: Section, material: Material):
        self.id = Element.id
        Element.id += 1
        self.start_node = start_node
        self.end_node = end_node
        self.section = section
        self.material = material
        self.length = sqrt((end_node.x - start_node.x) ** 2 +
                           (end_node.y - start_node.y) ** 2 +
                           (end_node.z - start_node.z) ** 2)

    @abstractmethod
    def _local_matrix(self) -> array:
        pass

    @abstractmethod
    def _transformation_matrix(self) -> array:
        pass

    @property
    @abstractmethod
    def _degrees_of_freedom(self) -> [DegreeOfFreedom]:
        pass

    @property
    @abstractmethod
    def matrix(self) -> array:
        pass

    @property
    @abstractmethod
    def elastic_geometric_matrix(self):
        pass
