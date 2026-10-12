from pathlib import Path
from ui.workbook import create_app
from library.manager import LibraryManager

def main():
    root = Path(__file__).parent
    library_root = root / "library"
    library = LibraryManager(library_root)

    app = create_app(library)
    app.mainloop()

if __name__ == "__main__":
    main()
