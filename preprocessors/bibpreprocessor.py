"""This preprocessor replaces bibliography code in markdowncell
"""

#-----------------------------------------------------------------------------
# Copyright (c) 2015, Julius Schulz
#
# Distributed under the terms of the Modified BSD License.
#
#-----------------------------------------------------------------------------

from IPython.nbconvert.preprocessors import *
import re
import os
import sys

class BibTexPreprocessor(Preprocessor):

    def create_bibentry(self, refkey, reference):
        entry  = "@article{" + refkey + ",\n"

        entry += "  author = {"
        entry += " and ".join(map(lambda a: a["family"] + ", " + a["given"], reference["author"]))
        entry += "}, \n"

        if ("title" in reference):
            entry += "  title = {" + reference["title"] + "}, \n"
        if ("issued" in reference):
            entry += "  year = {" + reference["issued"]["year"] + "}, \n"
        if ("container-title" in reference):
            entry += "  journal = {" + reference["container-title"] + "}, \n"
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
        try:
          self.references = nb["metadata"]["cite2c"]["citations"]
          self.create_bibfile(resources["output_files_dir"]+"/"+resources["unique_key"]+".bib")
        except:
          print "Did not find cite2c"
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
