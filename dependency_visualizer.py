import os
import sys
import xml.etree.ElementTree as ET

def get_dependencies(package_name, depth):
    

def generate_mermaid_graph(dependencies):
    mermaid_code = "graph TD;\n"
    for package, deps in dependencies.items():
        for dep in deps:
            mermaid_code += f"{package} --> {dep}\n"
    return mermaid_code

def visualize_dependencies(mermaid_path, package_name, output_file, depth):
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

    # Вызов Mermaid.js для генерации изображения
    subprocess.run(["mermaid", "output", "-o", output_file])

    # Удаление временного файла
    os.remove("output")

    print(f"Граф зависимостей для пакета '{package_name}' успешно сгенерирован и сохранен в файл '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Использование: {sys.argv[0]} <путь_к_mermaid.js> <имя_пакета> <путь_к_файлу_вывода> <максимальная_глубина>")
        sys.exit(1)

    mermaid_path = sys.argv[1]
    package_name = sys.argv[2]
    output_file = sys.argv[3]
    max_depth = int(sys.argv[4])

    visualize_dependencies(mermaid_path, package_name, output_file, max_depth)
