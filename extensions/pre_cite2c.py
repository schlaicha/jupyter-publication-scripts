# -*- coding: utf-8 -*-

"""This preprocessor replaces bibliography code in markdowncell
"""

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
#from __future__ import print_function
from __future__ import (absolute_import, division, print_function, unicode_literals)

from nbconvert.preprocessors import *
import os
import sys
import re
import json

from citeproc.py2compat import *
import citeproc
import citeproc.source.json

import unicode_tex

# unicode_tex replaces also spaces, this causes problems with bibtex and is undesirable anyway
try:
    del unicode_tex.unicode_to_tex_map[u' ']
except KeyError:
    pass

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------
def cite_warn(citation_item):
    print("WARNING: Reference with key '{}' not found in the bibliography.".format(citation_item.key))


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
        currently three common reference types are implemented: articles, books and chapter of books.
        non-ascii characters are only checked for in autor, title and journal name

        Parameters
        ----------
        refkey: str
            Zotero/Cite2c key of references
        reference: dictionary
            Dictonary with cite2c reference data as taken from cite2c JSON metadata
        """
        if (reference["type"] == "article-journal"):
            entry  = "@article{" + refkey + ",\n"
        elif (reference["type"] == "book"):
            entry  = "@book{" + refkey + ",\n"
        elif (reference["type"] == "chapter"):
            entry  = "@inbook{" + refkey + ",\n"
        else:
            # default type is misc!
            entry  = "@misc{" + refkey + ",\n"
            print("Warning: Unknown type of reference "+refkey)

        if ("author" in reference):
            entry += "  author = {"
            entry += " and ".join(map(lambda a: unicode_tex.unicode_to_tex(a["family"]) + ", " + unicode_tex.unicode_to_tex(a["given"]), reference["author"]))
            entry += "}, \n"
        else:
            print("Warning: No author(s) of reference " + refkey)

        if ("title" in reference):
            if reference["type"] == "chapter":
                entry += "  chapter = {" + unicode_tex.unicode_to_tex(reference["title"]) + "}, \n"
            else:
                entry += "  title = {" + unicode_tex.unicode_to_tex(reference["title"]) + "}, \n"
        else:
            print("Warning: No title of reference " + refkey)
        if ("container-title" in reference):
            if reference["type"] == "chapter":
                entry += "  title = {" + unicode_tex.unicode_to_tex(reference["container-title"]) + "}, \n"
            else:
                entry += "  journal = {" + unicode_tex.unicode_to_tex(reference["container-title"]) + "}, \n"

        if ("issued" in reference):
            entry += "  year = {" + reference["issued"]["year"] + "}, \n"
        if ("publisher" in reference):
            entry += "  publisher = {" + reference["publisher"] + "}, \n"
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

    def create_bibfile(self, resources, filename):
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

        data = ""

        for r in self.references:
            data += (self.create_bibentry(r, self.references[r]))
        f = open(filename, "w")
        f.write(data)
        f.close()

        resources['outputs'][filename] = data.encode("utf-8")

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
        if not "cite2c" in nb["metadata"]:
            print ("Did not find cite2c metadata")
            return nb, resources
        if not "citations" in nb["metadata"]["cite2c"]:
            print ("Did not find cite2c metadata")
            return nb, resources

        if "html" in resources["output_extension"]:
            newrefs = []
            for key, value in nb["metadata"]["cite2c"]["citations"].iteritems():
                temp = value
                temp["id"] = key
                newrefs.append(temp)
            bib_source = citeproc.source.json.CiteProcJSON(newrefs)
            bib_style = citeproc.CitationStylesStyle('harvard1', validate=False)
            self.bibliography = citeproc.CitationStylesBibliography(bib_style, bib_source, citeproc.formatter.html)

        if "tex" in resources["output_extension"]:
            self.references = nb["metadata"]["cite2c"]["citations"]
            self.create_bibfile(resources, resources["output_files_dir"]+"/"+resources["unique_key"]+".bib")

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
            replaced = None
            if "html" in resources["output_extension"]:
                replaced = cell.source
                for citation in re.finditer('<cite data-cite=\\"(.*?)\\"></cite>', cell.source):
                    tempcite = citeproc.Citation([citeproc.CitationItem(citation.groups()[0])])
                    self.bibliography.register(tempcite)
                    replaced = re.sub('<cite data-cite=\\"'+citation.groups()[0]+'\\"></cite>', '<a href="#'+tempcite['cites'][0]["key"]+'">'+str(self.bibliography.cite(tempcite, cite_warn))+'</a>', replaced)
            if "<div class=\"cite2c-biblio\"></div>" in cell.source:
                if "html" in resources["output_extension"]:
                    html_bibliography = '<h2 id="bibliography">Bibliography</h2>'
                    for item, key in zip(self.bibliography.bibliography(), self.bibliography.keys):
                        html_bibliography += '<p id="'+key+'">'
                        html_bibliography += str(item)
                        html_bibliography += '</p>\n'
                    replaced = re.sub("<div class=\"cite2c-biblio\"></div>", html_bibliography, cell.source)
                elif "tex" in resources["output_extension"]:
                    replaced = re.sub("<div class=\"cite2c-biblio\"></div>", r"\\bibliography{"+resources["output_files_dir"]+"/"+resources["unique_key"]+r"} \n ", cell.source)
            if replaced:
                cell.source = replaced
        return cell, resources
