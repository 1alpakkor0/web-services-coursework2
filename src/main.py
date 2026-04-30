try:
    from .crawler import Crawler
    from .indexer import Indexer
    from .search import SearchEngine
except ImportError:
    from crawler import Crawler
    from indexer import Indexer
    from search import SearchEngine


INDEX_FILE = "data/index.json"


def show_help():
    print("""
Available commands:

build
    Crawl the website, build the inverted index and save it.

load
    Load the previously saved index file.

print <word>
    Print the inverted index entry for a word.

find <query terms>
    Find pages containing all query terms.

help
    Show this help message.

exit
    Exit the search tool.
""")


def main():
    print("COMP3011 Search Engine Tool")
    print("Type 'help' to see available commands.")

    index_data = None
    search_engine = None

    while True:
        command = input("> ").strip()

        if not command:
            continue

        parts = command.split()
        action = parts[0].lower()

        if action == "exit":
            print("Exiting search tool.")
            break

        elif action == "help":
            show_help()

        elif action == "build":
            crawler = Crawler()
            pages = crawler.crawl()

            indexer = Indexer()
            index_data = indexer.build_index(pages)
            indexer.save_index(INDEX_FILE, index_data)

            search_engine = SearchEngine(index_data)

            print(f"Index built successfully.")
            print(f"Pages crawled: {len(index_data['documents'])}")
            print(f"Unique words indexed: {len(index_data['index'])}")
            print(f"Index saved to {INDEX_FILE}")

        elif action == "load":
            try:
                indexer = Indexer()
                index_data = indexer.load_index(INDEX_FILE)
                search_engine = SearchEngine(index_data)

                print("Index loaded successfully.")
                print(f"Documents loaded: {len(index_data['documents'])}")
                print(f"Unique words loaded: {len(index_data['index'])}")

            except FileNotFoundError as error:
                print(error)

        elif action == "print":
            if search_engine is None:
                print("No index loaded. Please run 'build' or 'load' first.")
                continue

            if len(parts) != 2:
                print("Usage: print <word>")
                continue

            word = parts[1]
            result = search_engine.print_word_index(word)
            print(result)

        elif action == "find":
            if search_engine is None:
                print("No index loaded. Please run 'build' or 'load' first.")
                continue

            if len(parts) < 2:
                print("Usage: find <query terms>")
                continue

            query = " ".join(parts[1:])
            results = search_engine.find(query)

            if not results:
                print("No matching pages found.")
            else:
                print(f"Found {len(results)} matching page(s):")
                for result in results:
                    print(
                        f"- {result['url']} "
                        f"(score: {result['score']}, doc_id: {result['doc_id']})"
                    )

        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()