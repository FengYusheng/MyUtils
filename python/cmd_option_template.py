# -*- coding: utf-8 -*

import optparse
import locale
import shutil
import sys
import os

ganyu = """
        感遇
    兰叶春葳蕤，桂华秋皎洁。
    欣欣此生意，自尔为佳节。
    谁知林栖者，闻风坐相悦。
    草木有本心，何须美人折。
        """

def parseOptinos():
    usage = 'Usage: %prog [options] arg1 arg2 ...'
    version = '%prog 0.1'

    parser = optparse.OptionParser(usage=usage, version=version)
    general = optparse.OptionGroup(parser, \
                                   'General options', \
                                   'These options get system information.')

    general.add_option('-s', '--system',     \
                     action='store_true',    \
                     dest='system',          \
                     default=False,          \
                     help='Get system platform.')

    general.add_option('-i', '--interpreter', \
                     action='store_true',     \
                     dest='interpreter',      \
                     default=False,           \
                     help='Get python interpreter version.')

    general.add_option('-e', '--encoding',    \
                     action='store_true',     \
                     dest='encoding',         \
                     default=False,           \
                     help='Get filesystem character encoding.')

    general.add_option('-t', '--terminal',    \
                     action='store_true',     \
                     dest='terminal',         \
                     default=False,           \
                     help='Get terminal size.')

    peom = optparse.OptionGroup(parser, \
                                'Peom options', \
                                'These options list peoms.')

    peom.add_option('--ganyu', \
                    action='store_true', \
                    dest='ganyu', \
                    default=False, \
                    help='Display Gan Yu by Zhang Jiuling.')


    parser.add_option_group(general)
    parser.add_option_group(peom)
    return parser.parse_args(sys.argv[1:])

def run(options, args):
    if options.system:
        print(sys.platform)

    if options.interpreter:
        print(sys.version)

    if options.encoding:
        filename = sys.getfilesystemencoding()
        text = locale.getpreferredencoding()
        print((filename, text))

    if options.terminal:
        terminal_size = shutil.get_terminal_size()
        print(terminal_size.columns, terminal_size.lines)

    if options.ganyu:
        print(ganyu)

if __name__ == '__main__':
    options, args = parseOptinos()
    run(options, args)
