c = get_config()
c.Exporter.preprocessors = [ 'pre_cite2c.BibTexPreprocessor', 'pre_pymarkdown.PyMarkdownPreprocessor', 'pre_markdown.MarkdownPreprocessor' ]
c.TemplateExporter.template_path = ['../templates','.']
c.Exporter.template_file = 'revtex_nocode.tplx'
#c.Exporter.template_file = 'article_nocode.tplx'
