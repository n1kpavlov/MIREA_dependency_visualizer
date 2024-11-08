import unittest
from dependency_visualizer import get_dependencies, generate_mermaid_graph, visualize_dependencies

class TestGetDependencies(unittest.TestCase):

    def test_empty_dependencies(self):
        package_path = "newtonsoft.json.13.0.3.nupkg"
        depth = 0
        dependencies = get_dependencies(package_path, depth)
        self.assertEqual(dependencies, {})

    def test_dependencies(self):
        package_path = "newtonsoft.json.13.0.3.nupkg"
        depth = 1
        dependencies = get_dependencies(package_path, depth)
        self.assertEqual(dependencies, {'Newtonsoft.Json:13.0.3': ['Microsoft.CSharp:4.3.0',
                            'NETStandard.Library:1.6.1',
                            'System.ComponentModel.TypeConverter:4.3.0',
                            'System.Runtime.Serialization.Primitives:4.3.0',
                            'System.Runtime.Serialization.Formatters:4.3.0',
                            'System.Xml.XmlDocument:4.3.0']})

class TestGenerateMermaidGraph(unittest.TestCase):

    def test_empty_dependencies(self):
        dependencies = {}
        mermaid_code = generate_mermaid_graph(dependencies)
        self.assertEqual(mermaid_code, "graph TD;\n")

    def test_single_dependency(self):
        dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0"]}
        mermaid_code = generate_mermaid_graph(dependencies)
        self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\n")

    def test_multiple_dependencies(self):
        dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0", "AnotherDependency:1.0.0"]}
        mermaid_code = generate_mermaid_graph(dependencies)
        self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\nTestPackage:1.0.0 --> AnotherDependency:1.0.0\n")

    def test_nested_dependencies(self):
        dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0"], "DependencyPackage:1.0.0": ["NestedDependency:1.0.0"]}
        mermaid_code = generate_mermaid_graph(dependencies)
        self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\nDependencyPackage:1.0.0 --> NestedDependency:1.0.0\n")

    def test_circular_dependencies(self):
        dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0"], "DependencyPackage:1.0.0": ["CircularDependency:1.0.0"], "CircularDependency:1.0.0": ["TestPackage:1.0.0"]}
        mermaid_code = generate_mermaid_graph(dependencies)
        self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\nDependencyPackage:1.0.0 --> CircularDependency:1.0.0\nCircularDependency:1.0.0 --> TestPackage:1.0.0\n")

class TestVisualizeDependencies(unittest.TestCase):

    def test_visualize_dependencies_call(self):
        # Тестирование вызова функции с несуществующими файлами
        mermaid_path = "mermaid"
        package_path = "test_package.nupkg"
        output_file = "test.png"
        depth = 1

        with self.assertRaises(FileNotFoundError): # Ожидаем ошибку нахождения файла
            visualize_dependencies(mermaid_path, package_path, output_file, depth)

if __name__ == '__main__':
    unittest.main()
