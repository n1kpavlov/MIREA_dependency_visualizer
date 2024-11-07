import os
import sys
import zipfile
import xml.etree.ElementTree as ET

def get_dependencies(package_path, depth, dependencies=None, visited=None):
    # Инициализация словаря зависимостей и множества посещенных пакетов
    if dependencies is None:
        dependencies = {}
    if visited is None:
        visited = set()

    # Отсчет максимальной глубины
    if depth > 0:
        # Открываем .nupkg файл как zip-архив
        with zipfile.ZipFile(package_path, 'r') as z:
            # Перебираем все файлы в архиве
            for filename in z.namelist():
                # Ищем файл .nuspec, содержащий метаданные пакета
                if filename.endswith('.nuspec'):
                    with z.open(filename) as file:
                        # Парсим .nuspec файл
                        tree = ET.parse(file)
                        root = tree.getroot()
                        ns = {'n': root.tag.split('}')[0].strip('{')}  # Определяем пространство имен
                        package_id = root.find('.//n:metadata/n:id', ns).text  # Получаем ID пакета
                        package_version = root.find('.//n:metadata/n:version', ns).text  # Получаем версию пакета
                        dependencies[f"{package_id}:{package_version}"] = []

                        # Проверяем, был ли уже обработан этот пакет
                        if f"{package_id}:{package_version}" not in visited:
                            visited.add(f"{package_id}:{package_version}")  # Добавляем пакет в посещенные

                            # Ищем группы зависимостей
                            for dep_group in root.findall('.//n:dependencies', ns):
                                for dep in dep_group.findall('.//n:dependency', ns):
                                    dep_package = dep.attrib['id']  # ID зависимого пакета
                                    dep_version = dep.attrib['version']  # Версия зависимого пакета
                                    if f"{dep_package}:{dep_version}" not in dependencies[f"{package_id}:{package_version}"]:
                                        dependencies[f"{package_id}:{package_version}"].append(f"{dep_package}:{dep_version}") # Добавление в список зависимостей

                                    # Если зависимый пакет еще не был посещен, устанавливаем его, рекурсивно ищем зависимости для него и удаляем
                                    if f"{dep_package}:{dep_version}" not in visited:
                                        os.system(f"curl -o {dep_package.lower()}.{dep_version}.nupkg https://api.nuget.org/v3-flatcontainer/{dep_package.lower()}/{dep_version}/{dep_package.lower()}.{dep_version}.nupkg")

                                        dep_nupkg_path = f"{dep_package.lower()}.{dep_version}.nupkg"
                                        get_dependencies(dep_nupkg_path, depth - 1, dependencies, visited)

                                        os.remove(f"{dep_package.lower()}.{dep_version}.nupkg")

    return dependencies  # Возвращаем все найденные зависимости

def generate_mermaid_graph(dependencies):
    mermaid_code = "graph TD;\n"

    # Преобразуем каждую зависимость в Mermaid код
    for package, deps in dependencies.items():
        for dep in deps:
            mermaid_code += f"{package} --> {dep}\n"

    return mermaid_code

def visualize_dependencies(mermaid_path, package_path, output_file, depth):
    dependencies = get_dependencies(package_path, depth)
    mermaid_code = generate_mermaid_graph(dependencies)

    # Создание временного файла с кодом Mermaid
    with open("output", "w") as f:
        f.write(mermaid_code)

    # Вызов Mermaid.js для генерации изображения
    os.system(f"{mermaid_path} output -o {output_file}")

    # Удаление временного файла
    os.remove("output")

    print(f"Граф зависимостей для пакета '{package_path}' успешно сгенерирован и сохранен в файл '{output_file}'.")

if __name__ == "__main__":
    # Парсинг команды из командной строки
    if len(sys.argv) != 5:
        print(f"Использование: {sys.argv[0]} <путь_к_mermaid.js> <путь_к_пакету> <путь_к_файлу_вывода> <максимальная_глубина>")
        sys.exit(1)

    mermaid_path = sys.argv[1]
    package_path = sys.argv[2]
    output_file = sys.argv[3]
    max_depth = int(sys.argv[4])

    visualize_dependencies(mermaid_path, package_path, output_file, max_depth)
