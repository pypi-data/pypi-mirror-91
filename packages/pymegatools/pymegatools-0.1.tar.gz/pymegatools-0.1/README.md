# PyMegatools - A WIP Python Wrapper for [megatools](https://megatools.megous.com/)

This is a WIP Python Library for the [megatools](https://megatools.megous.com/) command line utility 

As of right now, you can use this library to download files from mega.nz


## Installation

You can either install it from PyPi
```shell
pip install pymegatools
```

or traditionally with [setup.py](setup.py)
```shell
python3 setup.py install
```

## A quick example

This example shows how to use this wrapper to download any file from mega.nz

```python
from pymegatools import Megatools

# Initialization
# By default the linux x86_64 binary is loaded
mega = Megatools()

# Or you can get the official megatools static binaries for your platform at https://megatools.megous.com/builds/experimental/
# And load it like this:
mega = Megatools(executable="path/to/megatools")

# Downloading a file from url
url = 'https://mega.nz/file/PpVB0CTZ#bwa51HbeKaVjuCff_lzbH4nQnV27uBxmcF89PnnACvY'
output = mega.download(url)
print(output)
```

## Credits

[@megous](https://github.com/megous) for making the amazing megatools cmdline utility
