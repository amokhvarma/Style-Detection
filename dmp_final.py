import json
import os
import numpy as np
from bert_embedding import BertEmbedding
from sentence_transformers import SentenceTransformer as ST
from SplitIntoSentences import split_into_sentences

def diff(t1,t2):
    if(type(t1) != type(t2) or (type(t1) == list and len(t1) != len(t2))):
        print("Invalid op")
        return

    if(type(t1) == list):
        t = []
        for i in range(len(t1)):
            t.append(t1[i]-t2[i])
        return t
    else:
        return t1-t2


def process(all_para,changes,X,y,temp):
    # bert_embedding = BertEmbedding()
    s_model = ST('bert-base-nli-mean-tokens')
    y.extend(changes)
    y.append(1)
    result = []
    for text in all_para:
        sentences = split_into_sentences(text)
        se = s_model.encode(sentences)
        k = sum(se)/len(se)
        result.append(k)
    if (len(temp) != 0):
        X.append(diff(result[0], temp[len(temp)-1]))
    for i in range(1,len(result)):
        X.append(diff(result[i],result[i-1]))
    temp.append(result[len(result) - 1])
    # print(len(all_para),len(X),len(y))


def read_input(dir_name,type = "train"):
    X,y,changes = [], [], []
    temp = []
    count = 0
    file_count = len(os.listdir(dir_name))
    completed = 0
    for file in os.listdir(dir_name):
        print("File : ", file)
        if( file[-4:] == ".txt" ):

            f = open(dir_name+file,"r",encoding='utf-8')
            doc = f.read()
            para = doc.split("\n\n")
            count += len(para)

            if(type=="train"):
                try:
                    f_truth = open(dir_name + "truth-" + file[:-3] + "json")
                    doc = json.load(f_truth)
                    changes = [int(x) for x in doc["changes"]]
                    print(len(changes), len(para))
                    process(para, changes, X, y, temp)
                except:
                    print("Ground truth not found for : " , file)
                completed += 1
        print("Current :", completed + 1, "Total :", file_count / 2)
        print("Total Documents : ", count,len(X),len(y))
    # return (X,y)
path = "C:/Users/Ashish/Desktop/MTL782/Pan_20/train/dataset-wide/"
read_input(path)
# print(diff(2,[1,2]))