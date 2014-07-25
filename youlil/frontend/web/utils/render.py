class render_jinja:
    """
        Rendering interface to Jinja2 Templates
        Example:
        
        render= render_jinja('templates')
        render.hello(name='jinja2')
    """
    def __init__(self, *a, **kwargs):
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})

        from jinja2 import Environment,FileSystemLoader
        self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)
        
    def __getattr__(self, name):
        # Assuming all templates end with .html
        path = name + '.html'
        t = self._lookup.get_template(path)
        return t.render
        