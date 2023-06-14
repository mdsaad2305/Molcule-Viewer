import os
import sqlite3
from MolDisplay import Molecule

class Database:

	def __init__(self, reset=False):

		if reset is True:
			if os.path.exists('molecules.db'):
				os.remove('molecules.db') # remove table if it already exists

		self.conn = sqlite3.connect( 'molecules.db' ) # connect to table
		self.conn.isolation_level = None # for auto commit

	def create_tables( self ): # create all the tables
		self.conn.execute( """CREATE TABLE Elements
					( ELEMENT_NO INTEGER NOT NULL,
					ELEMENT_CODE VARCHAR(3) PRIMARY KEY NOT NULL,
					ELEMENT_NAME VARCHAR(32) NOT NULL,
					COLOUR1 CHAR(6) NOT NULL,
					COLOUR2 CHAR(6) NOT NULL,
					COLOUR3 CHAR(6) NOT NULL,
					RADIUS DECIMAL(3) NOT NULL);""" )

		self.conn.execute( """CREATE TABLE Atoms
					( ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					ELEMENT_CODE VARCHAR(3) NOT NULL,
					X DECIMAL(7,4) NOT NULL,
					Y DECIMAL(7,4) NOT NULL,
					Z DECIMAL(7,4) NOT NULL,
					FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements );""" )

		self.conn.execute( """CREATE TABLE Bonds
					( BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					A1 INTEGER NOT NULL,
					A2 INTEGER NOT NULL,
					EPAIRS INTEGER NOT NULL);""" )

		self.conn.execute( """CREATE TABLE Molecules
					( MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					NAME TEXT NOT NULL UNIQUE);""" )

		self.conn.execute( """CREATE TABLE MoleculeAtom
					( MOLECULE_ID INTEGER NOT NULL,
					ATOM_ID INTEGER NOT NULL,
					CONSTRAINT MA_PK PRIMARY KEY (MOLECULE_ID, ATOM_ID)
					FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
					FOREIGN KEY (ATOM_ID) REFERENCES Atoms);""" )

		self.conn.execute( """CREATE TABLE MoleculeBond
					( MOLECULE_ID INTEGER NOT NULL,
					BOND_ID INTEGER NOT NULL,
					CONSTRAINT MB_PK PRIMARY KEY (MOLECULE_ID,BOND_ID),
					FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
					FOREIGN KEY (BOND_ID) REFERENCES Bonds);""" )

	def __setitem__( self, table, values ):

		self.conn.execute(f"INSERT INTO {table} VALUES {values}")
		self.conn.commit()

	def add_atom( self, molname, atom ):

		element = atom.element
		x = atom.x
		y = atom.y
		z = atom.z
		molecule_id = self.conn.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME =?",(molname,)).fetchone()[0]
		self.conn.execute(f"""INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z)
					VALUES ('{element}','{x}','{y}','{z}');""")

		atom_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]


		self.conn.execute("""INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID)
					VALUES(?, ?);""", (molecule_id, atom_id))

	def add_bond( self, molname, bond ):

		a1 = bond.a1
		a2 = bond.a2
		epairs = bond.epairs

		molecule_id = self.conn.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME =?",(molname,)).fetchone()[0]

		self.conn.execute(f"""INSERT INTO Bonds (A1, A2, EPAIRS)
					VALUES('{a1}','{a2}','{epairs}');""")

		bond_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]


		self.conn.execute("""INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID)
					VALUES(?,?);""", (molecule_id, bond_id))

	def add_molecule( self, name, fp ):

		mol = Molecule()
		mol.parse(fp)

		self.conn.execute(f"""INSERT INTO Molecules (NAME)
					VALUES('{name}');""")

		i = 0
		j = 0

		while i < mol.atom_no:

			curr_atom = mol.get_atom(i)
			curr_element = curr_atom.element
			curr_x = curr_atom.x
			curr_y = curr_atom.y
			curr_z = curr_atom.z

			self.add_atom(name, curr_atom)

			i = i + 1

		while j < mol.bond_no:

			curr_bond = mol.get_bond(j)
			curr_a1 = curr_bond.a1
			curr_a2 = curr_bond.a2
			curr_epairs = curr_bond.epairs

			self.add_bond(name, curr_bond)

			j = j + 1


	def load_mol(self, name):

		mol1 = Molecule()

#		print( self.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );

		molecule_id = self.conn.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME =?",(name,)).fetchone()

		atom_query = f""" SELECT ELEMENT_CODE, X, Y, Z
				FROM Atoms
				INNER JOIN Molecules ON Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
				INNER JOIN MoleculeAtom ON MoleculeAtom.ATOM_ID = Atoms.ATOM_ID
				WHERE Molecules.NAME='{name}'"""

		my_atoms = self.conn.execute(atom_query).fetchall()
#		print(my_atoms)

		bond_query = f""" SELECT A1, A2, EPAIRS
                                FROM Bonds
                                INNER JOIN Molecules ON Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                                INNER JOIN MoleculeBond ON MoleculeBond.BOND_ID = Bonds.BOND_ID
                                WHERE Molecules.NAME='{name}'"""

		my_bonds = self.conn.execute(bond_query).fetchall()

#		print(len(my_bonds))
#		print(len(my_atoms))

#		print(self.conn.execute(" SELECT * FROM Atoms;" ).fetchall())
#		print(self.conn.execute(" SELECT * FROM Bonds;" ).fetchall())


#		molecule_id = self.conn.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME =?",(name,)).fetchone()[0]

#		print(molecule_id)

#		print( self.conn.execute(" SELECT * FROM MoleculeAtom WHERE MOLECULE_ID=?",(molecule_id,)).fetchall())

#		print(self.conn.execute("  SELECT * FROM MoleculeAtom WHERE MOLECULE_ID=?", (molecule_id,)).fetchall())

#		print( self.conn.execute( "SELECT * FROM Joint_Table;" ).fetchall() );

#		print(self.conn.execute("  SELECT * FROM JOINT_TABLE  WHERE MOLECULE_ID=?", (molecule_id,)).fetchall())

#		atom_count_var = self.conn.execute(" SELECT COUNT(*) FROM Atoms;" ).fetchall()

#		bond_count_var = self.conn.execute(" SELECT COUNT(*) FROM Bonds;" ).fetchall()

#		print(self.conn.execute(" SELECT * FROM JOINT_TABLE2;" ).fetchall())

#		atom_count = atom_count_var[0][0]

#		bond_count = bond_count_var[0][0]

		atom_count = len(my_atoms) # getting number of atoms

		bond_count = len(my_bonds) # getting number of bonds

#		print(my_atoms)

#		atom_code = self.conn.execute("SELECT ELEMENT_CODE, X, Y, Z FROM Atoms;").fetchall()

#		bond_code = self.conn.execute("SELECT A1, A2, EPAIRS FROM Bonds;").fetchall()

		atom_code = my_atoms # getting tuple of atoms

		bond_code = my_bonds # getting tuple of bonds

		i = 0

		j = 0

#		print(atom_code)
#		print(atom_code[0][1])

#		print(bond_code)
#		print(bond_code[0][1])

		while i < atom_count:

			mol1.append_atom(atom_code[i][0], atom_code[i][1], atom_code[i][2], atom_code[i][3])

			i = i + 1

		while j < bond_count:

			mol1.append_bond(bond_code[j][0], bond_code[j][1], bond_code[j][2])

			j = j + 1

		return mol1


#		print(mol1.atom_no)
#		print(mol1.bond_no)


	def radius( self ):

		dict = {}

		elmt_rad = self.conn.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements;").fetchall()

		elmt_rad_count = self.conn.execute("SELECT COUNT(*) FROM Elements;").fetchall()
#		print(elmt_rad_count)

		k = 0

		while k < elmt_rad_count[0][0]:

			dict[elmt_rad[k][0]] = elmt_rad[k][1]

			k = k + 1

		return dict


	def element_name( self ):

		dict2 = {}

		elmt_name = self.conn.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements;").fetchall()

		elmt_rad_count = self.conn.execute("SELECT COUNT(*) FROM Elements;").fetchall()

		l = 0

		while l < elmt_rad_count[0][0]:

			dict2[elmt_name[l][0]] = elmt_name[l][1]

			l = l + 1

		return dict2

	def radial_gradients( self ):

		string_elmts = self.conn.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements;").fetchall()

		elmt_rad_count = self.conn.execute("SELECT COUNT(*) FROM Elements;").fetchall()

		m = 0

		radialGradientSVG = ""

		while m < elmt_rad_count[0][0]:

			temp = f"""
				<radialGradient id='{string_elmts[m][0]}' cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
				<stop offset="0%" stop-color="{string_elmts[m][1]}"/>
				<stop offset="50%" stop-color="{string_elmts[m][2]}"/>
				<stop offset="100%" stop-color="{string_elmts[m][3]}"/>
				</radialGradient>"""

			radialGradientSVG = radialGradientSVG + temp

			m = m + 1

#		print(radialGradientSVG)

		return radialGradientSVG

	def delete_element(self, element_no):
		self.conn.execute("DELETE FROM Elements WHERE ELEMENT_NO=?",(element_no,))
		self.conn.commit()

