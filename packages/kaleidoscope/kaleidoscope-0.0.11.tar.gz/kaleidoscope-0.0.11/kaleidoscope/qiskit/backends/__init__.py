# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
==================================================================
IBM Quantum Backend Routines (:mod:`kaleidoscope.qiskit.backends`)
==================================================================

.. currentmodule:: kaleidoscope.qiskit.backends

System visualizations
=====================

.. autosummary::
   :toctree: ../stubs/

   system_error_map
   system_gate_map
   cnot_error_density

"""

from .mpl.cnot_err import cnot_error_density
from .interactive import system_error_map, system_gate_map
