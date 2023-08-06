from .. import build
from argparse import ArgumentParser


def main():
    args = process_args(vars(generate_parser().parse_args()))
    return build(args)


def generate_parser():
    parser = ArgumentParser()
    parser.add_argument('platform', default='je', choices=(
        'je', 'be'), help='Which platform the pack is targeting. Should be "je" or "be". Default value is "je".')
    parser.add_argument('type', default='normal', choices=('normal', 'compat', 'legacy', 'mcpack', 'zip'),
                        help='Build type. Depending on "platform" argument, this argument takes different values. For "je", "normal", "compat" and "legacy" are accepted; for "be", "mcpack" and "zip" are accepted. When is "legacy", implies "--format 3".')
    parser.add_argument('-r', '--resource', nargs='*', default='all',
                        help="(Experimental) Include resource modules. Should be module names, 'all' or 'none'. Defaults to 'all'.")
    parser.add_argument('-l', '--language', nargs='*', default='none',
                        help="(Experimental) Include language modules. Should be module names, 'all' or 'none'. Defaults to 'none'.")
    parser.add_argument('-x', '--mixed', nargs='*', default='none',
                        help="(Experimental) Include mixed modules. Should be module names, 'all' or 'none'. Defaults to 'none'.")
    parser.add_argument('-s', '--sfw', action='store_true',
                        help="Use 'suitable for work' strings, equals to '--language sfw'.")
    parser.add_argument('-c', '--collection', nargs='*', default='none',
                        help="(Experimental) Include module collections. Should be module names, 'all' or 'none'. Defaults to 'none'.")
    parser.add_argument('-m', '--mod', nargs='*', default='none',
                        help="(JE only)(Experimental) Include mod string files. Should be file names in 'mods/' folder, 'all' or 'none'. Defaults to 'none'. Pseudoly accepts a path, but only files in 'mods/' work.")
    parser.add_argument('-f', '--format', type=int,
                        help='(JE only) Specify "pack_format". When omitted, will default to 3 if build type is "legacy" and 7 if build type is "normal" or "compat". A wrong value will cause the build to fail.')
    parser.add_argument('-p', '--compatible', action='store_true',
                        help="(BE only) Make the pack compatible to other addons. This will generate only one language file 'zh_CN.lang'.")
    parser.add_argument('-o', '--output', nargs='?', default='builds',
                        help="Specify the location to output packs. Default location is 'builds/' folder.")
    parser.add_argument('--hash', action='store_true',
                        help="Add a hash into file name.")
    return parser


def process_args(args):
    module_types = ('resource', 'language', 'mixed', 'collection')
    args['modules'] = {key: args.pop(key) for key in module_types}
    if args['sfw'] and 'sfw' not in args['modules']['language']:
        args['modules']['language'].append('sfw')
    return args
