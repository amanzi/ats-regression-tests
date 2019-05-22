ATS Regression Test Suite
==============================

This is the regression test suite for ATS.

The full set of these runs should always work, and should always be run and, if necessary, updated prior to issuing a pull request.

TODO: Update these to fix timestep sizes to ensure easier comparability despite divergence of nonlinear iterates.


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

* add the xml file to the repo
* add the xml to a .cfg file in that subdirectory
* make sure that checkpoints are being written at sane times, and add "checkpoint=True" to xml files on evaluators whose results you wish to compare.
* run the test: `python regression_tests.py -n path_to.cfg -t "my_category-my_name"
* clean out the resulting gold directory: `./clean_gold.sh XX_my_category/my_category-my_name.regression.gold` to make sure that only the checkpoint files and the ats_version.txt files are left.
* commit and push


Updating tests:
---------------------
* update xml files, etc
* run the update: `python regression_tests.py -u path_to.cfg -t "my_category-my_name"
* clean out the resulting gold directory: `./clean_gold.sh XX_my_category/my_category-my_name.regression.gold` to make sure that only the checkpoint files and the ats_version.txt files are left.
* commit and push

