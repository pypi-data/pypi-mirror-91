# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

__author__ = "Sarath Menon, Jan Janssen"
__copyright__ = (
    "Copyright 2020, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0"
__maintainer__ = "Jan Janssen"
__email__ = "janssen@mpie.de"
__status__ = "production"
__date__ = "Feb 28, 2020"


func_list = [
    'file', 'extract_global', 'extract_box', 'extract_atom',
    'extract_fix', 'extract_variable', 'get_natoms', 'set_variable',
    'reset_box', 'generate_atoms', 'set_fix_external_callback',
    'get_neighlist', 'find_pair_neighlist', 'find_fix_neighlist',
    'find_compute_neighlist', 'get_neighlist_size',
    'get_neighlist_element_neighbors', 'command', 'gather_atoms',
    'scatter_atoms', 'get_thermo', 'extract_compute',
]

prop_list = [
    'version', 'natoms', 'has_exceptions', 'has_gzip_support',
    'has_png_support', 'has_jpeg_support', 'has_ffmpeg_support',
    'installed_packages',
]

command_list = [
    'angle_coeff', 'angle_style', 'atom_modify',
    'atom_style', 'atom_style', 'balance',
    'bond_coeff', 'box',
    'bond_style', 'boundary', 'change_box',
    'clear', 'comm_modify',
    'compute', 'compute_modify',
    'create_atoms', 'create_bonds',
    'create_box', 'delete_atoms', 'delete_bonds',
    'dielectric', 'dihedral_coeff', 'dihedral_style',
    'dimension', 'displace_atoms',
    'dump', 'dynamical_matrix', 'fix', 'fix_modify',
    'echo', 'group2ndx', 'ndx2group',
    'group', 'hyper',
    'improper_coeff', 'improper_style',
    'include', 'info', 'jump', 'kim_init',
    'kim_interactions', 'kim_query', 'kim_param',
    'kspace_modify', 'kspace_style',
    'label', 'log', 'message',
    'min_modify',
    'lattice', 'mass', 'minimize', 'minimize/kk', 'min_style',
    'molecule', 'neb', 'neb/spin', 'next',
    'neighbor', 'neigh_modify', 'newton', 'nthreads',
    'package',
    'pair_coeff', 'pair_modify', 'pair_style', 'pair_write',
    'partition', 'prd', 'print', 'python',
    'processors', 'read', 'read_data', 'read_dump', 'read_restart',
    'region', 'replicate', 'rerun', 'reset_ids', 'reset_timestep',
    'restart', 'run', 'run_style',
    'server', 'set', 'shell', 'special_bonds',
    'suffix', 'tad', 'temper',
    'thermo',
    'thermo_modify', 'thermo_style', 'third_order', 'timer',
    'timestep',
    'uncompute',
    'undump', 'unfix', 'units',
    'variable', 'velocity',
    'write_coeff', 'write_data', 'write_dump',
    'write_restart'
]

thermo_list = [
    "step", "elapsed", "elaplong", "dt", "time",
    "cpu", "tpcpu", "spcpu", "cpuremain", "part", "timeremain",
    "atoms", "temp", "press", "pe", "ke", "etotal", "enthalpy",
    "evdwl", "ecoul", "epair", "ebond", "eangle", "edihed", "eimp",
    "emol", "elong", "etail",
    "vol", "density", "lx", "ly", "lz", "xlo", "xhi", "ylo", "yhi", "zlo", "zhi",
    "xy", "xz", "yz", "xlat", "ylat", "zlat",
    "bonds", "angles", "dihedrals", "impropers",
    "pxx", "pyy", "pzz", "pxy", "pxz", "pyz",
    "fmax", "fnorm", "nbuild", "ndanger",
    "cella", "cellb", "cellc", "cellalpha", "cellbeta", "cellgamma"
]
