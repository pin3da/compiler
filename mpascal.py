import sys
import os.path
import mpasparse
import mpasgen
import semantic
from errors import subscribe_errors, errors_reported

if __name__ == '__main__':
    
    filename = sys.argv[1]
    outname = os.path.splitext(filename)[0] + ".s"
    parser  =  mpasparse.make_parser() 
    
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        # Revise el programa
        num_errors = semantic.check_program(program)
        # Si no ocurren errores, genere codigo
        if num_errors == 0:
            outf = open(outname,"w")
            mpasgen.generate(outf,program)
            outf.close()
        else:
            sys.stderr.write("Program couldn't be compiled\n")
