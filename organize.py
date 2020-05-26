import os
import sys
import hashlib


# Creates folders for different file types
def makeFolders(downloadDirectory, fileTypes):
    for fileType in fileTypes.keys():
        directory = downloadDirectory + "\\" + fileType

        if not os.path.exists(directory):
            os.mkdir(directory)


# Moves file to its proper folder and delete any duplicates
def moveFile(moveFile, downloadDirectory, fileTypes):
    # The file format is what is after the period in the file name
    if "." in moveFile:
        temp = moveFile.split(".")
        fileFormat = temp[-1]
    else:
        return

    for fileType in fileTypes.keys():
        if fileFormat in fileTypes[fileType]:
            srcPath = downloadDirectory + "\\" + moveFile
            dstPath = downloadDirectory + "\\" + fileType + "\\" + moveFile

            # If the file doesn't have a duplicate in the new folder, move it
            if not os.path.isfile(dstPath):
                os.rename(srcPath, dstPath)
            # If the file already exists with that name and has the same md5 sum
            elif os.path.isfile(dstPath) and \
                    checkSum(srcPath) == checkSum(dstPath):
                os.remove(srcPath)
                print
                var = "removed " + srcPath
            return


# Get md5 checksum of a file. Chunk size is how much of the file to read at a time.
def checkSum(fileDir, chunkSize=8192):
    md5 = hashlib.md5()
    f = open(fileDir)
    while True:
        chunk = f.read(chunkSize)
        # If the chunk is empty, reached end of file so stop
        if not chunk:
            break
        md5.update(chunk)
    f.close()
    return md5.hexdigest()


def main():
    # Dictionary contains file types as keys and lists of their corresponding file formats
    fileTypes = {"Images": ["jpg", "gif", "png", "jpeg", "bmp", "jpg", "JPG"], 
                 "Audio": ["mp3", "wav", "aiff", "flac", "aac", "mid"],
                 "Video": ["m4v", "flv", "mpeg", "mov", "mpg", "mpe", "wmv", "MOV", "mp4"],
                 "Documents": ["doc", "docx", "txt", "ppt", "pptx", "pdf", "rtf", "csv", "html", "xlsx"], 
                 "Installer": ["exe","msi"],
                 "Compressed": ["zip", "tar", "7", "rar","gz"], 
                 "Virtual Machines and ISO Images": ["vmdk", "ova", "iso"],
                 "Log Files": ["dat", "log"],
                 "SVG": ["svg"],
                 "JSON":["json"],
                 "Outlook":["msg"]}

    # The second command line argument is the download directory
    downloadDirectory = sys.argv[1]
    downloadFiles = os.listdir(downloadDirectory)
    makeFolders(downloadDirectory, fileTypes)

    for filename in downloadFiles:
        moveFile(filename, downloadDirectory, fileTypes)


main()
