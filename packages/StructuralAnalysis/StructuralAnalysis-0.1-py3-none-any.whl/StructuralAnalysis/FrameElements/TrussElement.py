"""
This class inherits from Element.
properties:
    self._degrees_of_freedom: 6 degrees of freedom (3 per node) - 3D element
"""


from numpy import *
from StructuralAnalysis.FrameElements.Element import Element


class TrussElement(Element):

    def _local_matrix(self):
        axial_rigidity = self.material.elasticity_modulus * self.section.area / self.length
        return axial_rigidity * array([[1, -1],
                                       [-1, 1]])

    def _transformation_matrix(self):
        x_diff = self.end_node.x - self.start_node.x
        y_diff = self.end_node.y - self.start_node.y
        z_diff = self.end_node.z - self.start_node.z

        lamda_x = x_diff / self.length
        lamda_y = y_diff / self.length
        lamda_z = z_diff / self.length

        return array([[lamda_x, lamda_y, lamda_z, 0, 0, 0],
                     [0, 0, 0, lamda_x, lamda_y, lamda_z]])

    @property
    def _degrees_of_freedom(self):
        return [self.start_node.dof_1,
                self.start_node.dof_2,
                self.start_node.dof_3,
                self.end_node.dof_1,
                self.end_node.dof_2,
                self.end_node.dof_3]

    @property
    def matrix(self) -> array:
        return dot(dot(self._transformation_matrix().T, self._local_matrix()),
                   self._transformation_matrix())
