from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Center, HorizontalSpace
from pylatex.utils import italic, bold

from objetcs import chapterObject, subchapterObject, lineObject


class generator:
    def __init__(self, lines):
        self.lines = lines
        self.currentChapter = ""
        self.currentSubChapter = ""
        self.inChapter = False
        self.inSubChapter = False
        self.inExample = False

        self.chapters = []

        super().__init__()

    def parseAll(self):
        chapterObj = chapterObject()
        subchapterObj = subchapterObject()
        lineObj = lineObject()
        for i, line in enumerate(self.lines):
            if not line.find("-|-") == -1:
                if self.inChapter:
                    chapterObj.subChapters.append(subchapterObj)
                    self.chapters.append(chapterObj)

                    subchapterObj = subchapterObject()
                    chapterObj = chapterObject()
                    chapterObj.subChapters = []
                    subchapterObj.lines = []

                self.currentChapter = line.split("-|-")[1]
                self.inChapter = True
                self.inSubChapter = False

                chapterObj.name = self.currentChapter
                continue

            if self.inChapter:
                if not line.find("-#-") == -1:

                    if self.inSubChapter:
                        chapterObj.subChapters.append(subchapterObj)
                        subchapterObj = subchapterObject()
                        subchapterObj.lines = []

                    self.currentSubChapter = line.split("-#-")[1]
                    subchapterObj.name = self.currentSubChapter

                    self.inSubChapter = True
                    continue

            if self.inChapter and not self.inSubChapter:
                lineObj.lineType = "normal"
                lineObj.content = line
                chapterObj.introLines.append(lineObj)
                lineObj = lineObject()

            if self.inSubChapter:
                lineObj.lineType = "normal"

                if self.inExample:
                    lineObj.lineType = "example"

                if not line.find("---") == -1 and line.find("--- ---") == -1:
                    self.inExample = True
                    lineObj.lineType = "example"
                    lineObj.title = line.split("---")[1]
                    line = ""

                if not line.find("--- ---") == -1:
                    self.inExample = False
                    continue

                if not line.find("***") == -1:
                    line = line.split("*** ")[1]
                    lineObj.lineType = "math"

                lineObj.content = line
                subchapterObj.lines.append(lineObj)
                lineObj = lineObject()

        chapterObj.subChapters.append(subchapterObj)
        self.chapters.append(chapterObj)
        return

    def generateLatex(self):

        geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
        doc = Document(geometry_options=geometry_options)

        for chapter in self.chapters:
            with doc.create(Section(str(chapter.name))):
                # Chapter Intro
                if not chapter.introLines == []:
                    for line in chapter.introLines:
                        if line.lineType == "normal":
                            doc.append(line.content)
                # Subchapter
                for subChapter in chapter.subChapters:
                    with doc.create(Subsection(subChapter.name)):
                        if not subChapter.lines == []:
                            for line in subChapter.lines:
                                # Normal Line
                                if line.lineType == "normal":
                                    doc.append(line.content)
                                # Line with formula
                                if line.lineType == "math":
                                    with doc.create(Alignat(numbering=True, escape=False)) as math_eq:
                                        math_eq.append(line.content)

                                # Example Lines
                                if line.lineType == "example":
                                    if not line.title == "":
                                        doc.append(bold(line.title+"\n"))
                                    else:
                                        # doc.append(HorizontalSpace(size="2cm"))
                                        doc.append(italic(line.content))

        doc.generate_pdf('full', clean_tex=False)

    def generate(self):
        self.parseAll()
        self.generateLatex()
