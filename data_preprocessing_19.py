import json
import os
import numpy
def breaker(all_para,switches,X):
    char_count = -1
    switch = 0
    y_changes_temp = []
    for text in all_para:
        char_count += 1
        words = text.split(' ')
        if(len(words) >= 10):
            new_author = 0
            X.append(text)
            while (switch < len(switches) and switches[switch] <= char_count + len(text)):
                new_author = 1
                switch += 1
            y_changes_temp.append(new_author)
        char_count += len(text)

    return y_changes_temp[1:len(y_changes_temp)]


def process(dir_name,type = "train"):
    X, y_mult, y_changes = [], [], []
    for file in os.listdir(dir_name):
        print("File : ", file)
        if( file[-4:] == ".txt" ):
            try:
                f = open(path+file, "r", encoding='utf-8')
                doc = f.read()
                all_para = doc.split("\n")

                f_truth = open(dir_name + file[:-3] + "truth")
                doc = json.load(f_truth)

                switches = [int(x) for x in doc["switches"]]
                y_changes.extend(breaker(all_para, switches, X))

                authors = numpy.unique(numpy.array(doc["structure"]))
                y_mult.append(len(authors))
            except:
                print("Ground truth not found for : ", file)

    print("Total Paragraphs : ", len(X),len(y_mult),len(y_changes))
    print(X[0])
    print(y_mult[0])
    print(y_changes[0])
    return (X,y_mult,y_changes)

path = "./Pan_19/train/"
process(path,"train")