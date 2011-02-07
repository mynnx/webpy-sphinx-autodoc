from sphinx.ext.autodoc import Documenter
import re

def pairs(a_list):
    prev = None
    for val in a_list:
        if prev:
            yield prev, val
            prev = None
        else:
            prev = val
        
class URIDocumenter(Documenter):
    objtype = 'uri'
    directivetype = 'function'
    content_indent = u''
    
    def _add_line(self, line):
        super(URIDocumenter, self).add_line(line, '<autodoc>')

    def _routes_from_config(self):
        routes_path = self.env.config.autouri_routes_path
        path, attr = routes_path.rsplit('.', 1)
        module = __import__(path, globals(), locals(), [attr], -1)
        routes = getattr(module, attr)
        return routes

    def parse_name(self):
        import pdb; pdb.set_trace()
        routes = self._routes_from_config()
        method, uri = self.name.split(' ')
        fullname = None
        for (rexp, module) in pairs(routes):
            if re.match(rexp, uri):
                fullname = module
                break

        if not fullname:
            self.directive.warn('No matching URI handlers found for %s' % uri)

        path_components = fullname.split('.')
        self.args = None
        self.retann = None
        self.fullname = fullname
        self.modname = path_components[0]
        self.objpath = path_components[1:] + [method]
        return True

    def add_directive_header(self, sig):
        values = self.name.split(' ')
        headers = ('Method', 'URI')
        col_widths = [len(max(column, key=len)) for column in zip(headers, values)]
        border = ' '.join('=' * width for width in col_widths)
        line_header = ' '.join(value.ljust(width) for (width, value) in zip(col_widths, headers))
        line_content = ' '.join(value.ljust(width) for (width, value) in zip(col_widths, values))

        self._add_line(border)
        self._add_line(line_header)
        self._add_line(border)
        self._add_line(line_content)
        self._add_line(border)
        
def debug_docstring(app, what, name, obj, options, lines):
    annotations = []
    for i, line in enumerate(lines):
        if line.startswith('@'):
            annotations.append(i)

        
    
def setup(app):
    app.add_autodocumenter(URIDocumenter)
    app.add_config_value('autouri_routes_path', None, 'env')
    #app.connect('autodoc-process-docstring', process_docstrings)
