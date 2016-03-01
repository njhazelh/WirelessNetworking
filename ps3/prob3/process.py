#!/usr/bin/env python2.7
import scipy
import numpy

FILE1 = "BPSK_in"
FILE2 = "BPSK_out"
# in seconds
TIME_RUN = 5

# determine the average BER between file 1 and file 2
def main():
	print "opening files..."
	# create numpy data type for a binary file
	dt = numpy.dtype('b1')

	# open with each bit as an element in a numpy array
	# (if you print these, they're an array of bool)
	f1 = scipy.fromfile(open(FILE1), dtype=dt)
	f2 = scipy.fromfile(open(FILE2), dtype=dt)

	# split these into arrays of bits, one per second
	print "splitting arrays..."
	inputs = numpy.array_split(f1, TIME_RUN)
	outputs = numpy.array_split(f2, TIME_RUN)	

	errors = 0
	# determine BER for each second/pair of arrays
	for i in range(TIME_RUN):
		print "processing second " + str(i) + " of " + str(TIME_RUN) + "..."
		ins = inputs[i]
		outs = outputs[i]
		num_bits = len(ins)
		# count number that are the same
		errors += numpy.sum(ins != outs)

	print "...done!"	
	BPS = len(f1) / TIME_RUN
	BER = errors / TIME_RUN
	print "Bits per second:" + str(BPS)
	print "Bit errors per second: " + str(BER)

if __name__ == "__main__":
	main()
