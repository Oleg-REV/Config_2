import yaml
import subprocess
from dependencies import get_dependencies
from pathlib import Path

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def generate_mermaid_graph(package, dependencies):
    graph = ["graph TD"]
    for dep, deps in dependencies.items():
        for sub_dep in deps:
            graph.append(f"    {dep} --> {sub_dep}")
    return "\n".join(graph)

def save_graph_as_png(graph, output_path, graphviz_path):
    mmd_file = Path(output_path).with_suffix(".mmd")
    with open(mmd_file, "w") as file:
        file.write(graph)
    
    subprocess.run([graphviz_path, "-Tpng", str(mmd_file), "-o", output_path], check=True)

def main():
    config = load_config()
    package = config["package_name"]
    max_depth = config["max_depth"]
    output_path = config["output_path"]
    graphviz_path = config["graphviz_path"]

    print("Анализ зависимостей...")
    dependencies = get_dependencies(package, max_depth)

    print("Генерация графа...")
    graph = generate_mermaid_graph(package, dependencies)

    print("Сохранение графа в PNG...")
    save_graph_as_png(graph, output_path, graphviz_path)

    print(f"Граф сохранен в {output_path}")

if name == "main":
    main()
