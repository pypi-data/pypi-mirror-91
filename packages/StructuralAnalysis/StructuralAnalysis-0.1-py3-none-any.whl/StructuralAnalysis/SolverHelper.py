from numpy import *
from StructuralAnalysis.Structure import Structure


def global_elastic_matrix(structure: Structure):
    ndof = structure.no_of_degrees_of_freedom
    initialized_matrix = zeros((ndof, ndof))
    for element in structure.elements:
        element_matrix = zeros((ndof, ndof))
        i = 0
        for row in element.matrix:
            j = 0
            for col in row:
                k, z = element._degrees_of_freedom[i].id-1, element._degrees_of_freedom[j].id-1
                element_matrix[k, z] = col
                j += 1
            i += 1
        initialized_matrix = add(initialized_matrix, element_matrix)

    return initialized_matrix


def global_elastic_geometric_matrix(structure: Structure):
    ndof = structure.no_of_degrees_of_freedom
    initialized_matrix = zeros((ndof, ndof))
    for element in structure.elements:
        element_matrix = zeros((ndof, ndof))
        i = 0
        for row in element.elastic_geometric_matrix:
            j = 0
            for col in row:
                k, z = element._degrees_of_freedom[i].id-1, element._degrees_of_freedom[j].id-1
                element_matrix[k, z] = col
                j += 1
            i += 1
        initialized_matrix = add(initialized_matrix, element_matrix)

    return initialized_matrix


def partition_global_matrix(structure, global_matrix):

    def ff_matrix():
        ndof = len(structure.free_degrees_of_freedom)
        ff_matrix = zeros((ndof, ndof))
        i = 0
        for dof_i in structure.free_degrees_of_freedom:
            j = 0
            for dof_j in structure.free_degrees_of_freedom:
                current = global_matrix[dof_i.id - 1, dof_j.id - 1]
                ff_matrix[i, j] = current
                j += 1
            i += 1
        return ff_matrix

    def fs_matrix():
        ndoff = len(structure.free_degrees_of_freedom)
        ndofs = len(structure.restrained_degrees_of_freedom)
        fs_matrix = zeros((ndoff, ndofs))
        i = 0
        for dof_i in structure.free_degrees_of_freedom:
            j = 0
            for dof_j in structure.restrained_degrees_of_freedom:
                current = global_matrix[dof_i.id - 1, dof_j.id - 1]
                fs_matrix[i, j] = current
                j += 1
            i += 1
        return fs_matrix

    def sf_matrix():
        ndoff = len(structure.free_degrees_of_freedom)
        ndofs = len(structure.restrained_degrees_of_freedom)
        sf_matrix = zeros((ndofs, ndoff))
        i = 0
        for dof_i in structure.restrained_degrees_of_freedom:
            j = 0
            for dof_j in structure.free_degrees_of_freedom:
                sf_matrix[i, j] = global_matrix[dof_i.id - 1, dof_j.id - 1]
                j += 1
            i += 1
        return sf_matrix

    def ss_matrix():
        ndof = len(structure.restrained_degrees_of_freedom)
        ss_matrix = zeros((ndof, ndof))
        i = 0
        for dof_i in structure.restrained_degrees_of_freedom:
            j = 0
            for dof_j in structure.restrained_degrees_of_freedom:
                ss_matrix[i, j] = global_matrix[dof_i.id - 1, dof_j.id - 1]
                j += 1
            i += 1
        return ss_matrix

    return ff_matrix(), fs_matrix(), sf_matrix(), ss_matrix()


def force_vector(structure):
    forces = zeros((len(structure.free_degrees_of_freedom)))
    i = 0
    for dof in structure.free_degrees_of_freedom:
        forces[i] = dof.force
        i += 1
    return forces


def restrained_displacement_vector(structure):
    displacements = zeros((len(structure.restrained_degrees_of_freedom)))
    i = 0
    for dof in structure.restrained_degrees_of_freedom:
        displacements[i] = dof.displacement
        i += 1
    return displacements


def solve_for_displacements(structure, ff_matrix, fs_matrix, restrained_displacement_vector, force_vector):
    displacements = dot(linalg.inv(ff_matrix),
                        force_vector - dot(fs_matrix, restrained_displacement_vector))
    i = 0
    for dof in structure.free_degrees_of_freedom:
        dof.displacement = displacements[i]
        i += 1
    return displacements


def update_node_coordinates(structure):
    for node in structure.nodes:
        node.x = node.x + node.dof_1.displacement
        node.y = node.y + node.dof_2.displacement
        node.z = node.z + node.dof_3.displacement


def solve_for_reactions(structure, displacements, restrained_displacement_vector, sf_matrix, ss_matrix):
    reactions = dot(sf_matrix, displacements) + \
                dot(ss_matrix, restrained_displacement_vector)
    i = 0
    for dof in structure.restrained_degrees_of_freedom:
        dof.force = reactions[i]
        i += 1
    return reactions