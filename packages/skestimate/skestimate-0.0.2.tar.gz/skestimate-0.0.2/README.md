**Package_VEnv-311:** 

## How to publish the package:

A repository named EstimatorPkg is created on github and cloned locally. We put the meta data in the top level of this repo and create a package named skestimate as a subdirectory. This package is going to be published on test pypi. During development importing the package is done in the virtual environment to ensure consistency.

`(EstimatorPkg) EstimatorPkg%> python`
```
>>> import skestimate	# executes __init__.py inside skestimate. Import also creates a sub namespace for skestimate which can be viewed by dir(skestimate). We can have sub packages in the package by creating a subdirectory containing ann__init__.py file. 
```

### Here are the steps to follow:

1. Create the repo EstimatorPkg in the github with readme, git ignore for python and MIT license
2. Clone the repo onto the local machine. `repos%> git clone https://github.com/skhabiri/EstimatorPkg.git`
3. Use `pyenv install 3.7` to install a specific python version for the package
4. Create a virtual env for the project EstimatePkg. `EstimatorPkg %> pipenv --python 3.7`
   1. Now a virtual environment including a Pipfile has been created. Pipfile can be edited manually too. We install all the required packages inside an activated virtualenv to update the environment with all the requirements through Pipfile, and Pipfile.lock.
5. Activate the virtual env. `EstimatorPkg%> pipenv shell`
   1.  `(EstimatorPkg) EstimatorPkg%> which python`        # points to the location of a specified version of python used in virtual env
6. Install the required packages in the virtual env. `(EstimatorPkg) EstimatorPkg%> pipenv install numpy pandas scikit-learn matplotlib`
7. Create the package directory and __init__.py file. `(EstimatorPkg) skestimate%> touch __init__.py `
8. Code the python modules or subpackages as needed. (fit_est.py)
9. To test the package locally:
   1. `EstimatorPkg) EstimatorPkg%> python`        # launch CLI python repl
   2. `import skestimate`        # import the package
   3. `est = skestimate.example()`        #load cover_type dataset and create an instance of Xest
   4. est.xscore(fit=True)        # test any method of the class
10.  Add twine to the dev packages for uploading the package onto the pypi `(EstimatorPkg) skestimate%> pipenv install -d twine`
11. Create a setup.py and (build)[python setup.py sdist bdist_wheel] the actual package.
    1. The instruction for pypi is in setup.py as a meta file located at project directory (EstimatePkg). setup.py uses setuptools.setup() to define the package.
    2. Note that package names in pypi require an underscore to be changed to dashe as a pypi convention. 
12. `(EstimatorPkg) EstimatorPkg%> python setup.py sdist bdist_wheel`        # builds the package based on the setup file. The binary is specific to an OS. Now we should have dist and build directories and skestimate.egg-info, next to the package directory.
13. If not yet, register for a [test pypi account](https://test.pypi.org/account/register/)
14. Upload the package to the test pypi using `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
    1. #upload the content of the dist/ into test.pypi.org
    2. `twine upload dist/*` for pypi.org
15. Start a Colab notebook, and install the package, `!pip install --index-url https://test.pypi.org/simple/ your_package`
16. Import the package in the notebook, and try it out!
