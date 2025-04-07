from json import dumps

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class schema_type(nodes.General, nodes.Element):
    pass


class SchemaTypeDirective(SphinxDirective):

    required_arguments = 1
    optional_arguments = 0
    has_content = False

    def run(self):
        url = self.arguments[0]
        node = schema_type()
        node["url"] = url
        return [node]


def visit_schema_type_node(self, node):
    title = node.parent.next_node(nodes.title)
    schema_type = node["url"]
    data = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title.astext(),
    }
    self.body.append(f'<script type="application/ld+json">{dumps(data)}</script>')


def depart_schema_type_node(self, node):
    return


def setup(app):
    app.add_directive("schema-type", SchemaTypeDirective)
    app.add_node(schema_type, html=(visit_schema_type_node, depart_schema_type_node))
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
