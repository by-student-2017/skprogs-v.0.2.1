*******
SkProgs
*******

Package containing a few programs that are useful in generating Slater-Koster
files for the DFTB-method.

**NOTE**: This packages comes with minimal documentation and with a currently
rather fragile user interface. It is considered to be neither stable nor
robust. Make sure, you check results as careful as possible. Use at your own
risk!


Installation
============

|build status|

Prerequisites
-------------

* Fortran 2003 compliant compiler

* CMake (>= 3.16)

* Python3 (>= 3.2)

* LAPACK/BLAS libraries (or compatible equivalents)

* libXC library with f03 interface (version >=6.0.0)


Obtaining via Conda
-------------------

The preferred way of obtaining SkProgs is to install it via the conda package
management framework using `Miniconda
<https://docs.conda.io/en/latest/miniconda.html>`_ or `Anaconda
<https://www.anaconda.com/products/individual>`_. Make sure to add/enable the
``conda-forge`` channel in order to be able to access SkProgs::

  conda config --add channels conda-forge
  conda config --set channel_priority strict

We recommend to set up a dedicated conda environment and to use the
`mamba solver <https://mamba.readthedocs.io/>`_ ::

  conda create --name skprogs
  conda activate skprogs
  conda install conda-libmamba-solver
  conda config --set solver libmamba

to install the latest stable release of SkProgs (Fortran and Python
components)::

  mamba install skprogs skprogs-python


Building from source
--------------------

Follow the usual CMake build workflow:

* Configure the project, specify your compilers (e.g. ``gfortran``),
  the install location (i.e. path stored in ``YOUR_SKPROGS_INSTALL_FOLDER``,
  e.g. ``$HOME/opt/skprogs``) and the build directory (e.g. ``_build``)::

    FC=gfortran cmake -DCMAKE_INSTALL_PREFIX=YOUR_SKPROGS_INSTALL_FOLDER -B _build .

  If libXC is installed in a non-standard location, you may need to specify
  either the ``CMAKE_PREFIX_PATH`` environment variable (if libXC was built with
  CMake) or the ``PKG_CONFIG_PATH`` environment variable (if libXC was built
  with autotools) in order to guide the library search::

    CMAKE_PREFIX_PATH=YOUR_LIBXC_INSTALL_FOLDER FC=gfortan cmake [...]

    PKG_CONFIG_PATH=FOLDER_WITH_LIBXC_PC_FILES FC=gfortran cmake [...]

* If the configuration was successful, build the code ::

    cmake --build _build -- -j

* After successful build, you should test the code by running ::

    pushd _build
    ctest -j
    popd

* If the tests were successful, install the package via ::

    cmake --install _build


Building libXC from source
--------------------------

Follow the usual CMake build workflow:

* Clone the official libXC repository and checkout the latest release tag, e.g.
  ``6.2.2``::

    git clone https://gitlab.com/libxc/libxc.git libxc
    cd libxc/
    git checkout 6.2.2

* Configure the project, specify your compilers (e.g. ``gfortran`` and ``gcc``),
  the install location (i.e. path stored in ``YOUR_LIBXC_INSTALL_FOLDER``, e.g.
  ``$HOME/opt/libxc``) and the build directory (e.g. ``_build``)::

      FC=gfortran CC=gcc cmake -DENABLE_FORTRAN=True -DCMAKE_INSTALL_PREFIX=YOUR_LIBXC_INSTALL_FOLDER -B _build .

* If the configuration was successful, build the code ::

    cmake --build _build -- -j

* After successful build, you should test the code by running ::

    pushd _build
    ctest -j
    popd

* If the tests were successful, install the package via ::

    cmake --install _build


Advanced build configuration
============================

Controlling the toolchain file selection
----------------------------------------

You can override the toolchain file, and select a different provided case,
passing the ``-DTOOLCHAIN`` option with the relevant name, e.g.::

  -DTOOLCHAIN=gnu

or ::

  -DTOOLCHAIN=intel

or by setting the toolchain name in the ``SKPROGS_TOOLCHAIN`` environment
variable. If you want to load an external toolchain file instead of one from the
source tree, you can specify the file path with the ``-DTOOLCHAIN_FILE`` option
::

  -DTOOLCHAIN_FILE=/path/to/myintel.cmake

or with the ``SKPROGS_TOOLCHAIN_FILE`` environment variable.

Similarly, you can also use an alternative build config file instead of
`config.cmake` in the source tree by specifying it with the
``-DBUILD_CONFIG_FILE`` option or by defining the ``SKPROGS_BUILD_CONFIG_FILE``
environment variable.


Generating SK-files
===================

The basic steps of generating the electronic part of the SK-tables are as
follows:

* If you have build SkProgs from source, initialize the necessary environment
  variables by sourceing the ``skprogs-activate.sh`` script (provided you have
  BASH or a compatible shell, otherwise inspect the script and set up the
  environment variables manually)::

    source <SKPROGS_INSTALL_FOLDER>/bin/skprogs-activate.sh

* Then create a file ``skdef.hsd`` containing the definitions for the elements
  and element pairs you wish to create. See the ``examples/`` folder for some
  examples.

* Run the ``skgen`` script to create the SK-tables. For example, in order to
  generate the electronic part of the SK-tables for C, H and O with dummy (zero)
  repulsives added, issue ::

    skgen -o slateratom -t sktwocnt sktable -d C,H,O C,H,O

  The SK-files will be created in the current folder. See the help (e.g. ``skgen
  -h``) for additional options.

Further documentation will be presented in a separate document later.


License
=======

SkProgs is released under the GNU Lesser General Public License.

You can redistribute it and/or modify it under the terms of the GNU Lesser
General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version. See the files
`COPYING <COPYING>`_ and `COPYING.LESSER <COPYING.LESSER>`_ for the detailed
licensing conditions.


.. |build status| image:: https://img.shields.io/github/actions/workflow/status/dftbplus/skprogs/build.yml
    :target: https://github.com/dftbplus/skprogs/actions/


Reference
=======
- [1] [DFTB Parameters for the Periodic Table: Part 1, Electronic Structure](https://pubs.acs.org/doi/10.1021/ct4004959)
- [2] [Self-Consistent-Charge Density-Functional Tight-Binding Parameters for Modeling an All-Solid-State Lithium Battery](https://doi.org/10.1021/acs.jctc.2c01115)


Note 1 (Importance of basis functions)
=======
- As pointed out in literature [1], basis functions are important (especially in the s-band). [1]
- Hence, to reproduce the KS matrix elements with Slater-type orbitals, special basis sets would need to be constructed to handle steep confinement potentials. [1]
- In "STO-nG" used in Gaussian etc., s and p orbitals are treated as SP. Therefore, here again, s and p are fitted using parameters other than Hubbard as SP.
- First, we will use the already known reference value for the "slateratom" parameter. The parameter of the reference atom is multiplied by "fitting atomic number/reference atomic number" to obtain the initial value of the search for the parameter of the fitting atom.
- Although the conditions are different from paper [1], good r0 results are obtained for "QUASINANO". There is a similar trend for simga parameters. When increasing simga from 2.0, the s-band approaches the DFT result.


Future plans
=======
- Create training data with QE. This is because the accuracy of QE is sufficiently guaranteed by the delta-factor. This was because I didn't have the budget, and although I contacted the developer, I was unable to purchase VASP for academic purposes. In my environment, I would not create training data with VASP.


My Wish
=======
- I strongly hope that parameter files will be prepared for almost all elements and their combinations free of charge.
- With Hotcent, I was not able to set the parameters satisfactorily due to my lack of skill. I hope that the parameters will be better organized in skprog-v.0.2.
- Ultimately, it is necessary to improve the repulsive force, but it is important to maintain the electronic structure in the optimal structure for almost all elements. In order to develop parameters that can be used free of charge, we sincerely hope for the cooperation of many people in terms of paper reports and financial support.


Acknowledgment (For examples)
=======
- This project (modified version) is/was partially supported by the following :
- meguREnergy Co., Ltd.
- ATSUMITEC Co., Ltd.
- RIKEN
- Without the support of "meguREnergy Co., Ltd." and "ATSUMITEC Co., Ltd.", I would not have been able to develop the examples to the level shown on this github. I would like to express my sincere gratitude. 


PC specs used for test
=======
+ OS: Microsoft Windows 11 Home 64 bit
+ BIOS: 1.14.0
+ CPU： 12th Gen Intel(R) Core(TM) i7-12700
+ Base Board：0R6PCT (A01)
+ Memory：32 GB
+ GPU: NVIDIA GeForce RTX3070
+ WSL2: VERSION="22.04.1 LTS (Jammy Jellyfish)"
+ [Quantum Espresso ver.7.2](https://www.quantum-espresso.org/release-notes/release-notes-QE7-2.html)
+ [PSLibrary 1.0.0](https://dalcorso.github.io/pslibrary/)
+ [DFTB+ ver.23.1](https://dftbplus.org/download/dftb-stable)
+ Python 3.10.12
+ Please, see "Installation_note_WSL2.txt"

