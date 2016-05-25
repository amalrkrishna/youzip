from __future__ import division
from itertools import islice
import time
import os
import pickle

code_dict = {}
encodelist = []
bitcount = 0

def frequncy(string):
	freq_dict = {}
	for i in string:
		if i in freq_dict.keys():
			freq_dict[i] = freq_dict[i] + 1
		else:
			freq_dict[i] = 1
	freq_list = freq_dict.items()
	freq_list = sorted(freq_list,key=lambda x:x[-1])
	return freq_list
	
def build_tr(freq_list):
	if freq_list.__len__() > 1:
		new_list = [((freq_list[0],freq_list[1]),freq_list[0][1] + freq_list[1][1])] + freq_list[2:]
		new_list = sorted(new_list,key=lambda x:x[-1])
	if new_list.__len__() > 1:
		prev = build_tr(new_list)
		return prev
	else:
		return new_list[0]
		
def trim(tuple_tr):
	if type(tuple_tr[0]) == type(""):
		return tuple_tr[0]
	else:
		return (trim(tuple_tr[0][0]),trim(tuple_tr[0][1]))
		
def give_codes(tuple_tr,path=""):
	global code_dict
	if type(tuple_tr) == type(""):
		code_dict[tuple_tr] = path
	else:
		give_codes(tuple_tr[0],path+'0')
		give_codes(tuple_tr[1],path+'1')
		
def new_encode(string):
	output = ''
	global bitcount
	global encodelist
	global code_dict
	for i in string:
		for j in code_dict[i]:
			if (bitcount % 8) == 0:
				newbyte = 0
				newbyte = newbyte | (int(j) << 7)
				encodelist.append(chr(newbyte))
				bitcount = bitcount + 1
			else:
				newbyte = encodelist[-1]
				newbyte = chr((ord(newbyte) | (int(j) << (7 - (bitcount % 8)))))
				encodelist[-1] = newbyte
				bitcount = bitcount + 1
	str = ''
	for i in encodelist:
		str = str + i
	return str
	
def decode_new(string,tr):
	output = '' 
	new_tr = tr
	for i in string:
		count = 0
		while True:
			if ((ord(i) & (1 << (7-count))) >> (7 - count) == 0):
				new_tr = new_tr[0]
			        count = count + 1
			else:
				count = count + 1
			        new_tr = new_tr[1]
			if type(new_tr) == type(""):
				output = output + new_tr
			        new_tr = tr
			if count % 8 == 0:
				count = 0
				break
	return output
	
def main():
	global code_dict
	while True:
		def compress ():
			inputc = raw_input("Input file name : ")
			outputc = raw_input("Output file name : ")
			
			start = time.clock()
			f1 = open(inputc,'r')
			input_str = f1.read()
			f1.close()
			freq_list = frequncy(input_str)
			tuple_tr = build_tr(freq_list)
			new_tuple_tr = trim(tuple_tr)
			with open('tree.dat','w') as f:
				pickle.dump(new_tuple_tr,f)
			give_codes(new_tuple_tr)
			k = []
			for i in input_str:
				k.append(i)
			output = new_encode(input_str)
			f2 = open(outputc,'a+')
			f2.write(output)
			f2.close()
			print "Time taken to Compress : " , time.clock() - start
			uncompressedSize = os.stat(inputc).st_size
			compressedSize = os.stat(outputc).st_size
			cr = compressedSize/uncompressedSize
			print 'Compression Ratio: %f'% (1-cr)
		
		def decompress ():
			inputd = raw_input("Input file name : ")
			outputd = raw_input("Output file name : ")
			
			start = time.clock()	
			f2 = open(inputd,'r')
			input_str = f2.read()
			with open('tree.dat','r') as f:
				new_tuple_tr = pickle.load(f)
			output = decode_new(input_str,new_tuple_tr)
			f2.close()
			
			f3 = open(outputd,'w')
			f3.write(output)
			f3.close()
			print "Time taken to Decompress : " , time.clock() - start
		
		def errhandler ():
			print "Error : Input a valid option"
			
		takeaction = {
		"1": compress,
		"2": decompress}

		choice = raw_input("Please enter your choice : \n1 : Compress\n2 : Decompress\nYour choice : ")
		takeaction.get(choice,errhandler)()
	
if __name__ == "__main__":
	main()
