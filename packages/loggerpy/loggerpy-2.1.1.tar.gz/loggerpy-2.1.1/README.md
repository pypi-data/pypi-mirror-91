# loggerpy

The simplest Python logger for everyday tasks.

[![](https://img.shields.io/github/v/release/mett96/loggerpy?color=orange)](https://github.com/mett96/loggerpy/releases/tag/v1.0)
[![](https://img.shields.io/pypi/v/loggerpy?color=green)](https://pypi.org/project/loggerpy/)
[![](https://img.shields.io/pypi/pyversions/loggerpy)](https://www.python.org/downloads/release/python-370/)
[![](https://img.shields.io/github/license/mett96/loggerpy)](https://github.com/mett96/loggerpy/blob/master/LICENSE.md)
[![](https://img.shields.io/github/stars/mett96/loggerpy?style=social)](https://github.com/mett96/loggerpy)



## Table of Contents

* [Installation](#Installation)
* [Instructions](#Instructions)
    * [Configuration](#Configuration)
    * [Logger](#Logger)
    * [Customization](#Customization)
    * [Logger Recovery](#LoggerRecovery)
* [Version](#Version)
* [Next features](#NextFeatures)
* [License](#License)
<!-- * [Authors](#Authors) -->


## Installation

The easiest way to install is throw pip.

```bash
pip install loggerpy
```

## Instructions


In order to use this simple logger, many examples are provided inside [examples directory](https://github.com/mett96/loggerpy/tree/master/examples)

![logging ](https://raw.githubusercontent.com/mett96/loggerpy/master/imgs/logger_example.png)


### Configuration
The main classes of the `loggerpy` package are `Logger` and `Level`.

```python
from loggerpy import Logger, Level
```

The `Logger` class is a _Singleton_, so you can recall the `__init__` method through `Logger()` and the same instance will always be returned.

```python
logger = Logger()
```

The possible customization of the logger instance are:
- name: the name of all loggers
- folder: the path of saving log if you want to save them
- print_level: the minimum level of printing 
- save_level: the minimum level of saving, they can be different

In order to simplify the customization of printing and saving level it is provided a class that contained the 6 possible levels of logging. 
Importing _Level_ from loggerpy, they can be used eg Level.DEBUG or Level.WARNING
- Level.NO_LOGGER
- Level.DEBUG
- Level.INFO
- Level.WARNING
- Level.ERROR
- Level.CRITICAL

The _path_ can be set as absolute or relative.
If the path is an absolute path it is used directly, otherwise it put after the project path. The default value is the project path

     E.g.
     Relative path
     -------------
     >>> logger.folder = 'relative_path'
     In this case the used path is:
     > /path/to/the/project/relative_path

     Absolute path
     -------------
     >>> logger.folder = 'absolute_path'
     It is setted as global path
     > /absolute_path/

Configuration [example](https://github.com/mett96/loggerpy/tree/master/examples/configuration.py)


### Logger
Now, it's time to create your first logger.
```python
from loggerpy import Logger

logger = Logger()
logger.name = "First logger"
```

First logger [example](https://github.com/mett96/loggerpy/tree/master/examples/first_logger.py)

### Customization
The parameters of the Logger class can be set all in one time.

```python
logger.configure(name="Name", log_folder="path/to/log/folder", print_level=Level.DEBUG, save_level=LEVEL.WARNING)
```

An [example](https://github.com/mett96/loggerpy/tree/master/examples/second_logger.py)


## Versions
*stable version*
* 1.0 : 
   - first release
* 1.1 : 
   - rewritten the input path of saving log in _configure()_ and _get_logger()_
   - configuration works properly for all file of your project
  
* 2.0 :
  - Logger is now a Singleton
  - Level is an enum


## NextFeatures
- [ ] custom _format_ for timestamp
- [ ] custom _format_ for all log
- [ ] custom _color_ for each level

<!-- ## Authors -->

## License
This project is under the GPL-3.0 license - see the [LICENSE.md](LICENSE.md) file for more details
