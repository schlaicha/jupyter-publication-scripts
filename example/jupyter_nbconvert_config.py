#--- nbextensions configuration ---
from jupyter_core.paths import jupyter_config_dir, jupyter_data_dir
import os
import sys

sys.path.append(os.path.join(jupyter_data_dir(), 'extensions'))

c = get_config()
c.Exporter.template_path = [ '.', os.path.join(jupyter_data_dir(), 'templates') ]

import publicationextensions.replace as pbe_replace
if not "filters" in c.TemplateExporter:
  c.TemplateExporter.filters = {}
c.TemplateExporter.filters["re_replace"] = pbe_replace.re_replace
