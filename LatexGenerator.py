import os
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Center, HorizontalSpace, Command, StandAloneGraphic, Package, Subsubsection
from pylatex.utils import italic, bold, NoEscape

from PIL import Image, ImageDraw, ImageFont  # dynamic import

from objetcs import chapterObject, subchapterObject, lineObject, subsubchapterObject


class generator:
    def __init__(self, filename, lines, filePath, imagesPath):
        self.filename = filename
        self.lines = lines
        self.currentChapter = ""
        self.currentSubChapter = ""
        self.currentSubSubChapter = ""
        self.inChapter = False
        self.inSubChapter = False
        self.inSubSubChapter = False
        self.inExample = False
        self.chapters = []
        self.imagesPath = imagesPath
        self.filePath = filePath

        super().__init__()

    def parseAll(self):
        chapterObj = chapterObject()
        subchapterObj = subchapterObject()
        sschapterObj = subsubchapterObject()
        lineObj = lineObject()

        for i, line in enumerate(self.lines):
            if not line.find("-|-") == -1:
                if self.inChapter:
                    chapterObj.subChapters.append(subchapterObj)
                    self.chapters.append(chapterObj)

                    sschapterObj = subsubchapterObject()
                    subchapterObj = subchapterObject()
                    chapterObj = chapterObject()

                self.currentChapter = line.split("-|-")[1]
                self.inChapter = True
                self.inSubChapter = False
                self.inSubSubChapter = False

                chapterObj.name = self.currentChapter
                continue

            if self.inChapter:
                if not line.find("-#-") == -1:

                    if self.inSubChapter:
                        if not sschapterObj.name == "" and not sschapterObj.lines == []:
                            subchapterObj.sschapters.append(sschapterObj)
                        chapterObj.subChapters.append(subchapterObj)
                        sschapterObj = subsubchapterObject()
                        subchapterObj = subchapterObject()

                    self.currentSubChapter = line.split("-#-")[1]
                    subchapterObj.name = self.currentSubChapter

                    self.inSubChapter = True
                    self.inSubSubChapter = False
                    continue

            if self.inSubChapter:
                if not line.find("-##-") == -1:
                    if self.inSubSubChapter:
                        if not sschapterObj.name == "" and not sschapterObj.lines == []:
                            subchapterObj.sschapters.append(sschapterObj)
                        sschapterObj = subsubchapterObject()

                    self.currentSubSubChapter = line.split("-##-")[1]
                    sschapterObj.name = self.currentSubSubChapter
                    self.inSubSubChapter = True
                    continue

            if not line.find("[[") == -1:
                lineObj.lineType = "image"
                lineObj.content = line.split("[[")[1].replace("]]", "").strip()

                if self.inChapter:
                    if self.inSubChapter:
                        subchapterObj.lines.append(lineObj)
                    else:
                        chapterObj.introLines.append(lineObj)

                lineObj = lineObject()
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
                if self.inSubSubChapter:
                    sschapterObj.lines.append(lineObj)
                else:
                    subchapterObj.lines.append(lineObj)
                lineObj = lineObject()

        subchapterObj.sschapters.append(sschapterObj)
        chapterObj.subChapters.append(subchapterObj)
        self.chapters.append(chapterObj)
        return

    def createParagraph(self, doc, line):
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
                doc.append(italic(line.content))

        if line.lineType == "image":
            imgPath = self.findImageAndConvert(
                line.content)
            if not imgPath == None:

                with doc.create(Figure(position='H')) as image:
                    image.add_image(
                        imgPath)

        return doc

    def generateLatex(self):

        geometry_options = {"tmargin": "1cm",
                            "lmargin": "3cm", "bmargin": "2cm"}
        doc = Document(geometry_options=geometry_options)

        doc.packages.append(Package("float"))

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
                                doc = self.createParagraph(
                                    doc, line)
                        if not subChapter.sschapters == []:
                            for sschapter in subChapter.sschapters:
                                with doc.create(Subsubsection(sschapter.name)):
                                    if not sschapter.lines == []:
                                        for line in sschapter.lines:
                                            doc = self.createParagraph(
                                                doc, line)

        doc.generate_pdf(self.filePath+self.filename, clean_tex=False)

    def findImageAndConvert(self, reqImage):
        path = None
        for fil in os.listdir(self.imagesPath):
            if fil.find(reqImage+".") != -1:
                # Converting Image if Not of the correct format
                if fil.replace(reqImage, "") == ".gif":
                    img = Image.open(self.imagesPath+fil)
                    img.save(self.imagesPath+reqImage+".png", 'png',
                             optimize=True, quality=100)
                    os.remove(self.imagesPath+fil)
                    path = self.imagesPath+fil

                path = self.imagesPath+fil
        return path

    def generate(self):
        self.parseAll()
        self.generateLatex()
