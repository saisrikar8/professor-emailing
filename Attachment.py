class Attachment:
    filePath = ''
    content = ''
    filename = ''

    def __init__(self, filepath=''):
        self.filePath = filepath
        filePathList = filepath.split('/')
        self.filename = filePathList[len(filePathList) - 1]
        with open(self.filePath, 'rb') as file_content:
            self.content = file_content.read()