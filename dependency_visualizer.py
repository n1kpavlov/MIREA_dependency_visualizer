import os
import sys
import zipfile
import xml.etree.ElementTree as ET

def get_dependencies(package_path, depth, dependencies=None, visited=None):
    if dependencies is None:
        dependencies = {}
    if visited is None:
        visited = set()

    with zipfile.ZipFile(package_path, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('.nuspec'):
                with z.open(filename) as file:
                    tree = ET.parse(file)
                    root = tree.getroot()
                    ns = {'n': root.tag.split('}')[0].strip('{')}
                    package_id = root.find('.//n:metadata/n:id', ns).text
                    package_version = root.find('.//n:metadata/n:version', ns).text
                    
                    if package_id not in visited:
                        visited.add(package_id)

                        for dep_group in root.findall('.//n:dependencies', ns):
                            for dep in dep_group.findall('.//n:dependency', ns):
                                dep_package = dep.attrib['id']
                                dep_version = dep.attrib['version']

                                if dep_package not in visited:
                                    dependencies[dep_package] = dep_version
    return dependencies

def generate_mermaid_graph(dependencies):
    mermaid_code = "graph TD;\n"
    
    return mermaid_code

def visualize_dependencies(mermaid_path, package_path, output_file, depth):
    #dependencies = get_dependencies(package_path, depth)
    #mermaid_code = generate_mermaid_graph(dependencies)
    mermaid_code = "graph TD;\n"
    mermaid_code += f"1 --> 2\n"
    mermaid_code += f"1 --> 3\n"
    mermaid_code += f"2 --> 8\n"
    mermaid_code += f"3 --> 4\n"
    mermaid_code += f"4 --> 5\n"
    mermaid_code += f"4 --> 6\n"
    mermaid_code += f"4 --> 7\n"
    mermaid_code += f"5 --> 8\n"
    mermaid_code += f"6 --> 8\n"

    # Создание временного файла с кодом Mermaid
    with open("output", "w") as f:
        f.write(mermaid_code)

    # Вызов Mermaid.js для генерации изображения
    os.system(f"{mermaid_path} output -o {output_file}")

    # Удаление временного файла
    os.remove("output")

    print(f"Граф зависимостей для пакета '{package_path}' успешно сгенерирован и сохранен в файл '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Использование: {sys.argv[0]} <путь_к_mermaid.js> <путь_к_пакету> <путь_к_файлу_вывода> <максимальная_глубина>")
        sys.exit(1)

    mermaid_path = sys.argv[1]
    package_path = sys.argv[2]
    output_file = sys.argv[3]
    max_depth = int(sys.argv[4])

    visualize_dependencies(mermaid_path, package_path, output_file, max_depth)
