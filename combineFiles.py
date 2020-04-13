import os

def combine(fileDir, fileType):
    fileArrayNames = []
    fileArrayInfo = []
    counter = 0
    fileWrite = ""
    createFile = os.path.join(fileDir, "output.txt")
    outputFile = open(createFile,"w+")
    for file in os.listdir(fileDir):
        if file.endswith(fileType):
            fileArrayNames = fileArrayNames + [os.path.join(fileDir, file)]
            fileArrayInfo = fileArrayInfo + [0]
            counter = counter + 1

    for i in range(counter):
        file = open(fileArrayNames[i])
        fileArrayInfo[i] = file.read()


    for i in range(counter):
        fileWrite = fileWrite + str(fileArrayInfo[i])
    fileWrite = fileWrite + "EOF"
    outputFile.write(fileWrite)

    