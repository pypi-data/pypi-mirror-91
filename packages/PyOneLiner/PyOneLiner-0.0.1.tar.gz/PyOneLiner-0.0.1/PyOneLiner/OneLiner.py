#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This package implement a code OneLiner for python (write a script and get it in oneline). """

###################
#    This package implement a code OneLiner for python.
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

from argparse import ArgumentParser
from secrets import token_bytes
from base64 import b16encode, b32encode, b64encode, b85encode, a85encode
import zlib
import bz2
import lzma
import gzip
import codecs


class OneLiner:

    """ This class implement some functions to get python/bash/batch one line code. """

    def __init__(self, filename, output=None, type_="bash"):
        self.filename = filename
        self.type = type_
        self.output = output
        self.get_bytes()

    def done(self):
        """ This function add the command, save the code and return it. """

        if self.type == "bash":
            self.line = self.line.replace('"', "\\x22")
            if "'" not in self.line:
                self.line += ";b''"
            self.line = f"""python3 -c {repr(self.line)}""".replace(
                "!", "\\x21"
            ).replace("`", "\\x60")
        elif self.type == "batch":
            self.line = self.line.replace('"', "\\x22")
            if "'" not in self.line:
                self.line += ";b''"
            self.line = f"""python -c {repr(self.line)}""".replace(r"\\", "\\")

        if self.output:
            file = open(self.output, "w")
            file.write(self.line)
            file.close()

        return self.line

    def get_bytes(self):
        """ This function get the script from the file. """

        file = open(self.filename, "rb")
        self.bytes = file.read()
        file.close()

    def get_bytecode(self, bytes_):
        """ This function return code in this format: "\\xXX". """

        return "".join(["\\x" + "%02x" % x for x in bytes_])

    def gzip(self):
        self.line = f"import gzip;code=b'{self.get_bytecode(gzip.compress(self.bytes))}';exec(gzip.decompress(code).decode())"

    def zlib(self):
        self.line = f"import zlib;code=b'{self.get_bytecode(zlib.compress(self.bytes))}';exec(zlib.decompress(code).decode())"

    def bz2(self):
        self.line = f"import bz2;code=b'{self.get_bytecode(bz2.compress(self.bytes))}';exec(bz2.decompress(code).decode())"

    def lzma(self):
        self.line = f"import lzma;code=b'{self.get_bytecode(lzma.compress(self.bytes))}';exec(lzma.decompress(code).decode())"

    def base64(self):
        self.line = (
            f"import base64; exec(base64.b64decode({b64encode(self.bytes)}).decode())"
        )

    def base32(self):
        self.line = (
            f"import base64; exec(base64.b32decode({b32encode(self.bytes)}).decode())"
        )

    def base16(self):
        self.line = (
            f"import base64; exec(base64.b16decode({b16encode(self.bytes)}).decode())"
        )

    def base85(self):
        if self.type == "bash":
            self.line = f"import base64; exec(base64.b85decode(b'{self.get_bytecode(b85encode(self.bytes))}').decode())"
        else:
            self.line = f"import base64; exec(base64.b85decode({b85encode(self.bytes)}).decode())"

    def ascii85(self):
        if self.type == "bash":
            self.line = f"import base64; exec(base64.b85decode(b'{self.get_bytecode(a85encode(self.bytes))}').decode())"
        else:
            self.line = f"import base64; exec(base64.b85decode({b85encode(self.bytes)}).decode())"

    def normal(self):
        self.line = f"exec({repr(self.bytes.decode())})"

    def ord(self):
        self.line = f"exec(bytes({[x for x in self.bytes]}).decode())"

    def uu(self):
        if self.type == "bash":
            self.line = f"from codecs import decode;exec(decode(b'{self.get_bytecode(codecs.encode(self.bytes, 'uu'))}', 'uu').decode())"
        else:
            self.line = f"from codecs import decode;exec(decode({codecs.encode(self.bytes, 'uu')}, 'uu').decode())"

    def binary(self):
        self.line = f"exec('{self.get_bytecode(self.bytes)}')"

    def unicode(self):
        bytecode = "".join(["\\u" + "%04x" % x for x in self.bytes])
        self.line = f"exec('{bytecode}')"

    def xor(self):
        key = token_bytes(15)
        key_lenght = len(key)

        bytecode = self.get_bytecode(
            bytes(
                [(key[x % key_lenght] ^ self.bytes[x]) for x in range(len(self.bytes))]
            )
        )

        self.line = f"exec(bytes([{key}[x%{key_lenght}]^b'{bytecode}'[x] for x in range({len(self.bytes)})]).decode())"


def parse():
    parser = ArgumentParser()
    parser.add_argument("filename", help="Script filename.")
    parser.add_argument(
        "--mode",
        "-m",
        help="Mode to change the python payload.",
        default="normal",
        choices=[
            "gzip",
            "bz2",
            "zlib",
            "lzma",
            "base85",
            "base64",
            "ascii85",
            "base32",
            "base16",
            "normal",
            "ord",
            "uu",
            "binary",
            "unicode",
            "xor",
        ],
    )
    parser.add_argument(
        "--console",
        "-c",
        help="Your console.",
        default="python",
        choices=["python", "bash", "batch"],
    )
    return parser.parse_args()


def main():
    parser = parse()

    oneline = OneLiner(parser.filename, type_=parser.console)
    getattr(oneline, parser.mode)()
    print(oneline.done())


if __name__ == "__main__":
    main()
