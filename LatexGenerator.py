from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Center
from pylatex.utils import italic


class generator:
    def __init__(self, lines):
        self.lines = lines
        self.currentChapter = ""
        self.currentSubChapter = ""
        self.inChapter = False
        self.inSubChapter = False

        self.chapters = []
        super().__init__()

    def parseAll(self):
        chapterObj = {
            "name": "",
            "intro": "",
            "subChapters": [],
        }
        subchapterObj = {
            "name": "",
            "text": ""
        }
        for i, line in enumerate(self.lines):
            if not line.find("-|-") == -1:
                if self.inChapter:
                    chapterObj["subChapters"].append(subchapterObj)
                    self.chapters.append(chapterObj)
                    chapterObj = {
                        "name": "",
                        "intro": "",
                        "subChapters": [],
                    }
                    subchapterObj = {
                        "name": "",
                        "text": ""
                    }

                self.currentChapter = line.split("-|-")[1]
                self.inChapter = True
                self.inSubChapter = False

                chapterObj["name"] = self.currentChapter
                continue

            if self.inChapter:
                if not line.find("-#-") == -1:

                    if self.inSubChapter:
                        chapterObj["subChapters"].append(subchapterObj)
                        subchapterObj = {
                            "name": "",
                            "text": ""
                        }

                    self.currentSubChapter = line.split("-#-")[1]
                    subchapterObj["name"] = self.currentSubChapter

                    self.inSubChapter = True
                    continue

            if self.inChapter and not self.inSubChapter:
                chapterObj["intro"] = chapterObj["intro"] + line

            if self.inSubChapter:
                subchapterObj["text"] = subchapterObj["text"] + line

        chapterObj["subChapters"].append(subchapterObj)
        self.chapters.append(chapterObj)
        return

    def generateLatex(self):

        geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
        doc = Document(geometry_options=geometry_options)

        for chapter in self.chapters:
            with doc.create(Section(str(chapter["name"]))):
                if not chapter["intro"] == []:
                    for line in chapter["intro"]:
                        doc.append(line)
                for subchapter in chapter["subChapters"]:
                    with doc.create(Subsection(subchapter["name"])):
                        if not subchapter["text"] == "":
                            for line in subchapter["text"]:
                                doc.append(line)

        doc.generate_pdf('full', clean_tex=False)

    def parseText(self):
        buff = []
        for i, chapter in enumerate(self.chapters):
            for line in chapter["intro"].split("\n"):
                if not line == "":
                    buff.append(str(line + "\n"))

            self.chapters[i]["intro"] = buff
            buff = []
            for j, subchapter in enumerate(chapter["subChapters"]):
                for line in subchapter["text"].split("\n"):
                    if not line == "":
                        buff.append(str(line + "\n"))
                        self.chapters[i]["subChapters"][j]["text"] = buff
                buff = []

    def generate(self):
        self.parseAll()
        self.parseText()
        self.generateLatex()
