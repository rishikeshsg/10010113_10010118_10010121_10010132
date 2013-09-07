#!/usr/bin/python

import sys
import time
import math
import pickle
import operator
import collections
from patricia import PatriciaTrie
from tokenizer import tokenize_and_remove_stopword
from tokenizer import stopword
from stemming.porter2 import stem
stopword('stopwords.dat')
list_query = []
doc_list = []
doc_length = []
doc_final_score = {}
k1 = 1.9
b = 0.75


def process_query(query):
	raw_terms = query.split()
	num_terms = len(raw_terms)
	final_query = ""
	if num_terms > 0: 
		tokin = open("tokin.dat","w")
		tokin.write(query.lower())
		tokin.close()
		q_temp = tokenize_and_remove_stopword("tokin.dat")
		q_temp = q_temp.split()
		final_query = ""
		for qw in q_temp:
			final_query = final_query + stem(qw) + " "
	return final_query

def score_qd(doc_id,doc_len,avgdl,query,N):
	query_terms = query.split()
	n = len(query)
	score_dq = 0
	for q in query_terms:
		q_index = query_terms.index(q)
		fq = freq(doc_id, q_index) 
		nq = num_docs(q_index)
		f1 = (N-nq+0.5) / (nq+0.5)
		idfq = math.log(f1,10)
		doc_len = float(doc_len)
		score_dq = score_dq + idfq * ((fq*(k1+1)) / (fq + k1*(1-b+b*(doc_len/avgdl))))
	return (doc_id, score_dq)

def freq(doc_id, q_index):
	for id in list_query[q_index]:
		if(id):
			if(int(id[0]) == doc_id):
				return id[1]
	return 0
	
def num_docs(q_index):
	return (len(list_query[q_index]))


if __name__ == '__main__':
	init_time = time.time()
	author_trie = PatriciaTrie()
	content_trie = PatriciaTrie()
	author_trie = pickle.load(open('authordump.dat', 'rb'))
	content_trie = pickle.load(open('contentdump.dat', 'rb'))
	inStream = open("query.dat","r")
	fo = open("doc_length.txt","r")
	for lines in fo.readlines():
		doc_length.append(lines.split('\n')[0])
	avgdl= float(doc_length[-1])
	del doc_length[-1]
	total_documents = len(doc_length)
	counter = 1;
	fo.close()
	fo = open("output_results.txt","w")
	mid_time = time.time()
	const_time = mid_time - init_time
	while(1):
		init_time = time.time()
		line = inStream.readline()
		if (line == ''):
			break
		else:
			query = process_query(line)
			query_word = query.split()
		list_query = []
		doc_list = []
		doc_final_score = {}
		for words in query_word:
			list_word =  []
			document_arr = content_trie.__contains__(words)
			if document_arr:
				for index in document_arr:
					list_id = [index,document_arr[index]]
					list_word.append(list_id)
					if(index not in doc_list):
						doc_list.append(index)
				list_query.append(list_word)
			else:
				list_query.append([[]])
				continue;
		for doc_id in doc_list:
			doc_len = doc_length[int(doc_id)-1]
			id, score = score_qd(int(doc_id),doc_len,avgdl,query,total_documents)
			doc_final_score[id] = score
		doc_sorted = sorted(doc_final_score.items(), key=operator.itemgetter(1), reverse = True)
		fin_time = time.time()
		fo.write(str(len(doc_sorted))+" results found in "+str(fin_time - init_time + const_time)+" seconds\n")
		fo.write("------------------------------------------------------------------\n")
		for i in range(0,15) :
			fo.write(str(counter) + ' '+ str(doc_sorted[i][0])+'\n')
		counter = counter + 1
		fo.write("------------------------------------------------------------------\n")
		fo.write("------------------------------------------------------------------\n")
	fo.close()
	inStream.close()


