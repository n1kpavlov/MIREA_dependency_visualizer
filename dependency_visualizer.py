import os
import sys
import subprocess
import requests
import xml.etree.ElementTree as ET
from typing import Dict, List

NUGET_API_URL = "https://api.nuget.org/v3/index.json"
MAX_DEPTH = 10

def get_dependencies(package_name: str, depth: int = 1) -> Dict[str, List[str]]:
    dependencies = {}
    dependencies[package_name] = []

    if depth <= 0:
        return dependencies

    response = requests.get(NUGET_API_URL)
    if response.status_code != 200:
        raise Exception(f"Ошибка получения данных с NuGet: {response.status_code}")

    data = response.json()
    print(data)

def generate_mermaid_graph(dependencies: Dict[str, List[str]]) -> str:
    mermaid_code = "graph TD;\n"
    
    return mermaid_code

def visualize_dependencies(mermaid_path: str, package_name: str, output_file: str, depth: int) -> None:
    #dependencies = get_dependencies(package_name, depth)
    #mermaid_code = generate_mermaid_graph(dependencies)
    mermaid_code = "graph TD;\n"
    mermaid_code += f"1 --> 2\n"
    mermaid_code += f"1 --> 3\n"
    mermaid_code += f"2 --> 3\n"
    mermaid_code += f"3 --> 4\n"

    # Создание временного файла с кодом Mermaid
    with open("output", "w") as f:
        f.write(mermaid_code)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Использование: {sys.argv[0]} <путь_к_mermaid.js> <имя_пакета> <путь_к_файлу_вывода> <максимальная_глубина>")
        sys.exit(1)

    mermaid_path = sys.argv[1]
    package_name = sys.argv[2]
    output_file = sys.argv[3]
    max_depth = int(sys.argv[4])

    visualize_dependencies(mermaid_path, package_name, output_file, max_depth)
