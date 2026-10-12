from PyPDF2 import PdfMerger
import sys

def main():
    merger = PdfMerger()
    for pdf in sys.argv[1:]:
        merger.append(pdf)
    merger.write("merged.pdf")
    merger.close()

if __name__ == "__main__":
    main()
