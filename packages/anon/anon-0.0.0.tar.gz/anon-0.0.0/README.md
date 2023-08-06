---
title: anon
...

<h1>anon</h1>

[![Build Status][travis-image]][travis-link]
[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Commits since latest release][gh-image]][gh-link]

**Table of contents**

- [Installation](#installation)


## Installation

The *base* anon package can be installed from a terminal with the following command:

```bash
$ pip install anon
```

This installation includes basic tools for composing "neural network" -like models along with some convenient IO utilities. However, both automatic differentiation and JIT capabilities require Google's Jaxlib module which is currently in early development and only packaged for Ubuntu systems. On Windows systems this can be easily overcome by downloading the Ubuntu terminal emulator from Microsoft's app store and enabling the Windows Subsystem for Linux (WSL). The following extended command will install anon along with all necessary dependencies for automatic differentiation and JIT compilation:

```bash
$ pip install anon[jax]
```

The in-development version can be installed the following command:

```bash
$ pip install https://github.com/claudioperez/anon/archive/master.zip
```

[pypi-v-image]: https://img.shields.io/pypi/v/anon.svg
[pypi-v-link]: https://pypi.org/project/anon/

[travis-image]: https://api.travis-ci.org/claudioperez/anon.svg?branch=master
[travis-link]: https://travis-ci.org/claudioperez/anon

[gh-link]: https://github.com/claudioperez/anon/compare/v0.0.0...master
[gh-image]: https://img.shields.io/github/commits-since/claudioperez/anon/v0.0.0.svg

