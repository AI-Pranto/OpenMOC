#!/usr/bin/env python

import os
import sys
import hashlib
sys.path.insert(0, os.pardir)
sys.path.insert(0, os.path.join(os.pardir, 'openmoc'))
from testing_harness import TestHarness
from input_set import SimpleLatticeInput
import openmoc.process as process
import numpy as np


class MeshReactionRateTallyTestHarness(TestHarness):
    """An eigenvalue calculation with a mesh tally of the fission rates
    using the openmoc.process module."""

    def __init__(self):
        super(MeshReactionRateTallyTestHarness, self).__init__()
        self.input_set = SimpleLatticeInput()

    def _run_openmoc(self):
        """Run an OpenMOC eigenvalue calculation."""
        super(MeshReactionRateTallyTestHarness, self)._run_openmoc()

    def _get_results(self, num_iters=True, keff=True, fluxes=True,
                     num_fsrs=True, num_tracks=True, num_segments=True,
                     hash_output=True):
        """Digest info from the mesh tallies and return as a string."""

        # Create OpenMOC Mesh on which to tally reaction rates
        mesh = process.Mesh()
        mesh.dimension = [4, 4]
        mesh.lower_left = [-2., -2.]
        mesh.upper_right = [2., 2.]
        mesh.width = [1., 1.]
        
        outstr = ""
        for rxn in ('fission', 'flux', 'total', 'nu-fission', 'scatter'):
            # Tally OpenMOC reaction rates on the Mesh
            rxn_rates = mesh.tally_reaction_rates_on_mesh(
                self.solver, rxn, volume='integrated')
            # Append reaction rates to the output string
            outstr += rxn.title() + ' Rate Mesh Tally\n'
            rates = ['{0:12.6E}'.format(rate) for rate in rxn_rates.ravel()]
            outstr += '\n'.join(rates) + '\n'
    
        return outstr


if __name__ == '__main__':
    harness = MeshReactionRateTallyTestHarness()
    harness.main()
