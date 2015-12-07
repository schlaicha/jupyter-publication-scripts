# -*- coding: utf-8 -*-

"""This preprocessor replaces bibliography code in markdowncell
"""

#-----------------------------------------------------------------------------
# Copyright (c) 2015, Julius Schulz
#
# Distributed under the terms of the Modified BSD License.
#
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import print_function

from nbconvert.preprocessors import *
import re
import os
import sys
import unicode_tex

# unicode_tex replaces also spaces, this causes problems with bibtex and is undesirable anyway
try:
    del unicode_tex.unicode_to_tex_map[u' ']
except KeyError:
    pass

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class BibTexPreprocessor(Preprocessor):
    def __init__(self, **kw):
        """
        Public constructor

        Parameters
        ----------
        config : Config
            Configuration file structure
        `**kw`
            Additional keyword arguments passed to parent
        """

        super(BibTexPreprocessor, self).__init__(**kw)

    def create_bibentry(self, refkey, reference):
        """
        returns a string with a bibtex-entry from cite2c reference data.
        currently pretty basic implemetation, does only create article entries.
        non-ascii characters are only checked for in autor, title and journal name

        Parameters
        ----------
        refkey: str
            Zotero/Cite2c key of references
        reference: dictionary
            Dictonary with cite2c reference data as taken from cite2c JSON metadata
        """
        entry  = "@article{" + refkey + ",\n"

        if ("author" in reference):
            entry += "  author = {"
            entry += " and ".join(map(lambda a: unicode_tex.unicode_to_tex(a["family"]) + ", " + unicode_tex.unicode_to_tex(a["given"]), reference["author"]))
            entry += "}, \n"
        else:
            print("Warning: No author(s) of reference " + refkey)

        if ("title" in reference):
            entry += "  title = {" + unicode_tex.unicode_to_tex(reference["title"]) + "}, \n"
        else:
            print("Warning: No title of reference " + refkey)

        if ("issued" in reference):
            entry += "  year = {" + reference["issued"]["year"] + "}, \n"
        if ("container-title" in reference):
            entry += "  journal = {" + unicode_tex.unicode_to_tex(reference["container-title"]) + "}, \n"
        if ("page" in reference):
            entry += "  pages = {" + re.sub("-", "--", reference["page"]) + "}, \n"
        if ("volume" in reference):
            entry += "  volume = {" + reference["volume"] + "}, \n"
        if ("issue" in reference):
            entry += "  issue = {" + reference["issue"] + "}, \n"
        if ("DOI" in reference):
            entry += "  doi = {" + reference["DOI"] + "}, \n"
        if ("URL" in reference):
            entry += "  url = {" + reference["URL"] + "}, \n"

        entry += "}\n"
        entry += "\n"
        return entry

    def create_bibfile(self, filename):
        """
        creates .bib with references from cite2c data in .ipynb JSON metadata
        references must be places in self.references beforehand

        Parameters
        ----------
        filename: str
            filename in which the bibtex entries are saved
        """
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        f = open(filename, "w")
        for r in self.references:
            if (sys.version_info > (3, 0)):
                f.write(self.create_bibentry(r, self.references[r]))
            else:
                f.write(self.create_bibentry(r, self.references[r]).encode('utf-8'))
        f.close()

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply on each notebook.

        Must return modified nb, resources.

        If you wish to apply your preprocessing to each cell, you might want
        to override preprocess_cell method instead.

        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """

        if resources["latex"] != "":
            try:
                self.references = nb["metadata"]["cite2c"]["citations"]
                self.create_bibfile(resources["output_files_dir"]+"/"+resources["unique_key"]+".bib")
                for index, cell in enumerate(nb.cells):
                    nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
            except:
              print ("Did not find cite2c")
        return nb, resources

    def preprocess_cell(self, cell, resources, index):
        """
        Preprocess cell

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """

        if cell.cell_type == "markdown":
            if "<div class=\"cite2c-biblio\"></div>" in cell.source:
                replaced = re.sub("<div class=\"cite2c-biblio\"></div>", r"\\bibliography{"+resources["output_files_dir"]+"/"+resources["unique_key"]+r"} \n ", cell.source)
                cell.source = replaced
        return cell, resources
