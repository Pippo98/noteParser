class chapterObject(object):
    name = ""
    introLines = []
    subChapters = []

    def __init__(self):
        self.name = ""
        self.introLines = []
        self.subChapters = []


class subchapterObject(object):
    name = ""
    lines = []
    sschapters = []

    def __init__(self):
        self.name = ""
        self.lines = []
        self.sschapters = []


class subsubchapterObject(object):
    name = ""
    lines = []
    sschapters = []

    def __init__(self):
        self.name = ""
        self.lines = []
        self.sschapters = []


class lineObject(object):
    lineType = "normal"
    content = ""
    title = ""

    def __init__(self):
        self.lineType = "normal"
        self.content = ""
        self.title = ""
