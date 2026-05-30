"""
Addition to harvester script
"""

# pylint: disable=consider-using-f-string,line-too-long

import os
import collections
import argparse
import textwrap
import pprint
from pprint import PrettyPrinter
from functools import singledispatch, wraps
from typing import get_type_hints
import svd2py


def common_container_checks(f):
    type_ = get_type_hints(f)['object']
    base_impl = type_.__repr__
    empty_repr = repr(type_())   # {}, [], ()
    too_deep_repr = f'{empty_repr[0]}...{empty_repr[-1]}'  # {...}, [...], (...)
    @wraps(f)
    def wrapper(object, context, maxlevels, level):
        if type(object).__repr__ is not base_impl:  # subclassed repr
            return repr(object)
        if not object:                              # empty, short-circuit
            return empty_repr
        if maxlevels and level >= maxlevels:        # exceeding the max depth
            return too_deep_repr
        oid = id(object)
        if oid in context:                          # self-reference
            return pprint._recursion(object)
        context[oid] = 1
        result = f(object, context, maxlevels, level)
        del context[oid]
        return result
    return wrapper

@singledispatch
def saferepr(object, context, maxlevels, level):
    return repr(object)

@saferepr.register
def _handle_int(object: int, *args):
    # uppercase hexadecimal representation with 0x prefix
    return f'0x{object:X}'

@saferepr.register
@common_container_checks
def _handle_dict(object: dict, context, maxlevels, level):
    level += 1
    contents = [
        f'{saferepr(k, context, maxlevels, level)}: '
        f'{saferepr(v, context, maxlevels, level)}'
        for k, v in sorted(object.items(), key=pprint._safe_tuple)
    ]
    return f'{{{", ".join(contents)}}}'

@saferepr.register
@common_container_checks
def _handle_list(object: list, context, maxlevels, level):
    level += 1
    contents = [
        f'{saferepr(v, context, maxlevels, level)}'
        for v in object
    ]
    return f'[{", ".join(contents)}]'

@saferepr.register
@common_container_checks
def _handle_tuple(object: tuple, context, maxlevels : int, level : int) -> str:
    level += 1
    if len(object) == 1:
        return f'({saferepr(object[0], context, maxlevels, level)},)'
    contents = [
        f'{saferepr(v, context, maxlevels, level)}'
        for v in object
    ]
    return f'({", ".join(contents)})'

class HexIntPrettyPrinter(PrettyPrinter):
    def format(self, *args):
        # it doesn't matter what the boolean values are here
        return saferepr(*args), True, False

def main() -> None:
    """
    Main function for SVD adder
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
    Add AVD data structure to device data files in device folder
        '''))

    parser.add_argument("folder",
                        help="path to folder with device files"
                        )

    parser.add_argument('-s', '--svdpath',
                             help="Path to SVD folder",
                             required=True)

    args = parser.parse_args()
    svdparser = svd2py.SvdParser()

    onlyfile = None
    if os.path.splitext(args.folder)[1].lower() == ".py": # only one file!
        onlyfile = os.path.basename(args.folder)
        args.folder = os.path.dirname(args.folder)

    for file in os.listdir(args.folder):
        if onlyfile and onlyfile != file:
            continue
        if os.path.splitext(file)[1].lower() != ".py":
            print("Skipping %s" %  file)
            continue
        svdfile = os.path.join(args.svdpath, os.path.splitext(file)[0].lower() + '.svd')
        if not os.path.exists(svdfile):
            print("No SVD file for '%s' found. Skipping!" % file)
            continue
        with  open(os.path.join(args.folder, file), 'r', encoding='utf-8') as f:
            devicefile = f.read()
        if "'svd' : {" in devicefile:
            print("%s contains already the SVD data" % file)
            continue
        print("Parsing SVD file %s and extending %s" % (svdfile, file))
        devicefile = devicefile[:devicefile.rindex('\n}')]
        svd = svdparser.convert(svdfile)
        with open(os.path.join(args.folder, file), 'w', encoding='utf-8') as f:
            f.write(devicefile)
            f.write(",\n\n    # SVD data\n    'svd' : ")
            hpp = HexIntPrettyPrinter(stream=f)
            hpp.pprint(svd)
            f.write("}")

if __name__ == "__main__":
    main()
