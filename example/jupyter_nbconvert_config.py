c = get_config()
c.Exporter.preprocessors = [ 'bibpreprocessor.BibTexPreprocessor', 'pymdpreprocessor.PyMarkdownPreprocessor', 'mdpreprocess.MarkdownPreprocessor' ]
c.Exporter.template_file = 'revtex_nocode.tplx'
