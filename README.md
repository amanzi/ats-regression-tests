ATS Regression Test Suite
==============================

This is the regression test suite for ATS.

The full set of these runs should always work, and should always be run and, if necessary, updated prior to issuing a pull request.


Quickstart
------------

To run a quick set of the tests that run fairly quickly, but should
not be considered complete, run:

```
python regression_tests.py --suite=standard .
```

To run the complete set of tests:

```
python regression_tests.py .
```

See also:
```
python regression_tests.py --help
```


Creating new tests
------------------

**Follow the naming convention:**  `test_category-test_name` where `test_category` is the subdirectory name.

* Add the xml file to the repo.
* Add the xml to a .cfg file in that subdirectory.
* Make sure that checkpoints are being written at sane times, and add "checkpoint=True" to xml files on evaluators whose results you wish to compare.
* Run the test.  
   * If the test is sensitive to timestep size history (e.g. it is a variable timestep history problem) then use the strategy: `python regression_tests.py -n  --save-dt-history path_to.cfg -t my_category-my_name`. This runs your test twice -- once to get a sane timestep size history, then parses that, saves it to disk, writes a new input file that uses that exact sequence of step sizes, and runs a second time ensure that the results work with that timestep size history.  This is a huge help for reproducibility and removing false negatives -- the solution can be quite sensitive to timestep size history, but rarely do we want to flag when a non-bitwise repeatable change randomly causes a solver to take one more timestep, thereby changing the answer.
   * If the test can be a fixed timestep size run, then just `python regression_tests.py -n path_to.cfg -t my_category-my_name` is sufficient.
   * Finally, after you've added the test, run once more to ensure that tolerances are good and the tests pass with what should be a bitwise identical run.
* Clean out the resulting gold directory: `./clean_gold.sh XX_my_category/my_category-my_name.regression.gold` to make sure that only the checkpoint files and the ats_version.txt files are left.
* Commit and push.


Updating tests:
---------------
* Update xml files, etc
* run the update: `python regression_tests.py -u path_to.cfg -t "my_category-my_name"
* clean out the resulting gold directory: `./clean_gold.sh XX_my_category/my_category-my_name.regression.gold` to make sure that only the checkpoint files and the ats_version.txt files are left.
* commit and push

Note that any non-bitwise reproducible result should likely get updated.  It is extremely useful to be able to rely on bitwise reproducibility (when it is available).  So, if changes result in bitwise changes in the solution, prefer to first verify that the tests pass (bitwise deltas should still pass!) and only then update the tests using the above procedure.  This way, if someone else makes a change that shouldn't affect bitwise reproducibility, they can assume safely that they should have it. 

Obviously any changes that cause a test to fail should be checked extensively, confirmed that the change is acceptible (or better), and the document carefully in a commit message why the solution changed.


Test Index:
-----------

Note that missing links mean the test does not yet exist.  Please feel free to help!

* `01_richards_steadystate`. These tests solve Richards equation in steadystate form.
* `02_richards` Transient Richards equation tests
* `03_surface_water` Solve some form of diffusion wave equation under assorted DEMs and boundary conditions.
* `04_integrated_hydro` Coupled flow on the surface and subsurface
* `05_surface_balance` Surface energy balance equations that somehow calculate evaporation or transpiration or both.
* `06_transport`  Surface and subsurface transport of nonreactive species.
  * `surface_tracer` A single tracer in a 1D reach
  * **`surface_tracer_logical` A single tracer on a logical mesh**
  * **`subsurface_tracer` A single tracer in a 2D transect domain**
  * **`integrated_tracer` An integrated surface and subsurface transport problem.**
  * **`integrated_tracer_coupled` The same integrated system but with a coupled flow solution.**
* `07_reactive_transport` Surface and subsurface reactive transport
  * `surface_decay_ingrowth` A two-specie system where the first specie decays into the second (daughter) specie.  A radioactive decay problem.
  * **`surface_decay_ingrowth_logical` The same problem on a logical mesh.**
  * **`subsurface_decay_ingrowth` The same problem on a 2D transect.**
  * **`integrated_decay_ingrowth` The same problem on surface + subsurface.**
  * **`integrated_decay_ingrowth_coupled` The same integrated system but with a coupled flow solution.**
  * `surface_denitrification` Dual-monod kinetics reaction system for aerobic respiration and DOM denitrification.  6 primary species and reactions.
  * **`surface_denitrification_logical` The same problem on a logical mesh.**
  * **`subsurface_denitrification` The same problem on a 2D transect.**
  * **`integrated_denitrification` The same problem on surface + subsurface.**  
  * **`integrated_denitrification_coupled` The same integrated system but with a coupled flow solution.**
* `08_energy`
  * **`advection` A simple surface-based advection-dominated problem.**
  * **`diffusion` A simple subsurface-based diffusion-dominated problem.**
  * **`permafrost` Some form of columnar permafrost test?** 
  * **`snow_distribution` Some form of 2D snow distribution test.**
* `09_subgrid_models`
  * **`columnar_permafrost` Four-column example of the 1D + 2D surface star system on an energy+flow system.**
  * **`columnar_permafrost_subcycled` Four-column example of the 1D + 2D surface star system on an energy+flow system with subcycling of columns**
  * **`hyporheic_exchange` Single reach example of the ADELS model.**

