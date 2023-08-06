# OneLiner

## Description
This package implement a code OneLiner for python (write a script and get it in oneline).

## Requirements
This package require :
 - python3
 - python3 Standard Library

## Installation
```bash
pip install PyOneliner
```

## Examples

### Command lines
1. For python console:
```bash
PyOneLiner script.py
PyOneLiner script.py --mode "uu"
```
2. For bash console:
```bash
PyOneLiner script.py --mode "base64" --console "bash"
PyOneLiner script.py --mode "unicode" --console "bash"
```
3. For windows cmd:
```bash
PyOneLiner script.py --mode "gzip" --console "batch"
PyOneLiner script.py --mode "ord" --console "batch"
```

### Python3
```python
from PyOneLiner import OneLiner
from os import system

oneliner = OneLiner("script.py", type_="python")
oneliner.xor()
oneline = oneliner.done()
exec(oneline)

oneliner.ascii85()
oneline = oneliner.done()
exec(oneline)

oneliner = OneLiner("script.py", type_="bash") # Linux
oneliner.lzma()
oneline = oneliner.done()
system(oneline)

oneliner.binary()
oneline = oneliner.done()
system(oneline)

oneliner = OneLiner("script.py", type_="batch") # Windows
oneliner.base16()
oneline = oneliner.done()
system(oneline)

oneliner.bz2()
oneline = oneliner.done()
system(oneline)
```

## Link
[Github Page](https://github.com/mauricelambert/PyOneLiner)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).