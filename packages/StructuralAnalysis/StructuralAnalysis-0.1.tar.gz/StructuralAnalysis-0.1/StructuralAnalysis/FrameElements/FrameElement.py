"""
This class inherits from Element.
properties:
    self._degrees_of_freedom: 12 degrees of freedom (6 per node) - 3D element
    self._transformation_matrix: does not take into account tilt angle (self.beta_angle) of the element
"""


from numpy import *
from StructuralAnalysis.FrameElements.Element import Element
from math import *


class FrameElement(Element):

    def __init__(self, start_node, end_node, section, material, beta_angle):
        super().__init__(start_node, end_node, section, material)
        self.beta_angle = radians(beta_angle)
        self.number_of_stations = 10

    def _local_matrix(self):
        l = self.length
        a = self.material.elasticity_modulus * self.section.area / l
        eiz = self.material.elasticity_modulus * self.section.inertia_z
        eiy = self.material.elasticity_modulus * self.section.inertia_y
        bz = 12 * eiz / (l ** 3)
        cz = 6 * eiz / (l ** 2)
        dz = 4 * eiz / l
        ez = 2 * eiz / l
        by = 12 * eiy / (l ** 3)
        cy = 6 * eiy / (l ** 2)
        dy = 4 * eiy / l
        ey = 2 * eiy / l
        t = self.section.polar_inertia*self.material.shear_modulus / l
        return array([[a,    0,     0,    0,    0,    0,    -a,   0,    0,    0,    0,    0],
                      [0,    bz,    0,    0,    0,    cz,   0,    -bz,  0,    0,    0,    cz],
                      [0,    0,     by,   0,    -cy,  0,    0,    0,    -by,  0,    -cy,  0],
                      [0,    0,     0,    t,    0,    0,    0,    0,    0,    -t,    0,   0],
                      [0,    0,     -cy,  0,    dy,   0,    0,    0,    cy,   0,    ey,   0],
                      [0,    cz,    0,    0,    0,    dz,   0,    -cz,  0,    0,    0,    ez],
                      [-a,   0,     0,    0,    0,    0,    a,    0,    0,    0,    0,    0],
                      [0,    -bz,   0,    0,    0,    -cz,  0,    bz,   0,    0,    0,    -cz],
                      [0,    0,     -by,  0,    cy,   0,    0,    0,    by,   0,    cy,   0],
                      [0,    0,     0,   -t,    0,    0,    0,    0,    0,    t,    0,    0],
                      [0,    0,     -cy,  0,    ey,   0,    0,    0,    cy,   0,    dy,   0],
                      [0,    cz,    0,    0,    0,    ez,   0,    -cz,  0,    0,    0,    dz]])

    # def _geometric_matrix(self, force_vector: array):
    #     fx2 = force_vector[[0]]
    #     Mx2 = force_vector[[0]]
    #     fx = force_vector[[0]]
    #     fx = force_vector[[0]]
    #     fx = force_vector[[0]]
    #     fx = force_vector[[0]]
    #     fx = force_vector[[0]]
    #     fx = force_vector[[0]]
    #     fx = force_vector[[0]]
    #     fx = force_vector[[0]]
    #
    #     l = self.length
    #
    #     return array([[fx2/l,    0,     0,    0,    0,    0,    -fx2/l,   0,    0,    0,    0,    0],
    #                   [0,    6*fx2/(5*l),    0,    my1/l,    mx2/l,    fx2/10,   0,    -6*fx2/(5*l),  0,    my2/l,    -mx2/l,    fx2/10],
    #                   [0,    0,     6*fx2/(5*l),   mz1/l,    -fx2/10,  0,    0,    0,    -by,  0,    -cy,  0],
    #                   [0,    0,     0,    t,    0,    0,    0,    0,    0,    -t,    0,   0],
    #                   [0,    0,     -cy,  0,    dy,   0,    0,    0,    cy,   0,    ey,   0],
    #                   [0,    cz,    0,    0,    0,    dz,   0,    -cz,  0,    0,    0,    ez],
    #                   [-a,   0,     0,    0,    0,    0,    a,    0,    0,    0,    0,    0],
    #                   [0,    -bz,   0,    0,    0,    -cz,  0,    bz,   0,    0,    0,    -cz],
    #                   [0,    0,     -by,  0,    cy,   0,    0,    0,    by,   0,    cy,   0],
    #                   [0,    0,     0,   -t,    0,    0,    0,    0,    0,    t,    0,    0],
    #                   [0,    0,     -cy,  0,    ey,   0,    0,    0,    cy,   0,    dy,   0],
    #                   [0,    cz,    0,    0,    0,    ez,   0,    -cz,  0,    0,    0,    dz]])


    def _transformation_matrix(self):
        if self.start_node.x == self.end_node.x and self.start_node.y == self.end_node.y:
            if self.end_node.z > self.start_node.z:
                matrix_gama = array([[0, 0, 1],
                                     [0, 1, 0],
                                     [-1, 0, 0]])
            else:
                matrix_gama = array([[0, 0, -1],
                                     [0, 1, 0],
                                     [1, 0, 0]])
        else:
            cxx = (self.end_node.x - self.start_node.x)/self.length
            cyx = (self.end_node.y - self.start_node.y)/self.length
            czx = (self.end_node.z - self.start_node.z)/self.length
            d = sqrt(cxx**2 + cyx**2)
            cxy = -cyx/d
            cyy = cxx/d
            czy = 0
            cxz = -cxx*czx/d
            cyz = -cyx*czx/d
            czz = d
            matrix_gama = array([[cxx, cyx, czx],
                                 [cxy, cyy, czy],
                                 [cxz, cyz, czz]])

        transformation_matrix = zeros((len(self._degrees_of_freedom), len(self._degrees_of_freedom)))
        for i in range(4):
            transformation_matrix[(i*3):(i+1)*3, (i*3):(i+1)*3] = matrix_gama

        return transformation_matrix

    def get_station_local_coord(self):
        local_coordinates = zeros((11, 3))
        inter_station_length = self.length / self.number_of_stations
        for i in range(0, self.number_of_stations+1):
            local_coordinates[i] = array([i*inter_station_length, 0, 0])
        return local_coordinates

    def get_stations_global_coordinates(self):
        local_coordinates = self.get_station_local_coord()
        transformed_coordinates = zeros((11, 3))
        transformation_matrrix = self._transformation_matrix()[0:3, 0:3]
        i = 0
        for station_coordinates in local_coordinates:
            transformed_coordinates[i] = dot(transformation_matrrix.T, station_coordinates.T) + \
                                         array([self.start_node.x, self.start_node.y, self.start_node.z])
            i += 1

        return array(transformed_coordinates)

    def get_stations_local_displacement(self):
        local_end_displacements = self.get_local_end_displacements()
        local_end_displacements_reordered = array([local_end_displacements[0],
                                                   local_end_displacements[6],
                                                   local_end_displacements[1],
                                                   local_end_displacements[7],
                                                   local_end_displacements[5],
                                                   local_end_displacements[11],
                                                   local_end_displacements[2],
                                                   local_end_displacements[8],
                                                   local_end_displacements[4],
                                                   local_end_displacements[10]])

        stations_local_displacement = zeros((11, 3))
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
            shape_func_matrix = array([[N1, N2, 0,  0,  0,  0,  0,  0,  0,  0],
                                      [0,  0,  N3, N4, N5, N6, 0,  0,  0,  0],
                                      [0,  0,  0,  0,  0,  0,  N3, N4, -N5, -N6]])
            stations_local_displacement[i] = dot(shape_func_matrix, local_end_displacements_reordered)
            i += 1

        return stations_local_displacement

    def get_stations_global_displaced_position(self):
        stations_global_displaced_position = zeros((11, 3))
        stations_local_displacements = self.get_stations_local_displacement()
        i = 0
        for displacements in stations_local_displacements:

            global_displacement = dot((self._transformation_matrix()[0:3, 0:3]).T, displacements.T)
            global_position = global_displacement + self.get_stations_global_coordinates()[i]
            stations_global_displaced_position[i] = global_position
            i += 1
        return stations_global_displaced_position

    def get_local_end_displacements(self):
        global_displacements = array([dof.displacement for dof in self._degrees_of_freedom])
        return dot(self._transformation_matrix(), global_displacements)

    @property
    def _degrees_of_freedom(self):
        return [self.start_node.dof_1, self.start_node.dof_2, self.start_node.dof_3,
                self.start_node.dof_4, self.start_node.dof_5, self.start_node.dof_6,
                self.end_node.dof_1, self.end_node.dof_2, self.end_node.dof_3,
                self.end_node.dof_4, self.end_node.dof_5, self.end_node.dof_6]

    @property
    def matrix(self) -> array:
        return dot(dot(self._transformation_matrix().T, self._local_matrix()),
                   self._transformation_matrix())

    @property
    def elastic_geometric_matrix(self):
        return None
