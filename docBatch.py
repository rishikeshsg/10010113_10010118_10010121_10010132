#! /usr/bin/python

# .I Identity
# .T Title
# .A Author
# .W Content
from xml.sax.saxutils import escape
fi = open("cacm.all", "r")
fo = open("cacm.xml", "w")
fo.write("<data>")
line = fi.readline()
while line:
	words = line.split()
	while words[0] == ".I":
		fo.write("<file>\n<index>" + words[1] + "</index>\n")
		line = fi.readline()
		words = line.split()
		if words[0] == ".T":
			fo.write("<Title>")
			line = fi.readline()
			if line:
				words = line.split()
			while words[0] != ".W" and words[0] != ".B":
				fo.write(escape(line))
				line = fi.readline()
				if line:
					words = line.split()
				else:
					break
			fo.write("</Title>\n")
		if words[0] == ".W":
			fo.write("<Content>")
			line = fi.readline()
			if line:
				words = line.split()
			while words[0] != ".B":
				fo.write(escape(line))
				line = fi.readline()
				if line:
					words = line.split()
				else:
					break
			fo.write("</Content>\n")
		if words[0] == ".B":
			line = fi.readline()
			fo.write("<B>" + escape(line) + "</B>\n")
		line = fi.readline()
		words = line.split()
		if words[0] == ".A":
			fo.write("<Author>")
			line = fi.readline()
			if line:
				words = line.split()
			while words[0] != ".N" and words[0] != ".K" and words[0] != ".C":
				fo.write(escape(line))
				line = fi.readline()
				if line:
					words = line.split()
				else:
					break
			fo.write("</Author>\n")
		fo.write("<N>")
		line = fi.readline()
		if line:
			fo.write(escape(line) + "</N>\n")
		line = fi.readline()
		words = line.split()
		if words[0] == ".X":
			fo.write("<X>")
			line = fi.readline()
			if line:
				words = line.split()
			while words[0] != ".I":
				fo.write(escape(line))
				line = fi.readline()
				if line:
					words = line.split()
				else:
					break
			fo.write("</X>\n")
		if words[0] == ".K":
			fo.write("<K>")
			line = fi.readline()
			if line:
				words = line.split()
			while words[0] != ".C" and words[0] != ".I":
				fo.write(escape(line))
				line = fi.readline()
				if line:
					words = line.split()
				else:
					break
			fo.write("</K>\n")
		if words[0] == ".C":
			fo.write("<C>")
			line = fi.readline()
			if line:
				words = line.split()
			while words[0] != ".I":
				fo.write(escape(line))
				line = fi.readline()
				if line:
					words = line.split()
				else:
					break
			fo.write("</C>\n")
		fo.write("</file>\n")
	line = fi.readline()
fo.write("</data>")
fi.close()
fo.close()