#!/bin/bash

#only necessary on strange jupyter/ipython transition setups
#export PYTHONPATH="../preprocessors/:$HOME/.ipython/nbextensions/usability/python-markdown/:$PYTHONPATH"

# convert ipython notebook to latex
ipython nbconvert --to=latex ExampleNotebook.ipynb

# typeset latex file into pdf and run bibtex inbetween, run pdflatex three times to get all references etc. correct
pdflatex ExampleNotebook.tex > /dev/null 2>&1
bibtex ExampleNotebook.aux
pdflatex ExampleNotebook.tex > /dev/null 2>&1
pdflatex ExampleNotebook.tex > /dev/null 2>&1

# cleanup temorary conversion and latex files
rm *.bbl *.aux *.blg *.log *.out *Notes.bib *.tex
#rm -rf ExampleNotebook_files
