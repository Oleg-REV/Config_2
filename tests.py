import pytest
from dependencies import get_dependencies
from visualizer import generate_mermaid_graph

def test_get_dependencies(mocker):
    mock_fetch = mocker.patch("dependencies.fetch_package_dependencies", return_value=["dep1", "dep2"])
    result = get_dependencies("example-package", 1)
    assert result == {"example-package": ["dep1", "dep2"]}
    mock_fetch.assert_called_once_with("example-package")

def test_generate_mermaid_graph():
    dependencies = {"pkg1": ["dep1", "dep2"], "dep1": ["dep3"]}
    result = generate_mermaid_graph("pkg1", dependencies)
    expected = (
        "graph TD\n"
        "    pkg1 --> dep1\n"
        "    pkg1 --> dep2\n"
        "    dep1 --> dep3"
    )
    assert result == expected
