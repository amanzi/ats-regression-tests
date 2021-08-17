# ATS Regression Test Suite


This is the regression test suite for ATS.

The full set of these runs should always work, and should always be run and, if necessary, updated prior to issuing a pull request.


## Quickstart

A basic python environment is needed -- for full details see the ATS python environment installation in the ATS Users Guide (work in progress, link coming!).  In the near term, a python3 installation that includes numpy, matplotlib, and h5py is likely sufficient.

To run the complete set of tests:

```
python regression_tests.py .
```

See also:
```
python regression_tests.py --help
```

## Test design

Developers should strive to include at least one new or modified test for each new process capability added to the code. 

Each test should be kept to under a minute of total runtime, and should prefer to be on a single core.  If tests add a new parallelization aspect, this should be tested with a single (or as few as possible) test(s) on multiple cores.  Recognize that many users develop on laptops with at most two physical cores, so parallel tests should try to stay small and short.  It is preferable to run two tests -- one parallel and extremely short (2-3 time steps even) and a second longer but serial to test -- to one long, parallel test.

Note that new tests are often fragile.  Floating point roundoff issues, compiler differences, and (especially) blas/lapack implementation differences often result in machine-precision level changes in answers.  These changes often cause drift in the final answer, especially if time stepping is adaptive (some timestep takes one more nonlinear iteration, which results in different timestep size records and different answers).  Try to run new tests on multiple machines to ensure that tolerances are reasonable (David Moulton and Ethan Coon can help with this if you do not have access to multiple machines).

## Using the test harness to run the tests

The test harness is built in python3, and requires the h5py package (to load checkpoint files) and numpy, along with a few other built-in packages.  It is distributed as a part of ATS (in [tools/testing/](https://github.com/amanzi/ats/tree/master/tools/testing).  The driving script is distributed in the regression test repository.  Tests can be run in two ways, via ctest and the standard Amanzi build system, or directly in python.

Typically the test harness assumes that the user has set the environmental variables:

    export AMANZI_SRC_DIR=/path/to/amanzi
    export ATS_SRC_DIR=${AMANZI_SRC_DIR}/src/physics/ats

### Download the test repository.

Note that the ats-regression-tests repo is also a submodule of the ATS repo, which itself is a submodule of the Amanzi repo.  Therefore, you get this the first time you install Amanzi via bootstrap, located at:

    $AMANZI_SRC_DIR/src/physics/ats/testing/ats-regression-tests

Alternatively, you can clone it directly:

    git clone https://github.com/amanzi/ats-regression-tests.git

### Run the test suite.

The test suite can be run in two ways.  The first is simply using standard ctest -- the tests are added via cmake in standard Amanzi-ATS configuration.  So after Amanzi-ATS is configured and built via bootstrap, one can simply:

    cd $AMANZI_BUILD_DIR
    make test

Alternatively, the test suite can be run manually in python.  Note that the ats-regression-tests suite is copied into the build directory so that all things are done "out of source."  The result of this is that running through `make test` and running directly in the source directory run _different copies_ of the test suite.  After bootstrap is run, the tests exist both at `$AMANZI_BUILD_DIR/src/physics/ats/testing/ats-regression-tests` and `$AMANZI_SRC_DIR/src/physics/ats/testing/ats-regression-tests`.

To run the test manually:

    cd $AMANZI_SRC_DIR/src/physics/ats/testing/ats-regression-tests
    python regression_tests.py .

Or to run a single test or suite of tests:

    python regression_tests.py 02_richards -t infiltration_fv


## Creating a new test:

* Create and `git add` the xml file to the repo.
* Add the name of the test to a .cfg file in the test's directory, e.g. `02_richards/richards.cfg`
* Make sure that checkpoints are being written at sane times, and add the option, "checkpoint=True" to xml files on evaluators whose results you wish to compare (e.g. saturation_liquid, etc).
* Run the test.  
   * If the test is sensitive to timestep size history (e.g. it is a variable timestep history problem) then use the strategy: `python regression_tests.py -n  --save-dt-history 0X_category/catagory.cfg -t my_test_name`. This runs your test twice -- once to get a sane timestep size history, then parses that, saves it to disk, writes a new input file that uses that exact sequence of step sizes, and runs a second time ensure that the results work with that timestep size history.  This is a huge help for reproducibility and removing false negatives -- the solution can be quite sensitive to timestep size history, but rarely do we want to flag when a non-bitwise repeatable change randomly causes a solver to take one more timestep, thereby changing the answer.
   * If the test can be a fixed timestep size run, then just `python regression_tests.py -n 0X_category/category.cfg -t my_test_name` is sufficient.
   * Finally, after you've added the test, run once more via `python regression_tests.py 0X_category/category.cfg -t my_test_name` (no `-n` this timie) to ensure that tolerances are good and the tests pass with what should be a bitwise identical run.
* Clean out the resulting gold directory: `./clean_gold.sh 0X_category/my_test_name.regression.gold` to make sure that only the checkpoint files and the ats_version.txt files are left.
* Commit and push.


## Updating tests:

* Update xml files, etc
* run the update: `python regression_tests.py -u 0X_category/category.cfg -t "my_test_name"
* clean out the resulting gold directory: `./clean_gold.sh 0X_category/my_test_name.regression.gold` to make sure that only the checkpoint files and the ats_version.txt files are left.
* commit and push

Note that any non-bitwise reproducible result should likely get updated.  It is extremely useful to be able to rely on bitwise reproducibility (when it is available).  So, if changes result in bitwise changes in the solution, prefer to first verify that the tests pass (bitwise deltas should still pass!) and only then update the tests using the above procedure.  This way, if someone else makes a change that shouldn't affect bitwise reproducibility, they can assume safely that they should have it. 

Obviously any changes that cause a test to fail should be checked extensively, confirmed that the change is acceptible (or better), and the document carefully in a commit message why the solution changed.


## Test Index:

Note that missing links mean the test does not yet exist.  Please feel free to help!

### [`01_richards_steadystate`](https://github.com/amanzi/ats-regression-tests/tree/master/01_richards_steadystate)

These tests solve Richards equation in steadystate form.

* [`fv`](https://github.com/amanzi/ats-regression-tests/blob/master/01_richards_steadystate/fv.xml) A 1D column using finite volumes.
* [`mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/01_richards_steadystate/mfd.xml) The same problem using mimetic finite differences.
* [`mfd-schur`](https://github.com/amanzi/ats-regression-tests/blob/master/01_richards_steadystate/mfd_schur.xml) The same problem using MFD and a Schur complement preconditioner.

### [`02_richards`](https://github.com/amanzi/ats-regression-tests/tree/master/02_richards)

Transient Richards equation tests.  In particular BCs, including seepage face BCs, cause trouble.

* [`infiltration_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/infiltration_fv_orig.xml) A 1D column infiltration problem, using finite volumes.
* [`infiltration_mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/infiltration_mfd_orig.xml) A 1D column infiltration problem using mimetic finite differences.
* [`seepage_infiltration_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_infiltration_fv_orig.xml) Infiltrate with a seepage face.
* [`seepage_infiltration_mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_infiltration_mfd_orig.xml) Same as above but with MFD.
* [`seepage_drawdown_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_drawdown_fv_orig.xml) A 1D column with a flux out the bottom.
* [`seepage_drawdown_mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_drawdown_mfd_orig.xml) Same as above but with MFD.
* [`seepage_drawdown_diag_tensor_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_drawdown_diag_tensor_fv_orig.xml) A 1D column with a flux out the bottom with a diagonal, non-isotropic tensor.
* [`seepage_drawdown_diag_tensor_mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_drawdown_diag_tensor_mfd_orig.xml) Same as above with MFD.
* [`seepage_drawdown_full_tensor_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_drawdown_full_tensor_fv_orig.xml) A 1D column with a flux out the bottom with a full tensor permeability.
* [`seepage_drawdown_full_tensor_mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_drawdown_full_tensor_mfd_orig.xml) Same as above with MFD.
* [`seepage_exfiltration_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_exfiltration_fv_orig.xml) A 1D column exfiltration problem, using finite volumes.
* [`seepage_exfiltration_mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/seepage_exfiltration_mfd_orig.xml) A 1D column exfiltration problem using mimetic finite differences.
* [`infiltration_then_seepage_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/infiltration_then_seepage_fv_orig.xml) A 1D column that infiltrates, then a seepage face turns on.
* [`infiltration_then_seepage_mfd`](https://github.com/amanzi/ats-regression-tests/blob/master/02_richards/infiltration_then_seepage_mfd_orig.xml) Same as above with MFD.

### [`03_surface_water`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water)

Solve some form of diffusion wave equation.  In particular BCs, including the plethora of outflow options, cause trouble.

* [`rainfall_fv`](https://github.com/amanzi/ats-regression-tests/blob/master/03_surface_water/rainfall_fv.xml) A simple rainfall problem, with finite volumes.
* [`rainfall_fv_jac`](https://github.com/amanzi/ats-regression-tests/blob/master/03_surface_water/rainfall_fv_jac.xml) The same problem, with Jacobian terms.
* [`rainfall_fv_simplified`](https://github.com/amanzi/ats-regression-tests/blob/master/03_surface_water/rainfall_fv_simplified.xml) The same problem, but with constant, non-temperature-based densities and viscosities.
* [`bc_critical_depth`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water/bc_critical_depth.xml) Tests the critical depth boundary condition with an injection problem.
* [`bc_max_head`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water/bc_max_head.xml) Tests the max head boundary condition with an injection problem.
* [`bc_zero_gradient`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water/bc_zero_gradient.xml) Tests the zero gradient boundary condition with an injection problem.
* [`uphill_head`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water/uphill_head.xml) Part of a series of problems dealing with transient BCs and flow causality causing difficulties in upwinding.
* [`uphill_piecewise_head`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water/uphill_piecewise_head.xml) Part of a series of problems dealing with transient BCs and flow causality causing difficulties in upwinding.
* [`downhill_head`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water/downhill_head.xml) Part of a series of problems dealing with transient BCs and flow causality causing difficulties in upwinding.
* [`downhill_piecewise_head`](https://github.com/amanzi/ats-regression-tests/tree/master/03_surface_water/downhill_piecewise_head.xml) Part of a series of problems dealing with transient BCs and flow causality causing difficulties in upwinding.
* `subgrid_microtopography` An example of the model for representing subgrid microtopography in surface flow.

### [`04_integrated_hydro`](https://github.com/amanzi/ats-regression-tests/tree/master/04_integrated_hydro)

Coupled flow on the surface and subsurface

* [`column_infiltration2`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/column_infiltration2_orig.xml) A 1D column, initially unsaturated, rained on.  Very similar to column_sat.  Second iteration of this test.
* [`column_exfiltration`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/column_exfiltration_orig.xml) A 1D column, initially unsaturated, with a flux in from the bottom until water expresses at the surface.
* [`column_drainage`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/column_drainage_orig.xml) A 1D column, initially saturated with surface water, with a flux out of the bottom until the surface is dry.
* [`column_sat`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/column_sat_orig.xml) A 1D column, saturation limited runoff generation.
* [`column_inf`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/column_inf_orig.xml) A 1D column, infiltration limited runoff generation.
* [`hillslope_sat`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/hillslope_sat_orig.xml) A 2D hillslope, saturation limited runoff generation.
* [`hillslope_inf`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/hillslope_inf_orig.xml) A 2D hillslope, infiltration limited runoff generation.
* [`hillslope_sat-np2`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/hillslope_sat-np2_orig.xml) A 2D hillslope, saturation limited runoff generation, on two cores.
* [`hillslope_inf-np2`](https://github.com/amanzi/ats-regression-tests/blob/master/04_integrated_hydro/hillslope_inf-np2_orig.xml) A 2D hillslope, infiltration limited runoff generation, on two cores.

### [`05_surface_balance`](https://github.com/amanzi/ats-regression-tests/tree/master/05_surface_balance)

Surface energy balance equations that somehow calculate evaporation or transpiration or both.

* [`general`](https://github.com/amanzi/ats-regression-tests/blob/master/05_surface_balance/general.xml) A very simple balance ODE, solving exponential decay, to test general surface balance PKs and time integration.
* [`lingzhang`](https://github.com/amanzi/ats-regression-tests/blob/master/05_surface_balance/lingzhang.xml) A simple test of the Ling & Zhang based surface energy balance model used in Arctic/Ecohydrology runs.
* [`priestly_taylor`](https://github.com/amanzi/ats-regression-tests/blob/master/05_surface_balance/priestly_taylor.xml) A simple test of the Priestly-Taylor potential ET model.
  
### [`06_transport`](https://github.com/amanzi/ats-regression-tests/tree/master/06_transport)

Surface and subsurface transport of nonreactive species.

* [`surface_tracer`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/surface_tracer.xml) A single tracer in a 1D reach
* `surface_tracer_logical` A single tracer on a logical mesh
* [`subsurface_tracer`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/subsurface_tracer.xml) A single tracer in a 2D transect.
* [`column_infiltration`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/column_infiltration.xml) Integrated transport on a single column of cells; an infiltration problem where the new water includes the tracer.
* [`column_exfiltration`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/column_exfiltration.xml) Integrated transport on a single column of cells; an exfiltration problem where water pushes up, making sure tracer ends up in the surface water.
* [`column_drainage`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/column_drainage.xml) Integrated transport on a single column of cells; a drainage problem where the water table draws down.
* [`column_infiltration_hot`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/column_infiltration_hot.xml) Same as above, but with a higher order transport discretization.
* [`column_exfiltration_hot`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/column_exfiltration_hot.xml) Same as above, but with a higher order transport discretization.
* [`column_drainage_hot`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/column_drainage_hot.xml) Same as above, but with a higher order transport discretization.

### [`07_reactive_transport`](https://github.com/amanzi/ats-regression-tests/tree/master/07_reactive_transport)

Surface and subsurface reactive transport

* [`surface_decay_ingrowth`](https://github.com/amanzi/ats-regression-tests/blob/master/07_reactive_transport/surface_decay_ingrowth.xml) A two-species system where the first species decays into the second (daughter) species.  A radioactive decay problem.
* `surface_decay_ingrowth_logical` The same problem on a logical mesh.
* `subsurface_decay_ingrowth` The same problem on a 2D transect.
* `integrated_decay_ingrowth` The same problem on surface + subsurface.
* `integrated_decay_ingrowth_coupled` The same integrated system but with a coupled flow solution.
* [`surface_denitrification`](https://github.com/amanzi/ats-regression-tests/blob/master/07_reactive_transport/surface_denitrification.xml) Dual-monod kinetics reaction system for aerobic respiration and DOM denitrification.  6 primary species and reactions.
* `surface_denitrification_logical` The same problem on a logical mesh.
* `subsurface_denitrification` The same problem on a 2D transect.
* `integrated_denitrification` The same problem on surface + subsurface.  
* `integrated_denitrification_coupled` The same integrated system but with a coupled flow solution.
* [`subsurface_sorption`](https://github.com/amanzi/ats-regression-tests/blob/master/07_reactive_transport/subsurface_sorption.xml) A single species subsurface transport with equilibrium sorption in a generated mesh
* [`subsurface_sorption_logical`](https://github.com/amanzi/ats-regression-tests/blob/master/07_reactive_transport/subsurface_sorption_logical.xml) Reactive transport (first order transformation taking place only in the aqueous phase) in subsurface where parent and daughter species have different sorption properties 
* [`dilution_test`](https://github.com/amanzi/ats-regression-tests/blob/master/07_reactive_transport/dilution_test.xml) A single tracer injection using "water_source" and geochemical condition (PFLOTRAN) to test units of effective solute injection rate 
* [`column_infiltration_alquimia_tracer`](https://github.com/amanzi/ats-regression-tests/blob/master/07_transport/column_infiltration_alquimia_tracer.xml) Integrated transport in a single column of cells; same infiltration problem as [`column_infiltration`](https://github.com/amanzi/ats-regression-tests/blob/master/06_transport/column_infiltration.xml) where the infiltrating water contains a tracer, the concentration of which is set in a pflotran input file, hence testing the alquimia-pflotran coupling as well as the surface-subsurface concentration coupling, and the geochemical source term for concentrations.
* [`column_infiltration_alquimia_crunch_tracer`](https://github.com/amanzi/ats-regression-tests/blob/master/07_transport/column_infiltration_alquimia_crunch_tracer.xml) Same as  [`column_infiltration_alquimia_tracer`](https://github.com/amanzi/ats-regression-tests/blob/master/07_transport/column_infiltration_alquimia_tracer.xml) but using CrunchFlow as geochemical engine. 
* [`column_infiltration_alquimia_calcite`](https://github.com/amanzi/ats-regression-tests/blob/master/07_transport/column_infiltration_alquimia_crunch_tracer.xml) Same as  [`column_infiltration_alquimia_crunch_tracer`](https://github.com/amanzi/ats-regression-tests/blob/master/07_transport/column_infiltration_alquimia_crunch_tracer.xml) but with a geochemical problem that involves calcite dissolution in the subsurface domain. So water infiltrates with rain water concentrations causing initial concentrations to decrease. However, calcite dissolution compensates in part for reactants. When infiltration stops, concentrations start to rebound. The geochemical uses CrunchFlow as engine. Tests mineral reaction capabilities.

### `08_energy`

A set of energy equations building toward freeze-thaw problems.

* [`surface_water`](https://github.com/amanzi/ats-regression-tests/blob/master/08_energy/surface_water.xml) A sheet of ice gets thawed on the surface.
* [`freezeup`](https://github.com/amanzi/ats-regression-tests/blob/master/08_energy/freezeup.xml) Freezes a column of water from below.
* [`permafrost`](https://github.com/amanzi/ats-regression-tests/blob/master/08_energy/permafrost.xml) A typical full permafrost problem.
* `snow_distribution` Some form of 2D snow distribution test.

### `09_multiscale_models`

A hodgepodge of subgrid models, including column-based 2.5D problems and more.

* [`columnar_permafrost`](https://github.com/amanzi/ats-regression-tests/blob/master/09_multiscale_models/columnar_permafrost.xml) Four-column example of 1D subsurface columns + 2D surface system on an energy+flow system.
* [`columnar_permafrost_subgrid`](https://github.com/amanzi/ats-regression-tests/blob/master/09_multiscale_models/columnar_permafrost_subgrid.xml) Four-column example of 1D subsruface columns + 2D subgrid surface system on an energy+flow system with seb subgrid (soil, water, ice) model.
* [`stream_hyporheic_conservative_tracer_reach`](https://github.com/amanzi/ats-regression-tests/blob/master/09_multiscale_models/stream_hyporheic_conservative_tracer_reach.xml) Single reach conservative tracer example of the ADELS model using Alquimia.
* [`stream_hyporheic_sorption`](https://github.com/amanzi/ats-regression-tests/blob/master/09_multiscale_models/stream_hyporheic_sorption.xml) Single reach tracer undergoing sorption in the sub-surface represented at subgrid level (ADELS model + Alquimia).
* [`stream_hyporheic_denitrification_reach`](https://github.com/amanzi/ats-regression-tests/blob/master/09_multiscale_models/stream_hyporheic_denitrification_reach.xml) Single reach denitrification example (ADELS model + Alquimia) with single-subgrid hyporheic zone.
* [`stream_hyporheic_denitrification_reach_multisubgrid`](https://github.com/amanzi/ats-regression-tests/blob/master/09_multiscale_models/stream_hyporheic_denitrification_reach_multisubgrid.xml) Single reach denitrification example (ADELS model + Alquimia) with multisubgrid hyporheic zones.
* [`stream_hyporheic_denitrification_watershed`](https://github.com/amanzi/ats-regression-tests/blob/master/09_multiscale_models/stream_hyporheic_denitrification_watershed.xml) Watershed scale denitrification example (ADELS model + Alquimia) with single-subgrid hyporheic zones.

