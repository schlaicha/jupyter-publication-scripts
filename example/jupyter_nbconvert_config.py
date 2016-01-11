c = get_config()
c.Exporter.preprocessors = [ 'pre_cite2c.BibTexPreprocessor', 'pymdpreprocessor.PyMarkdownPreprocessor', 'pre_markdown.MarkdownPreprocessor' ]
c.TemplateExporter.template_path = ['../templates','.']
c.Exporter.template_file = 'revtex_nocode.tplx'
#c.Exporter.template_file = 'article_nocode.tplx'

import re
def re_replace(vars):
    #print re.sub(vars[1], vars[2], vars[0])
    return re.sub(vars[1], vars[2], vars[0])
c.TemplateExporter.filters = { "re_replace" : re_replace}
