[![pipeline status](https://git.ligo.org/gwinc/pygwinc/badges/master/pipeline.svg)](https://git.ligo.org/gwinc/pygwinc/commits/master)

# Python Gravitational Wave Interferometer Noise Calculator

[![aLIGO](https://gwinc.docs.ligo.org/pygwinc/ifo/aLIGO.png "Canonical
IFOs")](IFO.md)

`pygwinc` is a multi-faceted tool for processing and plotting noise
budgets for ground-based gravitational wave detectors.  It's primary
feature is a collection of mostly analytic [noise calculation
functions](#noise-functions) for various sources of noise affecting
detectors (`gwinc.noise`):

* quantum noise
* mirror coating thermal noise
* mirror substrate thermal noise
* suspension fiber thermal noise
* seismic noise
* Newtonian/gravity-gradient noise
* residual gas noise

`pygwinc` is also a generalized noise budgeting tool (`gwinc.nb`) that
allows users to create arbitrary noise budgets (for any experiment,
not just ground-based GW detectors) using measured or analytically
calculated data.  See the [budget interface](#Budget-interface)
section below.

`pygwinc` includes canonical budgets for various well-known current
and future GW detectors (`gwinc.ifo`):

* [aLIGO](https://gwinc.docs.ligo.org/pygwinc/ifo/aLIGO.png)
* [A+](https://gwinc.docs.ligo.org/pygwinc/ifo/Aplus.png)
* [Voyager](https://gwinc.docs.ligo.org/pygwinc/ifo/Voyager.png)
* [Cosmic Explorer 1](https://gwinc.docs.ligo.org/pygwinc/ifo/CE1.png)
* [Cosmic Explorer 2 (Silica)](https://gwinc.docs.ligo.org/pygwinc/ifo/CE2silica.png)
* [Cosmic Explorer 2 (Silicon)](https://gwinc.docs.ligo.org/pygwinc/ifo/CE2silicon.png)

See [IFO.md](IFO.md) for the latest CI-generated plots and hdf5 cached
data.

The [`inspiral_range`](https://git.ligo.org/gwinc/inspiral-range)
package can be used to calculate various common "inspiral range"
figures of merit for gravitational wave detector budgets.  See the
[inspiral range](#inspiral-range) section below.


## usage

### command line interface

`pygwinc` provides a command line interface that can be used to
calculate and plot the various canonical IFO noise budgets described
above:
```shell
$ python3 -m gwinc aLIGO
```
Or [Custom budgets](#budget-interface) may also be processed by providing
the path to the budget module/package:
```shell
$ python3 -m gwinc path/to/mybudget
```

Budget plots can be saved in various formats (.png, .svg, .pdf):
```shell
$ python3 -m gwinc --save aLIGO.png aLIGO
```
Or trace data can be saved to an
[HDF5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) file:
```shell
$ python3 -m gwinc --save aLIGO.hdf5 aLIGO
```
Trace HDF5 files can also be plotted directly:
```shell
$ python3 -m gwinc aLIGO.hdf5
```

IFO parameters can be manipulated from the command line with the
`--ifo` option:
```shell
$ python3 -m gwinc aLIGO --ifo Optics.SRM.Tunephase=3.14
```
You can also dump the IFO parameters to a [YAML-formatted parameter
file](#yaml-parameter-files):
```shell
$ python3 -m gwinc --yaml aLIGO > my_aLIGO.yaml
$ edit my_aLIGO.yaml
$ python3 -m gwinc -d my_aLIGO.yaml aLIGO
                             aLIGO    my_aLIGO.yaml
Materials.Coating.Philown    5e-05            3e-05
$ python3 -m gwinc my_aLIGO.yaml
```
Stand-alone YAML files assume the nominal ['aLIGO' budget
description](gwinc/ifo/aLIGO).

The command line interface also includes an "interactive" mode which
provides an [IPython](https://ipython.org/) shell for interacting with
a processed budget:
```shell
$ python3 -m gwinc -i Aplus
GWINC interactive shell

The 'ifo' Struct and 'trace' data are available for inspection.
Use the 'whos' command to view the workspace.

You may interact with the plot using the 'plt' functions, e.g.:

In [.]: plt.title("My Special Budget")
In [.]: plt.savefig("mybudget.pdf")

In [1]: 
```

See command help for more info:
```shell
$ python3 -m gwinc -h
```


### library interface

For custom plotting, parameter optimization, etc. all functionality can be
accessed directly through the `gwinc` library interface:
```python
>>> import gwinc
>>> budget = gwinc.load_budget('aLIGO')
>>> trace = budget.run()
>>> fig = trace.plot()
>>> fig.show()
```
A default frequency array is used, but alternative frequencies can be
provided to `load_budget()` either in the form of a numpy array:
```python
>>> import numpy as np
>>> freq = np.logspace(1, 3, 1000)
>>> budget = gwinc.load_budget('aLIGO', freq=freq)
```
or frequency specification string ('FLO:[NPOINTS:]FHI'):
```
>>> budget = gwinc.load_budget('aLIGO', freq='10:1000:1000')
```

The `load_budget()` function takes most of the same inputs as the
command line interface (e.g. IFO names, budget module paths, YAML
parameter files), and returns the instantiated `Budget` object defined
in the specified budget module (see [budget
interface](#budget-interface) below).  The budget `ifo` `gwinc.Struct`
is available in the `budget.ifo` attribute.

The budget `run()` method calculates all budget noises and the noise
total and returns a `BudgetTrace` object with `freq`, `psd`, and `asd`
properties.  The budget sub-traces are available through a dictionary
(`trace['QuantumVacuum']`) interface and via attributes
(`trace.QuantumVacumm`).

The budget `freq` and `ifo` attributes can be updated at run time by
passing them as keyword arguments to the `run()` method:
```python
>>> budget = load_budget('aLIGO')
>>> freq = np.logspace(1, 3, 1000)
>>> ifo = Struct.from_file('/path/to/ifo_alt.yaml')
>>> trace = budget.run(freq=freq, ifo=ifo)
```


## noise functions

The `pygwinc` analytical noise functions are available in the
`gwinc.noise` package.  This package includes multiple sub-modules for
the different types of noises, e.g. `suspensionthermal`,
`coatingthermal`, `quantum`, etc.)

The various noise functions need many different parameters to
calculate their noise outputs.  Many parameters are expected to be in
the form of object attributes of a class-like container that is passed
to the calculation function.  The pygwinc
[`Struct`](#gwinc.Struct-objects) object is designed to hold such
parameters.

For instance, the `coating_brownian` function expects a `materials`
structure as input argument, that holds the various mirror materials
parameters (e.g. `materials.Substrate.MirrorY`):
```python
def coating_brownian(f, materials, wavelength, wBeam, dOpt):
    ...
    # extract substructures
    sub = materials.Substrate
    ...
    # substrate properties
    Ysub = sub.MirrorY
```


## `gwinc.Struct` objects

`pygwinc` provides a `Struct` class that can hold parameters in
attributes and additionally acts like a dictionary, for passing to the
noise calculation functions.  `Struct`s can be created from
dictionaries, or loaded from various file formats (see below).


### YAML parameter files

The easiest way to store all budget parameters is in a YAML file.
YAML files can be loaded directly into `gwinc.Struct` objects via
the `Struct.from_file()` class method:
```python
from gwinc import Struct
ifo = Struct.from_file('/path/to/ifo.yaml')
```

YAML parameter files can also be given to the `load_budget()` function
as described above, in which case the base 'aLIGO' budget structure
will be assumed and returned, with the YAML Struct inserted in the
`Budget.ifo` class attribute.

Here are the included ifo.yaml files for all the canonical IFOs:

* [aLIGO.yaml](gwinc/ifo/aLIGO/ifo.yaml)
* [Aplus.yaml](gwinc/ifo/Aplus/ifo.yaml)
* [Voyager.yaml](gwinc/ifo/Voyager/ifo.yaml)
* [CE1.yaml](gwinc/ifo/CE1/ifo.yaml)
* [CE2.yaml](gwinc/ifo/CE2/ifo.yaml)

The `Struct.from_file()` class method can also load MATLAB structs
defined in .mat files, for compatibility with
[matgwinc](https://git.ligo.org/gwinc/matgwinc), and MATLAB .m files,
although the later requires the use of the [python MATLAB
engine](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html).


## budget interface

`pygwinc` provides a generic noise budget interface, `gwinc.nb`, that
can be used to define custom noise budgets (it also underlies the
"canonical" budgets included in `gwinc.ifo`).  Budgets are defined in
a "budget module" which includes `BudgetItem` definitions.

### BudgetItem classes

The `gwinc.nb` package provides three `BudgetItem` classes that can be
inherited to define the various components of a budget:

* `nb.Noise`: a noise source
* `nb.Calibration`: a noise calibration
* `nb.Budget`: a group of noises

The primary action of a `BudgetItem` happens in it's `calc()` method.
For `Noise` classes, the `calc` method should return the noise PSD at
the specified frequency points.  For the `Calibration` class, `calc`
should return a frequency response.  `Budget` classes should not have
a special `calc` method defined as they already know how to calculate
the overall noise from their constituent noises and calibrations.

Additionally `BudgetItem`s have two other methods, `load` and
`update`, that can be overridden by the user to handle arbitrary data
processing.  These are useful for creating budgets from "live" dynamic
noise measurements and the like.  The three core methods therefore
are:

* `load()`: initial loading of static data
* `update(**kwargs)`: update data/attributes
* `calc()`: return final data array

Generally these methods are not called directly.  Instead, the `Noise`
and `Budget` classes include a `run` method that smartly executes them
in sequence and returns a `BudgetTrace` object for the budget.

See the built-in `BudgetItem` documentation for more info
(e.g. `pydoc3 gwinc.nb.BudgetItem`)


### budget module definition

A budget module is a standard python module (single `.py` file) or
package (directory containing `__inti__.py` file) containing
`BudgetItem` definitions describing the various noises and
calibrations of a budget, as well as the overall budget calculation
itself.  Each budget module should include one `nb.Budget` class
definition named after the module name.

Here's an example of a budget module named `MyBudget`.  It defines two
`Noise` classes and one `Calibration` class, as well as the overall
`Budget` class (name `MyBudget` that puts them all together):
```shell
$ find MyBudget
MyBudget/
MyBudget/__init__.py
MyBudget/ifo.yaml
$
```

```python
# MyBudget/__init__.py

import numpy as np
from gwinc import nb
from gwinc import noise


class SuspensionThermal(nb.Noise):
    """Suspension thermal noise"""
    style = dict(
        label='Suspension Thermal',
        color='#ad900d',
        linestyle='--',
    )

    def calc(self):
        n = noise.suspensionthermal.suspension_thermal(
            self.freq, self.ifo.Suspension)
        return 2 * n


class MeasuredNoise(nb.Noise):
    style = dict(
        label='Measured Noise',
        color='#838209',
        linestyle='-',
    )

    def load(self):
        psd, freq = np.loadtxt('/path/to/measured/psd.txt')
        self.data = self.interpolate(freq, psd)

    def calc(self):
        return self.data


class MyCalibration(nb.Calibration):
    def calc(self):
        return np.ones_like(self.freq) * 1234


class MyBudget(nb.Budget):
    noises = [
        SuspensionThermal,
        MeasuredNoise,
    ]
    
    calibrations = [
        MyCalibration,
    ]
```

The `style` attributes of the various `Noise` classes define plot
style for the noise.

This budget can be loaded with the `gwinc.load_budget()` function, and
processed as usual with the `Budget.run()` method:
```python
budget = load_budget('/path/to/MyBudget', freq)
trace = budget.run()
```

Other than the necessary `freq` initialization argument that defines
the frequency array, any additional keyword arguments are assigned as
class attributes to the budget object, and to all of it's constituent
sub noises/calibrations/budgets.

Note that the `SuspensionThermal` Noise class above uses the
`suspension_thermal` analytic noise calculation function, which takes
a "suspension" Struct as input argument.  In this case, this
suspension Struct is extracted from the `self.ifo` Struct at
`self.ifo.Suspension`.

If a budget module defined as a package includes an `ifo.yaml`
[parameter file](#parameter-files) in the package directory, the
`load_budget()` function will automatically load the YAML data into an
`ifo` `gwinc.Struct` and assign it to the `budget.ifo` attribute.

The IFOs included in `gwinc.ifo` provide examples of the use of the
budget interface (e.g. [gwinc.ifo.aLIGO](gwinc/ifo/aLIGO)).


### the "precomp" decorator

The `BudgetItem` supports "precomp" functions that can be used to
calculate common derived values needed in multiple `BudgetItems`.
They are specified using the `nb.precomp` decorator applied to the
`BudgetItem.calc()` method.  These functions are executed during the
`update()` method call, supplied with the budget `freq` and `ifo`
attributes as input arguments, and are expected to update the `ifo`
struct.  The execution state of the precomp functions is cached at the
Budget level, to prevent needlessly re-calculating them multiple
times.  For example:
```python
from gwinc import nb


def precomp_foo(freq, ifo):
    pc = Struct()
    ...
    return pc


def precomp_bar(freq, ifo):
    pc = Struct()
    ...
    return pc


class Noise0(nb.Noise):
    @nb.precomp(foo=precomp_foo)
    def calc(self, foo):
        ...

class Noise1(nb.Noise):
    @nb.precomp(foo=precomp_foo)
    @nb.precomp(bar=precomp_bar)
    def calc(self, foo, bar):
        ...

class MyBudget(nb.Budget):
    noises = [
        Noise0,
        Noise1,
    ]
```
When `MyBudget.run()` is called, all the `precomp` functions will be
executed, e.g.:
```python
precomp_foo(self.freq, self.ifo)
precomp_bar(self.freq, self.ifo)
```
But the `precomp_foo` function will only be calculated once even
though it's specified as needed by both `Noise0` and `Noise1`.


### extracting single noise terms

There are various way to extract single noise terms from the Budget
interface.  The most straightforward way is to run the full budget,
and extract the noise data the output traces dictionary:

```python
budget = load_budget('/path/to/MyBudget', freq)
trace = budget.run()
quantum_trace = trace['QuantumVacuum']
```

You can also calculate the final calibrated output noise for just a
single term using the Budget `calc_noise()` method:
```python
data = budget.calc_noise('QuantumVacuum')
```

You can also calculate a noise at it's source, without applying any
calibrations, by using the Budget `__getitem__` interface to extract
the specific Noise BudgetItem for the noise you're interested in, and
running it's `calc()` method directly:
```python
data = budget['QuantumVacuum'].calc()
```


# inspiral range

The [`inspiral_range`](https://git.ligo.org/gwinc/inspiral-range)
package can be used to calculate various common "inspiral range"
figures of merit for gravitational wave detector budgets.  Here's an
example of how to use it to calculate the inspiral range of the
baseline 'Aplus' detector:
```python
import gwinc
import inspiral_range
import numpy as np

freq = np.logspace(1, 3, 1000)
budget = gwinc.load_budget('Aplus', freq)
trace = budget.run()

range = inspiral_range.range(
    freq, trace.psd,
    m1=30, m2=30,
)
```

See the [`inspiral_range`](https://git.ligo.org/gwinc/inspiral-range)
package for more details.


<!-- ## comparison with MATLAB gwinc -->

<!-- `pygwinc` includes the ability use MATLAB gwinc directly via the -->
<!-- MATLAB python interface (see the CLI '--matlab' option above).  This -->
<!-- also allows for easy direct comparison between the pygwinc and -->
<!-- matgwinc noise budgets. -->

<!-- If you have a local checkout of matgwinc (at e.g. /path/to/gwinc) and -->
<!-- a local installation of MATLAB and it's python interface (at -->
<!-- e.g. /opt/matlab/python/lib/python3.6/site-packages) you can run the -->
<!-- comparison as so: -->
<!-- ```shell -->
<!-- $ export GWINCPATH=/path/to/matgwinc -->
<!-- $ export PYTHONPATH=/opt/matlab/python/lib/python3.6/site-packages -->
<!-- $ python3 -m gwinc.test -p aLIGO -->
<!-- ``` -->
<!-- This will produce a summary page of the various noise spectra that -->
<!-- differ between matgwinc and pygwinc. -->

<!-- Latest comparison plots from continuous integration: -->

<!-- * [aLIGO comparison](https://gwinc.docs.ligo.org/pygwinc/aLIGO_test.png) -->
<!-- * [A+ comparison](https://gwinc.docs.ligo.org/pygwinc/A+_test.png) -->
