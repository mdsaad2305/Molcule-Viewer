CC = clang -Wall -pedantic -std=c99


all: _molecule.so

libmol.so: mol.o
	$(CC) -shared mol.o -o libmol.so -lm

mol.o: mol.c mol.h
	$(CC) -c -fPIC mol.c -o mol.o

molecule_wrap.o: swig3.0 molecule_wrap.c
	$(CC) -fPIC -I /usr/include/python3.7m -c molecule_wrap.c -o molecule_wrap.o

_molecule.so: libmol.so molecule_wrap.o
	$(CC) -dynamiclib -L. -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -shared molecule_wrap.o -o _molecule.so -lmol -lpython3.7m

swig3.0: molecule.i
	swig3.0 -python molecule.i

clean:
	rm *.o *.so
