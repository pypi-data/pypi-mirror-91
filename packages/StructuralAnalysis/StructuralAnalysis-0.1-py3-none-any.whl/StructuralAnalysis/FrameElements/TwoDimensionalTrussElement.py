"""
This class inherits from Element.
properties:
    self._degrees_of_freedom: 4 degrees of freedom (2 per node) - 2D element
"""


from numpy import *
from StructuralAnalysis.FrameElements.Element import Element


class TwoDimensionalTrussElement(Element):

    def _local_matrix(self):
        axial_rigidity = self.material.elasticity_modulus * self.section.area / self.length
        return axial_rigidity * array([[1, -1],
                                       [-1, 1]])

    def _transformation_matrix(self):
        x_diff = self.end_node.x - self.start_node.x
        y_diff = self.end_node.y - self.start_node.y

        lamda_x = x_diff / self.length
        lamda_y = y_diff / self.length
        return array([[lamda_x, lamda_y, 0, 0],
                     [0, 0, lamda_x, lamda_y]])

    @property
    def _degrees_of_freedom(self):
        return [self.start_node.dof_1,
                self.start_node.dof_2,
                self.end_node.dof_1,
                self.end_node.dof_2]

    @property
    def matrix(self) -> array:
        return dot(dot(self._transformation_matrix().T, self._local_matrix()),
                   self._transformation_matrix())
