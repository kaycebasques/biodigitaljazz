from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class HiDirective(SphinxDirective):
    """A directive to say hello!"""

    required_arguments = 0

    def run(self) -> list[nodes.Node]:
        return [nodes.paragraph(text="hi")]


def setup(app):
    app.add_directive("hi", HiDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
