"""
This class inherits from Element.
properties:
    self._degrees_of_freedom: 6 degrees of freedom (3 per node) - 2D element
"""


from numpy import *
from StructuralAnalysis.FrameElements.Element import Element


class TwoDimensionalFrameElement(Element):
    def __init__(self, start_node, end_node, section, material):
        super().__init__(start_node, end_node, section, material)
        self.end_forces = zeros(6)
        self.deformed_shape = zeros((11, 2))

    def _local_matrix(self):
        l = self.length
        a = self.material.elasticity_modulus * self.section.area / l
        ei = self.material.elasticity_modulus * self.section.inertia_z
        b = 12*ei/(l**3)
        c = 6*ei/(l**2)
        d = 4*ei/l
        e = 2*ei/l
        self.number_of_stations = 10
        return array([[a, 0, 0, -a, 0, 0],
                      [0, b, c, 0, -b, c],
                      [0, c, d, 0, -c, e],
                      [-a, 0, 0, a, 0, 0],
                      [0, -b, -c, 0, b, -c],
                      [0, c, e, 0, -c, d]])

    def _transformation_matrix(self):
        x_diff = self.end_node.x - self.start_node.x
        y_diff = self.end_node.y - self.start_node.y

        lamda_x = x_diff / self.length
        lamda_y = y_diff / self.length

        return array([[lamda_x, lamda_y, 0, 0, 0, 0],
                      [-lamda_y, lamda_x, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, lamda_x, lamda_y, 0],
                      [0, 0, 0, -lamda_y, lamda_x, 0],
                      [0, 0, 0, 0, 0, 1]])

    def geometric_matrix(self):
        self.end_forces += self.local_end_forces()
        fx2 = self.end_forces[3]
        print(fx2)
        l = self.length
        a = 6/5
        b = l/10
        c = 2*l**2 / 15
        d = l**2 / 30

        return dot(fx2/l, array([[1, 0, 0, -1, 0, 0],
                                 [0, a, b, 0, -a, b],
                                 [0, b, c, 0, -b, -d],
                                 [-1, 0, 0, 1, 0, 0],
                                 [0, -a, -b, 0, a, -b],
                                 [0, b, -d, 0, -b, c]]))

    def global_end_forces(self):
        displacements = array([dof.displacement for dof in self._degrees_of_freedom])
        print(displacements)
        print(shape(displacements))
        return dot(self.matrix, displacements)

    def local_end_forces(self):
        local_end_forces = dot(self._transformation_matrix(), self.global_end_forces())
        return local_end_forces

    # ***************
    def get_station_local_coord(self):
        local_coordinates = zeros((11, 2))
        inter_station_length = self.length / self.number_of_stations
        for i in range(0, self.number_of_stations+1):
            local_coordinates[i] = array([i*inter_station_length, 0])
        return local_coordinates

    def get_stations_global_coordinates(self):
        local_coordinates = self.get_station_local_coord()
        transformed_coordinates = zeros((11, 2))
        transformation_matrrix = self._transformation_matrix()[0:2, 0:2]
        i = 0
        for station_coordinates in local_coordinates:
            transformed_coordinates[i] = dot(transformation_matrrix.T, station_coordinates.T) \
                                         + array([self.start_node.x, self.start_node.y])
            i += 1
        return array(transformed_coordinates)

    def get_stations_local_displacement(self):
        local_end_displacements = self.get_local_end_displacements()
        local_end_displacements_reordered = array([local_end_displacements[0],
                                                   local_end_displacements[3],
                                                   local_end_displacements[1],
                                                   local_end_displacements[4],
                                                   local_end_displacements[2],
                                                   local_end_displacements[5]])
        stations_local_displacement = zeros((11, 2))
        i = 0
        for station in self.get_station_local_coord():
            x = station[0]
            l = self.length
            N1 = 1 - x/l
            N2 = x/l
            N3 = 1 - 3*(x/l)**2 + 2*(x/l)**3
            N4 = 3*(x/l)**2 - 2*(x/l)**3
            N5 = x * (1 - x/l)**2
            N6 = x * ((x/l)**2 - x/l)
            shape_func_matrix = array([[N1, N2, 0,  0,  0,  0],
                                      [0,  0,  N3, N4, N5, N6]])
            stations_local_displacement[i] = dot(shape_func_matrix, local_end_displacements_reordered)
            i += 1
        return stations_local_displacement

    def get_stations_global_displaced_position(self):
        stations_global_displaced_position = zeros((11, 3))
        stations_local_displacements = self.get_stations_local_displacement()
        i = 0
        for displacements in stations_local_displacements:

            global_displacement = dot((self._transformation_matrix()[0:2, 0:2]).T, displacements.T)
            global_position = global_displacement + self.get_stations_global_coordinates()[i]
            stations_global_displaced_position[i] = append(global_position, 0)
            i += 1

        return stations_global_displaced_position

    def get_local_end_displacements(self):
        global_displacements = array([dof.displacement for dof in self._degrees_of_freedom])
        return dot(self._transformation_matrix(), global_displacements)

    @property
    def _degrees_of_freedom(self):
        return [self.start_node.dof_1,
                self.start_node.dof_2,
                self.start_node.dof_6,
                self.end_node.dof_1,
                self.end_node.dof_2,
                self.end_node.dof_6]

    @property
    def matrix(self) -> array:
        return dot(dot(self._transformation_matrix().T, self._local_matrix()),
                   self._transformation_matrix())

    @property
    def elastic_geometric_matrix(self):
        return dot(dot(self._transformation_matrix().T, self._local_matrix() +
                       self.geometric_matrix()),
                   self._transformation_matrix())
