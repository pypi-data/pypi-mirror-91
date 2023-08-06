import os
from pprint import pprint

import click
import yaml

from splitem.lib import read_target


@click.command()
@click.argument("target")
@click.option("--ext", default='yml', type=str, help='YAML extension to append to output files [Default: yml]')
@click.option("--out-dir", default='', type=str, help='Output directory for generated files. [Default: "./"]')
def run(target, ext, out_dir):
    """Parse a target manifest and extract individual manifests into separate files."""
    manifests = read_target(target)
    out_dir = os.path.abspath(out_dir)
    for manifest in manifests:
        file_name = manifest['metadata']['name'].lower()
        file_desc = manifest['kind'].lower()
        full_file = "{}/{}-{}.{}".format(out_dir, file_desc, file_name, ext)
        print("writing {}".format(full_file))
        with open(full_file, 'w') as f:
            yaml.dump(manifest, f)
