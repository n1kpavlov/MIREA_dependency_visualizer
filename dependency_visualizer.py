import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Использование: {sys.argv[0]} <путь_к_mermaid.js> <имя_пакета> <путь_к_файлу_вывода> <максимальная_глубина>")
        sys.exit(1)

    mermaid_path = sys.argv[1]
    package_name = sys.argv[2]
    output_file = sys.argv[3]
    max_depth = int(sys.argv[4])

    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    print(sys.argv[4])
