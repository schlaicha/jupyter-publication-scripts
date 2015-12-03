from distutils.core import setup
setup(name = 'jupyter-publication-scripts',
      version = '0.1-dev',
      description = 'Useful scripts for Making publication ready Python Notebooks',
      maintainer = 'Alexander Schlaich',
      maintainer_email = 'aschlaich@physik.fu-berlin.de',
      download_url = 'https://github.com/schlaicha/jupyter-publication-scripts',
      py_modules = ['publicationextensions.PrettyTable'],
)


# Install notebook specific extensions

from jupyter_core.paths import jupyter_config_dir, jupyter_data_dir
import os
import shutil


### from nbextensions ###


# http://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

#
# 1. Get the local configuration file path
#
config_dir = jupyter_config_dir()
data_dir = jupyter_data_dir()

print("Configuration files directory: %s" % config_dir)
print("Extensions and templates path: %s" % data_dir)

# now test if path exists
if os.path.exists(config_dir) is False:
    os.mkdir(config_dir)
if os.path.exists(data_dir) is False:
    os.mkdir(data_dir)

#
# 2. Install files
#   Indiscriminately copy all files from the nbextensions, extensions and template directories
#   Currently there is no other way, because there is no definition of a notebook extension package
#
        
# copy extensions to IPython extensions directory
src = 'extensions'
destination = os.path.join(data_dir, 'extensions')
print("Install Python extensions to %s" % destination)
recursive_overwrite(src, destination)

