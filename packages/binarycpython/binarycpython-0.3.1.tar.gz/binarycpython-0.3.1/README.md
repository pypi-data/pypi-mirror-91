# Python module for binary_c
Coverage: ![alt text](coverage.svg)
Based on a original work by Jeff Andrews (can be found in old_solution/ directory)
updated and extended for Python3 by Robert Izzard, David hendriks

Warning : THIS CODE IS EXPERIMENTAL!

r.izzard@surrey.ac.uk
http://personal.ph.surrey.ac.uk/~ri0005/binary_c.html
09/06/2019

Requirements
---------------------
- Python3
- binary_c version 2.1+
- requirements.txt (no?)

Environment variables
---------------------
Before compilation you should set the following environment variables:

- required: `BINARY_C` should point to the root directory of your binary_c installation
- recommended: `LD_LIBRARY_PATH` should include $BINARY_C/src and whatever directories are required to run binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)
- recommended: `LIBRARY_PATH` should include whatever directories are required to build binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)

Build instructions
---------------------
To build the module, make sure you have built binary_c (with `make` in the binary_c root directory), its shared library (with `make libbinary_c.so` in the binary_c root directory), and set environment variables as described above, then run the following code in t:
```
make clean
make
```
Then to test the Python module:
```
python3 ./python_API_test.py
```
You will require whatever libraries with which binary_c was compiled, as well as the compiler with which Python was built (usually gcc, which is easily installed on most systems).

If you want to be able to import the binary_c module correctly for child directories (or anywhere for that matter), execute or put the following code in your .bashrc/.zshrc: 
```
export LD_LIBRARY_PATH=<full path to root dir of repo>:$LD_LIBRARY_PATH
export PYTHONPATH=<full path to root dir of repo>:$PYTHONPATH
```

Usage notes
---------------------
When running a jupyter notebook and importing binary_c, it might happen that the module binary_c cannot be found. I experienced this when I executed Jupyter Notebook from a virtual environment which didnt use the same python (version/binary/shim) as the one I built this library with. Make sure jupyter does use the same underlying python version/binary/shim. That resolved the issue for me.

Also: I figured that having binaryc output the log like "<LOG HEADER> t=10e4 ..." (i.e. printing the parameter names as well as their values) would be useful because in that way one can easily have python read that out automatically instead of having to manually copy the list of parameter names.

See examples/ dir for some working examples

When you try to `import binary_c_python_api` and python complains about it not existing, but you are sure that you correctly included the necessary pythonpaths, then you probably need to rebuild the package.

FAQ:
--------------------

Building issues with binary_c itself: 
- see the documentation of binary_c (in doc/). 
- If you have MESA installed, make sure that the `$MESASDK_ROOT/bin/mesasdk_init.sh` is not sourced. It comes with its own version of some programs, and those can interfere with installing.  

Pip install failed:
- Run the installation with `-v` and/or `--log <logfile>` to get some more info
- If gcc throws errors like `gcc: error: unrecognized command line option ‘-ftz’; did you mean ‘-flto’?`, this might be due to that the python on that system was built with a different compiler. It then passes the python3.6-config --cflags to the binarycpython installation, which, if done with gcc, will not work. Try a different python3.6. I suggest using `pyenv` to manage python versions. If installing a version of python with pyenv is not possible, then try to use a python version that is avaible to the machine that is built with the same compiler as binary_c was built with. 

if pip installation results in `No files/directories in /tmp/pip-1ckzg0p9-build/pip-egg-info (from PKG-INFO)`, try running it verbose (`-v`) to see what is actually going wrong. 
