import subprocess
from collections import defaultdict

def fetch_package_dependencies(package):
    try:
        result = subprocess.run(
            ["apk", "info", "-R", package], 
            capture_output=True, 
            text=True, 
            check=True
        )
        lines = result.stdout.splitlines()
        dependencies = []
        for line in lines[1:]:
            dep = line.strip()
            if dep:
                dependencies.append(dep)
        return dependencies
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ошибка получения зависимостей для {package}: {e}")

def get_dependencies(package, max_depth):
    graph = defaultdict(list)
    visited = set()

    def dfs(pkg, depth):
        if depth > max_depth or pkg in visited:
            return
        visited.add(pkg)
        deps = fetch_package_dependencies(pkg)
        graph[pkg].extend(deps)
        for dep in deps:
            dfs(dep, depth + 1)

    dfs(package, 0)
    return graph
