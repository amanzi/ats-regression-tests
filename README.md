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


New tests
--------------

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
---------------------
* Update xml files, etc
* run the update: `python regression_tests.py -u path_to.cfg -t "my_category-my_name"
* clean out the resulting gold directory: `./clean_gold.sh XX_my_category/my_category-my_name.regression.gold` to make sure that only the checkpoint files and the ats_version.txt files are left.
* commit and push

Note that any non-bitwise reproducible result should likely get updated.  It is extremely useful to be able to rely on bitwise reproducibility (when it is available).  So, if changes result in bitwise changes in the solution, prefer to first verify that the tests pass (bitwise deltas should still pass!) and only then update the tests using the above procedure.  This way, if someone else makes a change that shouldn't affect bitwise reproducibility, they can assume safely that they should have it. 

Obviously any changes that cause a test to fail should be checked extensively, confirmed that the change is acceptible (or better), and the document carefully in a commit message why the solution changed.

