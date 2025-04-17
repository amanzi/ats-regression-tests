Amanzi Benchmark Tests
----------------------

The amanzi_benchmark-\* tests are from Amanzi's user guide tests, in `$AMANZI_SRC_DIR/test_suites/benchmarking/chemistry`.

These can be run in the ATS regression suite, then compared to output from PFLOTRAN, Crunch, and Amanzi.

To do so:

1. Build ATS and run ats-regression-tests:
   ```
   cd $ATS_SRC_DIR/testing/ats-regression-tests
   python regression_tests.py 07_reactive_transport -t amanzi_benchmark-*
   ```

2. Build Amanzi, setting `AMANZI_INSTALL_DIR` and set variables for this installation:

   ```
   export AMANZI_INSTALL_DIR=PATH_TO_AMANZI_DIR
   export PYTHONPATH=${AMANZI_SRC_DIR}/tools/utils:${AMANZI_SRC_DIR}/tools/testing:${PYTHONPATH}
   ```

3. Run the Amanzi script -- this runs Amanzi for a bunch of different test variations, and makes a plot

   ```
   cd $AMANZI_SRC_DIR/test_suites/benchmarking/chemistry/TEST_NAME
   python TEST_NAME_1d.py
   open TEST_NAME_1d.png
   ```


If all goes as planned, this should generate an image that includes
lines for each of Crunch, PFloTran, multiple configurations of Amanzi,
and ATS.


Note that most tests result in a slightly sharper interface for ATS
than for Amanzi, and significantly sharper than PFLoTran or Crunch.
The latter is because ATS and Amanzi use second order methods.  I'm
not entirely sure why ATS is sharper than Amanzi -- there are two
plausible candidates:

- Amanzi uses a 2nd order time integration scheme, whereas ATS uses
  forward Euler
- Amanzi includes a "Dispersion Solver" even in cases where the
  diffusivity is 0 and no dispersion is prescribed.  I wonder if
  Amanzi enforces a minimal diffusivity?  ATS does not, so there is no
  diffusion solve, and no non-numerical diffusion included.
