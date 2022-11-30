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

import environment
import visualiser
import genotype


class TestsGenotypeToPhenotype:
    def __init__(self):
        self.env = environment.Environment()
        self.visuals = visualiser.Visualiser(self.env)

    def run_tests(self):
        self.visuals.run()

    def build_genotype_1(self):
        g = genotype.Genotype()
