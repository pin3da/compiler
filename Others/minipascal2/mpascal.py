import sys
import mpasgen
import mpasparse

if __name__ == "__main__":
	test = sys.argv[1]	
	f = open(test)
	s = f.read()
	result = mpasparse.parser.parse(s)
	if result:
		outf = open(test[:-4]+".out","w")		
		mpasgen.generate(outf,result)
		outf.close()	

