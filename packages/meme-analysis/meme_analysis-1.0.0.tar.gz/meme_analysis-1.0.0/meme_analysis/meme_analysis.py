# -*- coding: utf-8 -*-

import torchtext.vocab as vocab
import math
import numpy as np
import re
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import argparse
import logging
import os
import scipy

def reading(corpus_data_dir):
    with open(corpus_data_dir, "r") as fin:
        return fin.read()
def sentence_tokenize(raw_text):
    filters =  "\\【.*?】+|\\《.*?》+|\\#.*?#+|[/_$&%^*()<>+""'@|:~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]"
    raw_sentence = raw_text
    cleanr = re.compile('<.*?>|[\\r]|[\\n]')
    raw_sentence = re.sub(cleanr, ' ', raw_sentence)
    raw_sentence = re.sub(filters,'',raw_sentence)
    return re.split("\.|,|!|\?|\"", raw_sentence)
def sentenceIndexList(word,word_to_index,sentence_matrix):
    sentence_index_list = []
    for i,sentence_vector in enumerate(sentence_matrix):
        if word in sentence_vector:
            sentence_index_list.append(i)
    return sentence_index_list
def norm_vector(raw_vector):
    norm_vector = []
    for eigenvalues in raw_vector:
        weight = eigenvalues / sum(raw_vector)
        norm_vector.append(weight)
    return norm_vector
def norm_matrix(matrix):
    row_max = matrix.max(axis=1)
    row_max = row_max.reshape(-1, 1)
    matrix = matrix - row_max
    norm_matrix = []
    for vector in matrix:
        norm_vector = []
        for eigenvalues in vector:
            x = eigenvalues / sum(vector)
            norm_vector.append(x)
        norm_matrix.append(norm_vector)
    return norm_matrix
def cos_similarity(x, y, norm=False):
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
    return 0.5 * cos + 0.5 if norm else cos
def remove_list(iterable: list, target: list):
        return [n for n in iterable if n not in target]
def transformMatrix(m):
    return list(zip(*m))
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def evalue_clustering(sentence_index_to_lable,sentence_matrix,sentence_index_list,k):
    for i in np.arange(k):
        print("Label:",sentence_index_to_lable[i]," | "," ".join(sentence_matrix[sentence_index_list[i]]))
def find_nearest_word(word,word_to_idx,embedding_weights):
    index = word_to_idx[word]
    embedding = embedding_weights[index]
    cos_dis = np.array([scipy.spatial.distance.cosine(e, embedding) for e in embedding_weights])
    return [idx_to_word[i] for i in cos_dis.argsort()[:10]]
def find_nearest_vec(vector,embedding_weights,idx_to_word):
    cos_dis = np.array([scipy.spatial.distance.cosine(e, vector) for e in embedding_weights])
    return [idx_to_word[i] for i in cos_dis.argsort()[:10]]

# cache_dir : per-train data save（cache_dir = "./data"）
# dimension : per-train data word embedding dimension (dimension = 50 or 100 or 200 or 300)
# corpus_data_dir : Corpus for training morphemes (corpus_data = path of wikipedia_english)
def text_preprocessing(cache_dir:str,
                    dimension:int,
                    corpus_data_dir:str
                   ):
    print("---sememe analysis start---")
    glove = vocab.pretrained_aliases["glove.6B."+str(dimension)+"d"](cache=cache_dir)
    print("number of vocabularies : ",len(glove.stoi))
    raw_text = reading(corpus_data_dir)
    print("corpus data preprocessing...")
    sentence = [w for w in sentence_tokenize(raw_text)]
    print("making sentence matrix...")
    sentence_matrix = [[lower_word for lower_word in w.lower().split()] for w in sentence]
    sentence_embedding_matrix = [[glove.stoi.get(word, "NON") for word in words]for words in sentence_matrix]
    sentence_embedding_matrix = [[i for i in sen if i != "NON"] for sen in sentence_embedding_matrix ]
    sentence_embedding_matrix = [sen for sen in sentence_embedding_matrix if len(sen)!=1 and len(sen)!=0]
    sentence_matrix = [[glove.itos[i] for i in sen_i] for sen_i in sentence_embedding_matrix]
    print("saved : model,sentence matrix and sentence embedding matrix")
    return glove,sentence_matrix,sentence_embedding_matrix

# word_str : one word (word_str = "apple")
# word_to_index : word to index (word_to_index = glove.stoi)
# index_to_vec : index to vector (index_to_vec = glove.vectors)
# sentence_embedding_matrix : from _, _, * = text_preprocessing()
# sentence_matrix : from _, * _, = text_preprocessing()
# num_clusters : number of sememe
# dimensionality_reduction : Whether to perform dimensionality reduction analysis
def word_sememe_analysis(word:str,
                         word_to_index,
                         index_to_word,
                         index_to_vec,
                         sentence_embedding_matrix,
                         sentence_matrix,
                         num_clusters:int,
                         dimensionality_reduction:bool
                        ):
    word_sememe_matrix = []
    center_vector = index_to_vec[word_to_index[word]]
    sentence_index_list = sentenceIndexList(word,word_to_index,sentence_matrix)
    print("------------------------")
    print("Calculating morpheme matrix...")
    for index in sentence_index_list:
        context_indices = remove_list(sentence_embedding_matrix[index],[word_to_index[word]])
        #context_indices = remove_list(context_indices,["NON"])
        if context_indices == []:
            print("context_indices == []")
        context_vec = [index_to_vec[i] for i in context_indices]
        weight_list = [cos_similarity(i,center_vector) for i in context_vec]
        if weight_list == []:
            print("weight_list == []")
        # len(weight_list)==len(context_vec)
        if len(weight_list) != len(context_vec):
            print("error : len(weight_list) != len(context_vec)")
        #if len(context_vec) == 1:
            #print("error : context_vec == 1 ; context_vec : ",[glove.itos[i] for i in context_indices])
        norm_weight_list = norm_vector(weight_list)
        weight_vector = np.multiply(np.array(norm_weight_list),np.array(transformMatrix(context_vec)))
        # len(weight_vector) == len(transformMatrix(context_vec))
        if len(weight_vector) != len(transformMatrix(context_vec)):
            print("error : len(weight_vector) != len(transformMatrix(context_vec))")
        relation_vector = [math.atan(sum(w)) for w in weight_vector]
        # len(relation_vector) == len(weight_vector)
        if len(relation_vector) != len(weight_vector):
            print("error : len(relation_vector) == len(weight_vector)")
        if relation_vector == []:
            print("error : relation_vector == [] | relation_vector: ",[glove.itos[i] for i in context_indices])
        word_sememe_matrix.append(relation_vector)
    print("------------------------")
    print("The morpheme matrix is completed!")
    print("------------------------")
    print("Trying to cluster the morpheme matrix...")
    print("------------------------")
    clustering = KMeans(num_clusters).fit(word_sememe_matrix)
    sentence_index_to_lable = clustering.labels_
    print("Text classification on morphemes <Top10>...")
    evalue_clustering(sentence_index_to_lable,sentence_matrix,sentence_index_list,10)
    print("------------------------")
    if dimensionality_reduction:
        print("The cluster distribution scatter plot is being produced...")
        tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000, method='exact')
        low_dim_embs = tsne.fit_transform(word_sememe_matrix)
        centers_low_dim_embs = tsne.fit_transform(clustering.cluster_centers_)
        plt.scatter(low_dim_embs[:, 0], low_dim_embs[:, 1], c=sentence_index_to_lable,s=50, cmap='viridis')
    print("------------------------")
    print("The classifier is being used to evaluate the clustering results...")
    x_train, x_test, y_train, y_test = train_test_split(word_sememe_matrix, sentence_index_to_lable, random_state=1, train_size=0.7)
    clf = make_pipeline(StandardScaler(), SVC(kernel='linear',gamma='auto'))
    clf.fit(x_train, y_train.ravel())
    print("Train score:",clf.score(x_train, y_train))
    print("Test score:",clf.score(x_test, y_test))
    print("------------------------")
    print("Find the word that is closest to the sum of phonemes...")
    sememe_sum = find_nearest_vec(sum(clustering.cluster_centers_),index_to_vec,index_to_word)
    print(sememe_sum)
    print("------------------------")
    for sememe_i in clustering.cluster_centers_:
        sememe_nearest = find_nearest_vec(sememe_i,index_to_vec,index_to_word)
        print("The closest word of the phoneme of the",word,":\n",sememe_nearest)
    print("------------------------End------------------------")
    
    
def get_args():
    parser = argparse.ArgumentParser(description='Train embedding')
    parser.add_argument('--pertrain_data_dir', type=str, default="./data", help='cache_dir : per-train data save（cache_dir = "./data"）')
    parser.add_argument('--dimension', type=int, default=50, help='per-train data word embedding dimension (dimension = 50 or 100 or 200 or 300)')
    parser.add_argument('--corpus_data_dir', type=str, required=True, help='Corpus for training morphemes (corpus_data = path of wikipedia_english)')
    parser.add_argument('--word', type=str,default="apple", help='embedding size')
    parser.add_argument('--num_clusters', type=int,default=2, help='number of sememe')
    parser.add_argument('--dimensionality_reduction', type=bool,default=False, help='Whether to perform dimensionality reduction analysis')

    return parser.parse_args()
    

def main():
    args = get_args()
    dirs = './data'
    if not os.path.exists(dirs):
       os.makedirs(dirs)
    glove,sentence_matrix,sentence_embedding_matrix = text_preprocessing(cache_dir=args.pertrain_data_dir,
                                                                         dimension=args.dimension,
                                                                         corpus_data_dir=args.corpus_data_dir)
    
    word_sememe_analysis(word=args.word,
                         word_to_index=glove.stoi,
                         index_to_word=glove.itos,
                         index_to_vec=glove.vectors,
                         sentence_embedding_matrix=sentence_embedding_matrix,
                         sentence_matrix=sentence_matrix,
                         num_clusters=args.num_clusters,
                         dimensionality_reduction=args.dimensionality_reduction
                        )
if __name__ == '__main__':
    main()
    