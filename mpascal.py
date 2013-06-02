import sys
import os.path
import mpasparse
import mpasgen



if __name__ == '__main__':
    
    filename = sys.argv[1]
    outname = os.path.splitext(filename)[0] + ".s"

    f = open(filename)
    data = f.read()
    f.close()
    parser  =  mpasparse.make_parser() 
    top = parser.parse(data)
    if top:
        outf = open(outname,"w")
        mpasgen.generate(outf,top)
        outf.close()
