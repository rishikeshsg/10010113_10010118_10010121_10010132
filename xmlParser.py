import xml.etree.ElementTree as ET
from tokenizer import tokenize_and_remove_stopword
from tokenizer import stopword
from stemming.porter2 import stem
tree = ET.parse('cacm.xml')
root = tree.getroot()

fo = open("patin.xml","w")
stopword('stopwords.dat')
fo.write("<data>")
for file in root.findall('file'):
	tokin = open("tokin.dat", "w")
	index = file.find('index').text
	fo.write("<file>\n")
	fo.write("<I>"+index+"</I>\n")
	author = file.find('Author')
	if author is not None:
		fo.write("<A>")
		authin = open("authin.dat", "w")
		authin.write(author.text.lower())
		authin.close()
		tok = tokenize_and_remove_stopword('authin.dat')
		tok = tok.lower().split()
		for w in tok:
			fo.write(stem(w) + " ")
		fo.write("</A>\n")
	
	title = file.find('Title').text
	if title is not None:
		tokin.write(title)
	
	content = file.find('Content')
	if content is not None:
		tokin.write(content.text)
	tokin.close()
	tok = tokenize_and_remove_stopword('tokin.dat')
	fo.write("<C>")
	#fo.write(porter_stemming("stemin.dat") + "\n\n")
	tok = tok.lower().split()
	for w in tok:
		fo.write(stem(w) + " ")
	fo.write("\n\n</C>\n")
	fo.write("</file>\n")
fo.write("</data>")
fo.close()
