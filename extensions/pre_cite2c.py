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

    def replace_chars(self, toreplace):
        """
        replaces non-ascii characters in string with latex version, currently only limited characterset

        Parameters
        ----------
        toreplace: str
            string to replace characters in
        """
        new = ""
        for c in toreplace:
            if c==u"&":
                new += r"\&"
            elif c==u"á":
                new += r"\'a"
            elif c==u"é":
                new += r"\'e"
            elif c==u"ó":
                new += r"\'o"
            elif c==u"ú":
                new += r"\'u"
            elif c==u"à":
                new += r"\`a"
            elif c==u"ò":
                new += r"\`o"
            elif c==u"ù":
                new += r"\`u"
            elif c==u"ä":
                new += r"\"a"
            elif c==u"ö":
                new += r"\"o"
            elif c==u"ü":
                new += r"\"u"
            elif c==u"č":
                new += r"{\v{c}}"
            else:
                new += c
        return new

    def create_bibentry(self, refkey, reference):
        """
        returns a string with a bibtex-entry from cite2c reference data.
        currently pretty basic implemetation, does only create article entries.
        non-ascii characters are only checked for in autor and journal name, characterset is also limited!!

        Parameters
        ----------
        refkey: str
            Zotero/Cite2c key of references
        reference: dictionary
            Dictonary with cite2c reference data as taken from cite2c JSON metadata
        """
        entry  = "@article{" + refkey + ",\n"

        entry += "  author = {"
        entry += " and ".join(map(lambda a: self.replace_chars(a["family"]) + ", " + self.replace_chars(a["given"]), reference["author"]))
        entry += "}, \n"

        if ("title" in reference):
            entry += "  title = {" + reference["title"] + "}, \n"
        if ("issued" in reference):
            entry += "  year = {" + reference["issued"]["year"] + "}, \n"
        if ("container-title" in reference):
            entry += "  journal = {" + self.replace_chars(reference["container-title"]) + "}, \n"
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

        try:
          self.references = nb["metadata"]["cite2c"]["citations"]
          self.create_bibfile(resources["output_files_dir"]+"/"+resources["unique_key"]+".bib")
        except:
          print ("Did not find cite2c")
        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
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
