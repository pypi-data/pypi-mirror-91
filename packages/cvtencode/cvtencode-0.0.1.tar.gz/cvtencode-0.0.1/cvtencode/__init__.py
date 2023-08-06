import os
import sys
import codecs
import chardet

list_folders = []
list_files = []
def list_folders_files(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_folders.append(file)
            list_folders_files(file_path)
        else:
            # if(file.find(".c", -2) != -1 or file.find(".h", -2) != -1):
            if(file.find(".html", -5) != -1):
                list_files.append(path+'\\'+file)
    return (list_folders, list_files)


def convert(file, in_enc="GBK", out_enc="UTF-8"):
    in_enc = in_enc.upper()
    out_enc = out_enc.upper()
    try:
        print("convert [ " + file.split('\\')[-1] + " ].....From " + in_enc + " --> " + out_enc )
        f = codecs.open(file, 'r', in_enc)
        new_content = f.read()
        codecs.open(file, 'w', out_enc).write(new_content)
    # print (f.read())
    except IOError as err:
        print("I/O error: {0}".format(err))



if __name__ == "__main__":
    path = r""
    (list_foldersx, list_filesx) = list_folders_files(path)
    print(list_foldersx)

    for fileName in list_filesx:
        # filePath = path + '\\' + fileName
        # print("Path: " + filePath)
        print("Path: " + fileName)
        with open(fileName, "rb") as f:
            data = f.read()
            codeType = chardet.detect(data)['encoding']
            print(codeType)
            convert(fileName, codeType, 'UTF-8-SIG')
