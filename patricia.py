#! /user/bin/env python3
import sys
import math
import pickle
import xml.etree.ElementTree as ET


def matching_prefix_index(word1, word2):
	max_len = min(len(word1),len(word2))
	for i in range(max_len):
		if word2[i] != word1[i]:
			return i
	return max_len

class PatriciaTrie(object):
	def __init__(self):
		self._storage = {}
		self._complete_prefix_flag = False
		self._dict = {}

	def _find_storage_key(self, word):
		for key in self._storage:
			prefix_index = matching_prefix_index(key, word)
			if prefix_index > 0:
				return (key, prefix_index)
		return (None, None)

	def add(self, word, id):
		if word == '':
			self._complete_prefix_flag = True
			if id in self._dict:
				self._dict[id] = self._dict[id] + 1
			else:	
				self._dict[id] = 1
			return True

		key, prefix_index = self._find_storage_key(word)
		if key is not None:
			if prefix_index == len(key):
				return self._storage[key].add(word[len(key):], id)
			else:
				new_tree = PatriciaTrie()
				new_tree._storage[key[prefix_index:]] = self._storage.pop(key)
				self._storage[key[0:prefix_index]] = new_tree
				return new_tree.add(word[prefix_index:], id)
		else:
			self._storage[word] = PatriciaTrie()
			self._storage[word].add('', id)
			return True

	def remove(self, word):
		if word == '':
			self._complete_prefix_flag = False
			self._dict = {}
			return True

		key, prefix_index = self._find_storage_key(word)
		if key is None or prefix_index != len(key):
			return False

		subword = word[prefix_index:]
		subtrie = self._storage[key]
		if subtrie.remove(subword):
			if (not subtrie._complete_prefix_flag) and len(subtrie._storage) == 0:
				self._storage.pop(key)
			return True
		else:
			return False

	def __contains__(self, word):
		if word == '':
			if self._complete_prefix_flag:
				return self._dict

		key, prefix_index = self._find_storage_key(word)
		if key is None or prefix_index != len(key):
			return False
		else:
			return (self._storage[key].__contains__(word[prefix_index:]))

	def has_prefix(self, word):
		if word == '':
			return True

		key, prefix_index = self._find_storage_key(word)
		if key is None:
			return False
		elif len(key) > len(word):
			return (prefix_index == len(word))
		elif len(key) != prefix_index:
			return False
		else:
			return self._storage[key].has_prefix(word[prefix_index:])
			
	def save_index(self,filename):
		t = open(filename,"wb")
		pickle.dump(self,t)


	
if __name__ == '__main__':		
	author_trie = PatriciaTrie()
	content_trie = PatriciaTrie()
	sample = []
	tree = ET.parse('patin.xml')
	root = tree.getroot()
	fo = open("doc_length.txt","w")
	flag = 0
	total_length = 0;
	for file in root.findall('file'):
		index = file.find('I').text
		author = file.find('A')
		if author is not None:
			if author.text is not None:
				a = author.text.split()	
				a = [x for x in a if(x!= '' and x!= '\n' )]
			if a is not None:
				for name in a:
					author_trie.add(name,index)
					content_trie.add(name,index)
		content = file.find('C')
		if content is not None:
			content = content.text.split()
			content = [x for x in content if(x!= '' and x!= '\n' )]
			fo.write(str(len(content))+"\n")
			total_length = total_length + len(content)
			flag = flag + 1
			for text in content:
				content_trie.add(text,index)
	fo.write(str(total_length/flag))
	fo.close()

	content_trie.save_index('contentdump.dat')
	author_trie.save_index('authordump.dat')
