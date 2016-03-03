#!/usr/bin/env python2.7
import scipy
import numpy

FILE1 = "QPSK_in"
FILE2 = "QPSK_out"
# to include a progress indicator
NUM_SPLITS = 10

# determine the average BER between file 1 and file 2
def main():
	print "opening files (this may take a while)..."
	# open with each bit as an element in a numpy array
	f1 = numpy.unpackbits(scipy.fromfile(open(FILE1), dtype="uint8"))
	f2 = numpy.unpackbits(scipy.fromfile(open(FILE2), dtype="uint8"))

	num_bits = len(f1)

# split these into a few arrays so that we can print a progress indicator 
	print "splitting arrays..."
	inputs = numpy.array_split(f1, NUM_SPLITS)
	outputs = numpy.array_split(f2, NUM_SPLITS)	

	errors = 0
	# determine BER for each second/pair of arrays
	for i in range(NUM_SPLITS):
		ins = inputs[i]
		outs = outputs[i]
		# count number that are the same
		errors += numpy.sum(ins != outs)
		print str((i+1) / float(NUM_SPLITS) * 100) + "%..."
	

	print "...done!"	
	
	print "total bits: " + str(num_bits)
	print "bit error ratio: " + str(errors) + "/" + str(num_bits) + " = " + str(errors/float(num_bits))

if __name__ == "__main__":
	main()
