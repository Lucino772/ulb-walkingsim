"""
3D PyChrono muscle-based walking simulator
File: test_genotype_to_phenotype.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Manual tests for spawning a creature (its phenotype) based on a
    genotype.
"""

import pychrono as chrono
import sys

import walkingsim.environment as environment
import walkingsim.visualiser as visualiser
import walkingsim.creature.genotype as genotype
import walkingsim.creature.phenotype.bone as bone


class TestsGenotypeToPhenotype:
    def __init__(self):
        self.env = environment.Environment()

    def run_tests(self):
        self.visuals = visualiser.Visualiser(self.env)
        self.visuals.run()

    def build_creature_with_one_part(self):
        #  g = genotype.Genotype()
        #  g.add_node(genotype.GenotypeNode((20, 20, 40)))
        b = bone.Bone((0.3, 1.80, 0.7))
        #  b.SetMass(80)
        self.env.Add(b)

    def build_creature_with_two_legs(self):
        trunk = bone.Bone((0.3, 1.0, 0.7), chrono.ChVectorD(0, 20, 0))
        self.env.Add(trunk)
        #  leg1 = bone.Bone((0.


if __name__ == "__main__":
    t = TestsGenotypeToPhenotype()
    #  t.build_creature_with_one_part()
    t.build_creature_with_two_legs()
    t.run_tests()
