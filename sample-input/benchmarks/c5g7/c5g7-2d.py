import openmoc
import openmoc.log as log
import openmoc.plotter as plotter
from openmoc.options import Options
from lattices import lattices, universes, cells, surfaces

###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.num_omp_threads
azim_spacing = options.azim_spacing
num_azim = options.num_azim
polar_spacing = options.polar_spacing
num_polar = options.num_polar
tolerance = options.tolerance
max_iters = options.max_iters

uu = universes['UO2 Unrodded Assembly']
ur = universes['UO2 Rodded Assembly']
mu = universes['MOX Unrodded Assembly']
mr = universes['MOX Rodded Assembly']
ru = universes['Reflector Unrodded Assembly']
rr = universes['Reflector Rodded Assembly']
ri = universes['Reflector Right Assembly']
rb = universes['Reflector Bottom Assembly']
rc = universes['Reflector Corner Assembly']

# 3 x 3 x 9 core to represent 3D core
lattices['Root'].setWidth(width_x=21.42, width_y=21.42)
lattices['Root'].setUniverses3D([[[uu, mu, ri],
                                  [mu, uu, ri],
                                  [rb, rb, rc]]])

cells['Root'].setFill(lattices['Root'])

###############################################################################
##########################     Creating Cmfd mesh    ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating Cmfd mesh...')

cmfd = openmoc.Cmfd()
cmfd.setSORRelaxationFactor(1.5)
cmfd.setLatticeStructure(51,51)
cmfd.setGroupStructure([1,4,8])
cmfd.setCentroidUpdateOn(True)
cmfd.setKNearest(3)

###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = openmoc.Geometry()
geometry.setRootUniverse(universes['Root'])
geometry.setCmfd(cmfd)
geometry.initializeFlatSourceRegions()

###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

quad = openmoc.EqualAnglePolarQuad()
quad.setNumPolarAngles(num_polar)

track_generator = openmoc.TrackGenerator(geometry, num_azim, num_polar,
                                         azim_spacing)
track_generator.setQuadrature(quad)
track_generator.setNumThreads(num_threads)
track_generator.generateTracks()

###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = openmoc.CPUSolver(track_generator)
solver.setConvergenceThreshold(tolerance)
solver.setNumThreads(num_threads)
solver.computeEigenvalue(max_iters)
solver.printTimerReport()

###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

plotter.plot_materials(geometry, gridsize=500)
plotter.plot_cells(geometry, gridsize=500)
plotter.plot_flat_source_regions(geometry, gridsize=500)
plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7],
                            gridsize=500, plane='xy', offset=0.)


log.py_printf('TITLE', 'Finished')
