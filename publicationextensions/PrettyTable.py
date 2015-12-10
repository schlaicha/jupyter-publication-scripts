# class PrettyTable
import collections

class PrettyTable(list):
    """ Overridden list class which takes a 2-dimensional list of
        the form [[1,2,3],[4,5,6]], and renders HTML and LaTeX Table in
        IPython Notebook. For LaTeX export two styles can be chosen.
        If the list is one dimensional it is converted to a single-column list, extra_header may
        then be either a list containing a single element or a string.
        """
    def __init__(self, initlist=[], extra_header=None, print_latex_longtable=True, formatstring=""):
        """
        Public constructor

        Parameters
        ----------
        initlist : list
            list to be converted into pretty table
        extra_header : list
            list of captions for each column of initlist, can also be a string for one dimensional lists
        print_latex_longtable : bool
            if True create longtable in latex representation, otherwise output a simple tabular environment
        formatstring : str
            custom format string for number conversion
        """
        self.print_latex_longtable = print_latex_longtable
        self.formatstring = formatstring
        if not isinstance(initlist[0], collections.Iterable):
            initlist = map(lambda x: [x], initlist)
            if isinstance(extra_header, str):
                extra_header = [extra_header]
        if extra_header is not None:
            if len(initlist[0]) != len(extra_header):
                raise ValueError("Header list must have same length as data has columns.")
            initlist = [extra_header]+list(map(lambda x: map(lambda xx: format(xx, self.formatstring), x), initlist))
#            initlist = [extra_header] + [format(xx, self.formatstring) for x in initlist for xx in x]
        super(PrettyTable, self).__init__(initlist)

    def latex_table_tabular(self):
        latex = ["\\begin{tabular}"]
        latex.append("{"+"|".join((["l"]*len(self[0])))+"}\n")
        for row in self:
            latex.append(" & ".join(map(format, row)))
            latex.append("\\\\ \n")
        latex.append("\\end{tabular}")
        return ''.join(latex)
    def latex_longtable(self):
        latex = ["\\begin{longtable}[c]{@{}"]
        latex.append("".join((["l"]*len(self[0]))))
        latex.append("@{}}\n")
        latex.append("\\toprule\\addlinespace\n")
        first = True
        for row in self:
            latex.append(" & ".join(map(format, row)))
            latex.append("\\\\\\addlinespace \n")
            if first:
                latex.append("\\midrule\\endhead\n")
                first = False
        latex.append("\\bottomrule \n \\end{longtable}")
        return ''.join(latex)

    def _repr_html_(self):
        html = ["<table>"]
        for row in self:
            html.append("<tr>")
            for col in row:
                html.append("<td>{0}</td>".format(col))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)
    def _repr_latex_(self):
        if self.print_latex_longtable:
            return self.latex_longtable()
        else:
            return self.latex_table_tabular()
