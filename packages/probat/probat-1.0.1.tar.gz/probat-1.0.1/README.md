## ProBat
**Battery life saver and reminder**

## Getting Started:
Current requirements are:
 - python-termcolor: colorizing the shell on unix

### Install:

    # Via PIP:
    $ pip install probat


    # From Arch AUR repo:
    $ ... -S python-probat

### Run:

    $ probat

### Pro tip:

    # Add this line to your .bashrc so you will see the battery status at login:
    ...
    # Run `probat` if it's found in $PATH
    command -v probat &>/dev/null && probat
    ...

## Contributing

This project welcomes with open arms any intent to contribute in any way :)

**Please leave feedback and ideas on the [issues](https://github.com/codeswhite/waller/issues) page**

Easily set up the project locally for development/testing purposes:

    $ git clone https://github.com/codeswhite/probat
    $ cd ./probat
    $ pipenv install

Note that installing the python requirements can be **alternatively** done via basic `pip`:

    $ pip install -r requirements.txt
