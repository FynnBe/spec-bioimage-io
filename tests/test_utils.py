from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from marshmallow import post_load
from ruamel.yaml import YAML

from bioimageio.spec import fields, load_model_spec, nodes, raw_nodes, schema, utils

yaml = YAML(typ="safe")


@dataclass
class MyNode(nodes.Node):
    field_a: str
    field_b: int


def test_iter_fields():
    entry = MyNode("a", 42)
    assert [("field_a", "a"), ("field_b", 42)] == list(utils._iter_fields(entry))


@dataclass
class Content:
    data: str


class TestNodeVisitor:
    @dataclass
    class Tree(nodes.Node):
        left: Any
        right: Any

    @dataclass
    class URL:
        url: str

    @pytest.fixture
    def tree(self):
        return self.Tree(
            self.Tree(self.Tree(None, None), self.URL("https://example.com")),
            self.Tree(None, self.Tree(None, self.Tree(None, None))),
        )

    def test_node(self, tree):
        visitor = utils._NodeVisitor()
        visitor.visit(tree)

    def test_node_transform(self, tree):
        class MyTransformer(utils._NodeTransformer):
            def transform_URL(self, node):
                return Content(f"content of url {node.url}")

        assert isinstance(tree.left.right, self.URL)
        transformer = MyTransformer()
        transformed_tree = transformer.transform(tree)
        assert isinstance(transformed_tree.left.right, Content)


@dataclass
class MySpec(nodes.Node):
    spec_uri_a: raw_nodes.SpecURI
    spec_uri_b: raw_nodes.SpecURI


class SubSpec(schema.PyBioSchema):
    axes = fields.Axes()

    @post_load
    def make_object(self, data, **kwargs):
        return data


class Spec(schema.PyBioSchema):
    spec_uri_a = fields.SpecURI(SubSpec)
    spec_uri_b = fields.SpecURI(SubSpec)

    @post_load
    def make_object(self, data, **kwargs):
        return MySpec(**data)


class TestTraversingSpecURI:
    def test_resolve_spec(self):
        tree = Spec().load({"spec_uri_a": "https://example.com", "spec_uri_b": "../file.yml"})

        class MyTransformer(utils._NodeTransformer):
            def transform_SpecURI(self, node):
                res = {"axes": "xyc"}
                return node.spec_schema.load(res)

        transformer = MyTransformer()
        transformed_tree = transformer.transform(tree)
        assert {"axes": "xyc"} == transformed_tree.spec_uri_a
        assert {"axes": "xyc"} == transformed_tree.spec_uri_b


def test_resolve_import_path(tmpdir):
    tmpdir = Path(tmpdir)
    manifest_path = tmpdir / "manifest.yaml"
    manifest_path.touch()
    filepath = tmpdir / "my_mod.py"
    filepath.write_text("class Foo: pass", encoding="utf8")
    node = raw_nodes.ImportablePath(filepath=filepath, callable_name="Foo")
    uri_transformed = utils._UriNodeTransformer(root_path=tmpdir).transform(node)
    source_transformed = utils._SourceNodeTransformer().transform(uri_transformed)
    assert isinstance(source_transformed, nodes.ImportedSource)
    Foo = source_transformed.factory
    assert Foo.__name__ == "Foo"
    assert isinstance(Foo, type)


def test_resolve_directory_uri(tmpdir):
    node = raw_nodes.URI(scheme="", authority="", path=str(tmpdir), query="", fragment="")
    uri_transformed = utils._UriNodeTransformer(root_path=Path(tmpdir)).transform(node)
    assert uri_transformed == Path(tmpdir)


def test_load_model_spec(rf_config_path):
    rf_model_data = yaml.load(rf_config_path)
    load_model_spec(rf_model_data, rf_config_path)
