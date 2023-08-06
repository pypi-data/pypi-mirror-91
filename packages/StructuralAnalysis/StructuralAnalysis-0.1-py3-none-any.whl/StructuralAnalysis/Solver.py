from StructuralAnalysis.SolverHelper import *
import sys


def analyze_first_order_elastic(structure: Structure):
    global_matrix = global_elastic_matrix(structure)
    ff, fs, sf, ss = partition_global_matrix(structure, global_matrix)
    support_settlements = restrained_displacement_vector(structure)
    external_force_vector = force_vector(structure)

    if linalg.cond(ff) >= 1 / sys.float_info.epsilon:
        print("Matrix is singular or ill-conditioned! Check for stability.")
    else:
        displacements = solve_for_displacements(structure, ff, fs, support_settlements, external_force_vector)
        reactions = solve_for_reactions(structure, displacements, support_settlements, sf, ss)
        # print(linalg.slogdet(structure.ff_matrix()))
        print("*********DISPLACEMENTS***********")
        print(displacements)
        print("***********REACTIONS*************")
        print(reactions)


def analyze_second_order_elastic(structure):
    lamda = 20
    load_step = dot(1/lamda, force_vector(structure))
    for iteration in range(lamda):
        global_matrix = global_elastic_geometric_matrix(structure)
        ff, fs, sf, ss = partition_global_matrix(structure, global_matrix)
        support_settlements = restrained_displacement_vector(structure)
        external_force_vector = load_step

        if linalg.cond(ff) >= 1 / sys.float_info.epsilon:
            print("Matrix is singular or ill-conditioned! Check for stability.")
        else:
            displacements = solve_for_displacements(structure, ff, fs, support_settlements, external_force_vector)
            reactions = solve_for_reactions(structure, displacements, support_settlements, sf, ss)
            print("*********DISPLACEMENTS***********")
            print(displacements)
            print("***********REACTIONS*************")
            print(reactions)
            update_node_coordinates(structure)
            for element in structure.elements:
                element.update_deformed_shape()
