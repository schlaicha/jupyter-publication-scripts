# -*- coding: utf-8 -*-

"""This preprocessor replaces HTML colors with latex colors in markdowncell
(this might be extended to more nice things...)
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

from nbconvert.preprocessors import *
import re

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class MarkdownPreprocessor(Preprocessor):
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

        self.colormatch = re.compile(r"<font color='(.*?)'>(.*?)</font>")

        super(MarkdownPreprocessor, self).__init__(**kw)

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
            cell.source = self.colormatch.sub(r"\\textcolor{\1}{\2}", cell.source)
        return cell, resources
