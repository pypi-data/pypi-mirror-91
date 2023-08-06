
treeconfigparser
================

Custom configuration parser based on a tree. 

[Documentation]

[Documentation]: https://gitlab.enpc.fr/cerea-da-team/treeconfigparser

Installation
------------

    $ pip install treeconfigparser

Main usage
----------

    >>> import treeconfigparser as tcp
    >>> config = tcp.TreeConfigParser()
    >>> config.read_file(file_name)
    >>> config.get(['sec1', 'subsec11', 'opt1'])
    'val1'

Features
--------

- Arbitrary configuration tree are possible.
- Can read and parse configuration file. Two different
  and intuitive file formats are supported.
- Configuration files can include comments and
  cross-references between options.
- Alternatively, the configuration can be manipulated
  using the class methods.
- The access to options is simple and supports customised 
  type conversions.
- The configuration can also be written to a file to be
  re-used later on.

More details can be found in the [documentation].

