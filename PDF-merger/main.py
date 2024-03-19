from tkinter import *

from tkinter import filedialog
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import PyPDF2

global root
global pdfTree
global count
global filePath
#global pop

count = 0
filePath = '%userprofile%/documents'


# Helper function to sort pdf:s
def treeToList():
    pdfList = []
    for pdf in pdfTree.get_children():
        pdfList.append(pdfTree.item(pdf)['values'])

    return pdfList


# Remove all pdf:s in the list
def removeAll():
    global pdfTree
    for pdf in pdfTree.get_children():
        pdfTree.delete(pdf)


# Remove selected pdf:S
def removeRow():
    pdfs = pdfTree.selection()
    for pdf in pdfs:
        pdfTree.delete(pdf)

# Sort the pdf list in ascending order.
def ascendingOrder():
    global count
    pdfList = treeToList()
    pdfList.sort()
    removeAll()
    for pdf in pdfList:
        pdfTree.insert(parent='', index='end', iid=count, text="", values=pdf)
        count += 1

# Sort the odf list in descending order
def descendingOrder():
    global count
    pdfList = treeToList()
    pdfList.sort()
    removeAll()
    for pdf in reversed(pdfList):
        pdfTree.insert(parent='', index='end', iid=count, text="", values=pdf)
        count += 1

# Add pdf to list
def addPdf():
    global pdfTree
    global count
    global filePath

    # Put filepath in list
    pdfPaths = filedialog.askopenfilenames(initialdir=filePath,
                                           title="Select PDFs to add",
                                           filetypes=(("PDF", "*.pdf"),))

    # Splitt path in directory and filename and put them in treeview
    for p in pdfPaths:
        splittedPAth = [p[0:p.rfind('/') + 1], p[p.rfind('/') + 1:]]
        pdfTree.insert(parent='', index='end', iid=count, text="", values=splittedPAth)

        count += 1

    filePath = splittedPAth[0]

# Merge pdf:s in the list
def mergePdf():
    pdfList = treeToList()

    if len(pdfList) == 0:
        return

    fileName = filedialog.asksaveasfilename(defaultextension="*.pdf", title="Save file", initialdir=filePath,
                                            filetypes=(("PDF", "*.pdf"),))

    outputFile = PyPDF2.PdfMerger()

    if len(pdfList) == 0:
        return

    for pdf in pdfList:
        outputFile.append(pdf[0] + pdf[1])

    outputFile.write(fileName)

# Move selected pdf:s in the list up
def moveUp():
    rows = pdfTree.selection()

    for row in rows:
        pdfTree.move(row, pdfTree.parent(row), pdfTree.index(row) - 1)

# Move selected pdf:s in the list down
def moveDown():
    rows = pdfTree.selection()

    for row in reversed(rows):
        pdfTree.move(row, pdfTree.parent(row), pdfTree.index(row) + 1)

# Start to bild the GUI
def buildGUI():
    # Variables
    global root
    global pdfTree
    title = 'PDF-merger 2000'
    windowWidth = 700
    windowHeight = 800
    leftMargin = 20
    style = "info"

    # Root setup
    root = tb.Window(themename="solar")
    root.title(title)
    root.geometry(f'{windowWidth}x{windowHeight}')
    root.minsize(windowWidth, windowHeight)

    # Name tag
    nameFrame = Frame(root)
    nameFrame.pack(fill=X)

    nameTag = Label(nameFrame, text=title, font=("", 20))
    nameTag.pack(side=LEFT, padx=leftMargin)

    # Main frame
    mainFrame = Frame(root)
    mainFrame.pack(fill=BOTH, padx=leftMargin)

    # Tree view to hold PDF-list
    treeViewFrame = Frame(mainFrame)
    treeViewFrame.pack(fill=BOTH)

    treeScroll = tb.Scrollbar(treeViewFrame, bootstyle=f"{style} round")
    treeScroll.pack(side=RIGHT, fill=Y)

    columns = ("Directory", "File name")
    pdfTree = tb.Treeview(treeViewFrame,
                          columns=(columns),
                          show="headings",
                          bootstyle=(style),
                          height=40,
                          yscrollcommand=treeScroll.set)

    treeScroll.config(command=pdfTree.yview)

    for c in columns:
        pdfTree.heading(c, text=c, anchor=W)
    pdfTree.pack(fill=BOTH)

    # Create buttons and put them in a frame
    buttonFrame = Frame(mainFrame, width=640, height=150)
    buttonFrame.pack_propagate(False)
    for column in range(4):
        buttonFrame.columnconfigure(column, weight=1)

    buttonFrame.pack(pady=20, side=LEFT)

    # Constructing a 2D list containing button test and button function
    buttonList = [
        ["Remove all", "Ascending order", "Move upp", "Add PDF", "Remove row(s)", "Descending  order", "Move down",
         "Merge PDFs"],
        [removeAll, ascendingOrder, moveUp, addPdf, removeRow, descendingOrder, moveDown, mergePdf]]

    for index, (text, command) in enumerate(zip(buttonList[0], buttonList[1])):
        if text != "Merge PDFs":
            buttonSize = 17
            button = tb.Button(buttonFrame,
                               bootstyle=style,
                               text=text,
                               command=command,
                               width=buttonSize)

        else:
            buttonStyle = tb.Style()
            buttonStyle.configure('succes.TButton', font=(33,))
            button = tb.Button(buttonFrame, bootstyle=style, text=text, command=command, style='succes.TButton')

        xPos = 700 / 4 * (index % 4)
        yPos = 50 * (index // 4)
        button.place(y=yPos, x=xPos)

    root.mainloop()


def main():
    buildGUI()
    fileList = []


if __name__ == '__main__':
    main()
