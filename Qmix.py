#!/usr/bin/env python3.8
import argparse
import os
import sys


def run(args):
    os.chdir("workflow")
    cmd = "python start.py %s %s %d %s %s"%(args.model,args.cor,int(args.threads),args.initial,args.data)
    os.system(cmd)

# call main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QMix')
    parser.add_argument('-model',
                        type=str,
                        default='4M',
                        choices=['4M', '4X'])

    parser.add_argument('-cor',
                        type=str,
                        default="0.99",
                        help='the correlation threshold')

    parser.add_argument('-threads',
                        type=str,
                        default="18",
                        help='The number of computing threads')

    parser.add_argument('-initial',
                        type=str,
                        default='LG',
                        help='The initial matrix')
    parser.add_argument('-data',
                        type=str,
                        default='',
                        help='The full path of training alignment dataset')

    args = parser.parse_args(sys.argv[1:])

    run(args)
