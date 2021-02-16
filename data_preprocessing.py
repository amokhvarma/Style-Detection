import json
import os
def read_input(dir_name,type = "train"):
    X,y_mult,y_changes = [],[],[]
    for file in os.listdir(dir_name):
        print("File : ", file)
        if( file[-4:] == ".txt" ):

            f = open(dir_name+file,"r")
            doc = f.read()
            para = doc.split("\n\n")
            # para = embed(para)
            X.append(para)
            if(type=="train"):
                try:
                    f_truth = open(dir_name+"truth-"+file[:-3]+"json")
                    doc = json.load(f_truth)
                    y_mult.append(int(doc["multi-author"]))
                    y_changes.append([int(x) for x in doc["changes"]])


                except:
                    print("Ground truth not found for : " , file)
                    X.pop()

    print("Total Documents : ", len(X),len(y_mult),len(y_changes),X[0],y_mult[0],y_changes[0])
    return (X,y_mult,y_changes)


path = "./train/dataset-wide/"
(X,y1,y2) = read_input(path,"train")