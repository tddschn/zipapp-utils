# zipapp-utils

zipapp utilities

- [zipapp-utils](#zipapp-utils)
  - [Features](#features)
  - [Demo](#demo)
  - [Install, Upgrade and Uninstall](#install-upgrade-and-uninstall)
    - [pipx (recommended)](#pipx-recommended)
    - [pip](#pip)
  - [Usage](#usage)
    - [zipapp-utils](#zipapp-utils-1)
    - [zipapp-utils py2pyz](#zipapp-utils-py2pyz)
    - [zipapp-utils create-archive](#zipapp-utils-create-archive)
    - [zipapp-utils create-shell-script](#zipapp-utils-create-shell-script)
    - [Examples](#examples)
      - [Generate a shell script that bundles and runs a python script](#generate-a-shell-script-that-bundles-and-runs-a-python-script)
  - [Why did you make this?](#why-did-you-make-this)
  - [Changelog](#changelog)

## Features
- Creating application archive (`.pyz` files) like `python -m zipapp` does, but with convenient features.
- Create shell scripts that bundle a python scripts with all of its dependencies, and can be executable on any system that has `python3 >= 3.5` installed.

## Demo

See [Generate a shell script that bundles and runs a python script](#generate-a-shell-script-that-bundles-and-runs-a-python-script)

<a href="https://asciinema.org/a/502539"><img src="https://asciinema.org/a/502539.svg" alt="Asciicast" width="650"/></a>

## Install, Upgrade and Uninstall

### pipx (recommended)
```bash
pipx install zipapp-utils
```

About [`pipx`](https://pypa.github.io/pipx)


### [pip](https://pypi.org/project/zipapp-utils)
```bash
pip install zipapp-utils
```


## Usage

### zipapp-utils

zipapp-utils is the base command.

zau is an installed alias for zipapp-utils, you can use them interchangeably.


```
$ zipapp-utils --help # or zau --help

usage: zipapp-utils [-h] [-V] {py2pyz,p,create-archive,ca,zipapp,create-shell-script,sh} ...

zipapp utilities

positional arguments:
  {py2pyz,p,create-archive,ca,zipapp,create-shell-script,sh}
    py2pyz (p)          Create archive from a python script
    create-archive (ca, zipapp)
                        Create a zipapp archive
    create-shell-script (sh)
                        Create an ASCII shellscript that runs a zipapp archive

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
```

### zipapp-utils py2pyz

Create archive from a python script

```
$ zau p --help

usage: zipapp-utils py2pyz [-h] [-d DEP] [-r [REQUIREMENT]] [--output OUTPUT] [--python PYTHON] [--main MAIN] [--compress] SCRIPT

Create archive from a python script

positional arguments:
  SCRIPT                Python script file

options:
  -h, --help            show this help message and exit
  -d DEP, --dep DEP     Add dependency
  -r [REQUIREMENT], --requirement [REQUIREMENT]
                        Install dependencies from the given requirements file. Defaults to "requirements.txt"
  --output OUTPUT, -o OUTPUT
                        The name of the output archive. Required if SOURCE is an archive.
  --python PYTHON, -p PYTHON
                        The name of the Python interpreter to use (default: no shebang line).
  --main MAIN, -m MAIN  The main function of the application (default: use an existing __main__.py).
  --compress, -c        Compress files with the deflate method. Files are stored uncompressed by default.
```

### zipapp-utils create-archive

Create a zipapp archive (.pyz file)

```
$ zau ca --help

usage: zipapp-utils create-archive [-h] [--output OUTPUT] [--python PYTHON] [--main MAIN] [--compress] [--info] source

Create a zipapp archive

positional arguments:
  source                Source directory (or existing archive).

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        The name of the output archive. Required if SOURCE is an archive.
  --python PYTHON, -p PYTHON
                        The name of the Python interpreter to use (default: no shebang line).
  --main MAIN, -m MAIN  The main function of the application (default: use an existing __main__.py).
  --compress, -c        Compress files with the deflate method. Files are stored uncompressed by default.
  --info                Display the interpreter from the archive.
```

### zipapp-utils create-shell-script

Create an ASCII shellscript that runs a zipapp archive

```
$ zau sh --help

usage: zipapp-utils create-shell-script [-h] [-o OUTPUT] PYTHON_APPLICATION_ARCHIVE

Create an ASCII shellscript that runs a zipapp archive

positional arguments:
  PYTHON_APPLICATION_ARCHIVE
                        Path to the pyz file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to the output file, or stdout if not set
```

### Examples

#### Generate a shell script that bundles and runs a python script

As described in the [Why did you make this?](#why-did-you-make-this) section.

See [Demo](#demo) for a recording of the process.

```bash
# make an executable, compressed .pyz file from the script post_status.py, with dependencies pysnc and requests-oauthlib, outputs to test.pyz
zau p post_status.py -d pysnc -d requests-oauthlib -o test.pyz -c

# run test.pyz to verify it works
./test.pyz

# create a shell script that runs test.pyz
zau sh test.pyz -o test.sh

# run test.sh to verify it works
./test.sh

# if it works, just copy the content of test.sh and paste it into a jenkins textbox that runs the script.
# make sure python3 >= 3.5 is installed on the jenkins executor node.
```


## Why did you make this?

This project was created because I needed to run a python script with some dependencies in on a managed Jenkins environment,

and I wasn't able to install any software (including pypi packages) on the node.

I tried to bundle the pypi dependency in my script. 

The closest I've tried was to use `pyinstaller`, which allows you to compile a single executable from a python script. It compiled and ran on my Linux box, but not on the Jenkins node because of incompatible glibc version used by python in the binary.

Then I remembered the `zipapp` module, which allowed me to use this script on Jenkins:

```bash
#!/usr/bin/env bash

ENCODED_PYZ_FILE='{{ encoded_pyz_file }}'

echo -n "${ENCODED_PYZ_FILE}" | base64 -d > /tmp/pyz.pyz
python3 /tmp/pyz.pyz

```

And voila, it worked!

So I decided to create this project to ease the process of creating such shell scripts for use on Jenkins.



## [Changelog](CHANGELOG.md)