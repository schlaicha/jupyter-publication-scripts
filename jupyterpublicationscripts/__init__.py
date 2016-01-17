from __future__ import print_function

import sys
import os
import json
import io

import logging
from .compat import JUPYTER

log = logging.getLogger(__name__)
log.setLevel(20)


if JUPYTER:
    import notebook.nbextensions as nbe
    from IPython.paths import locate_profile
    from IPython.utils.py3compat import cast_unicode_py2
    from jupyter_core.paths import jupyter_config_dir
    from traitlets.config import Config, JSONFileConfigLoader, ConfigFileNotFound
else :
    import IPython.html.nbextensions as nbe
    from IPython.utils.path import locate_profile
    from IPython.utils.py3compat import cast_unicode_py2
    from IPython.config import Config, JSONFileConfigLoader, ConfigFileNotFound


def install(profile='default', symlink=True, user=False,
            prefix=None, verbose=False, path=None):

    dname = os.path.dirname(__file__)

    # might want to check if already installed and overwrite if exist
    if symlink and verbose:
        log.info('Will try symlink nbextension')
    if prefix and verbose:
        log.info("I'll install in prefix:", prefix)
    
    ''' once we have a notebook extension we might use something like this:

    nbe.install_nbextension(os.path.join(dname,'gdrive'),
                                symlink=symlink,
                                   user=user,
                                 prefix=prefix,
                                 nbextensions_dir=path)
    '''

    activate(profile)

class jconfig(object):

    def __init__(self, profile):
        """
        A context manager that simply expose the configuration values.

        Mutate the value of the configuration while in the context manager,
        and it will be written to disk on exit.
        """
        self.profile = profile

    def __enter__(self):
        if JUPYTER:
            self.pdir = jupyter_config_dir()
            self.cff_name = 'jupyter_nbconvert_config.json'
        else:
            self.pdir = locate_profile(self.profile)
            self.cff_name = 'ipython_nbconvert_config.json'

        jc = JSONFileConfigLoader(self.cff_name, self.pdir)

        try:
            self.config = jc.load_config();
        except (ConfigFileNotFound,ValueError):
            self.config = Config()
        return self.config


    def __exit__( self, type, value, tb ):
        self.config['format'] = 1
        # option to cleanup empty dicts
        if not os.path.exists(self.pdir):
            os.mkdir(self.pdir)
        with io.open(os.path.join(self.pdir,self.cff_name),'w', encoding='utf-8') as f:
            f.write(cast_unicode_py2(json.dumps(self.config, indent=2, default=lambda _:{})))


def activate(profile='default'):
    if not profile:
        raise ValueError('Profile cannot be NoneType')

    return _activate(profile)

def _activate(profile):
    dname = os.path.dirname(__file__)

    with jconfig(profile) as config:
        if "Exporter" in config:
            if (config["Exporter"].get("preprocessors",{})):
                # manually merge setting if exist
                if not 'pre_markdown.MarkdownPreprocessor' in config.Exporter.preprocessors:
                    config['Exporter']['preprocessors'].append('pre_markdown.MarkdownPreprocessor')
                if not 'pre_cite2c.BibTexPreprocessor' in config.Exporter.preprocessors:
                    config['Exporter']['preprocessors'].append('pre_cite2c.BibTexPreprocessor')
            else:
                my_config  = JSONFileConfigLoader('jupyter_nbconvert_config.json', dname).load_config()
                config.merge(my_config)

        if not JUPYTER:
            log.info('Activating preprocessors for profile "%s"' % profile)
        else:
            log.info('Activating preprocessors')


def deactivate(profile='default'):
    """should be a matter of just unsetting the above keys
    """
    with jconfig(profile) as config:
        deact = True;
        if not 'preprocessors' in config.Exporter:
            deact=False
        if deact:
            if 'pre_markdown.MarkdownPreprocessor' in config.Exporter.preprocessors:
                del config.Exporter.preprocessors[config.Exporter.preprocessors.index('pre_markdown.MarkdownPreprocessor')]
            if 'pre_cite2c.BibTexPreprocessor' in config.Exporter.preprocessors:
                del config.Exporter.preprocessors[config.Exporter.preprocessors.index('pre_cite2c.BibTexPreprocessor')]

def main(argv=None):
    import argparse
    prog = '{} -m jupyter-publication-scripts'.format(os.path.basename(sys.executable))
    parser = argparse.ArgumentParser(prog=prog,
                    description='Install jupyter-publication-scripts.')
    parser.add_argument('profile', nargs='?', default='default', metavar=('<profile_name>'), help='profile name in which to install google drive integration for IPython 3.x')

    parser.add_argument("-S", "--no-symlink", help="do not symlink at install time",
                    action="store_false", dest='symlink', default=True)
    parser.add_argument("-u", "--user", help="force install in user land",
                    action="store_true")
    parser.add_argument("-p", "--prefix", help="Prefix where to install extension",
                    action='store', default=None)
    parser.add_argument("-P", "--path", help="explicit path on where to install the extension",
                    action='store', default=None)
    parser.add_argument("-v", "--verbose", help="increase verbosity",
                    action='store_true')
    parser.add_argument("--deactivate", help='deactivate', action='store_true')
    args = parser.parse_args(argv)

    if args.deactivate:
        deactivate()
    else:
        install(   path=args.path,
                   user=args.user,
                 prefix=args.prefix,
                profile=args.profile,
                symlink=args.symlink,
                verbose=args.verbose
                )
