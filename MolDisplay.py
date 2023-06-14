from molecule import atom
from molecule import bond
from molecule import bondget
from molecule import bondset
from molecule import molecule


header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""

offsetx = 500
offsety = 500


class Atom:
	def __init__(self, c_atom):
		self.atom = c_atom # getting atom value
		self.z = c_atom.z # getting z value


	def __str__(self):
		return "element = " + self.atom.element + "\nx = " + str(self.atom.x) + "\ny = " + str(self.atom.y) + "\nz = " + str(self.atom.z)

	def svg(self):

		x_coord = (self.atom.x * 100) + offsetx
		y_coord = (self.atom.y * 100) + offsety

		svg_string = ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' %(x_coord, y_coord, radius[self.atom.element], element_name[self.atom.element])

		return svg_string

class Bond:
	def __init__(self, c_bond):
		self.bond = c_bond # getting bond value
		self.z = c_bond.z # getting z value

	def __str__(self):
		bond_string = "a1 = " + str(self.bond.a1) + "\na2 = " + str(self.bond.a2) + "\nepairs = " + str(self.bond.epairs) + "\nx1 = " + str(self.bond.x1) + "\nx2 = " + str(self.bond.x2) + "\ny1 = " + str(self.bond.y1) + "\ny2 = " + str(self.bond.y2) + "\nz = " + str(self.z) + "\nlen = " + str(self.bond.len) + "\ndx = " + str(self.bond.dx) + "\ndy = " + str(self.bond.dy)
		return bond_string

	def svg(self):
		index1 = self.bond.a1 # index for a1
		index2 = self.bond.a1 # index for a2

		x1_centre = (self.bond.x1 * 100) + offsetx #x coordinate of circle 1
		y1_centre = (self.bond.y1 * 100) + offsety #y coordinate of circle 1

		x2_centre = (self.bond.x2 * 100) + offsetx #x coordinate of circle 2
		y2_centre = (self.bond.y2 * 100) + offsety #y coordinate of circle 2

		a1_lower_corner_x = x1_centre + (self.bond.dy * 10) # x coordinate for corner 1
		a1_lower_corner_y = y1_centre + (self.bond.dx * 10) # y coordinate for corner 1
		a1_upper_corner_x = x1_centre - (self.bond.dy * 10) # x coordinate for corner 2
		a1_upper_corner_y = y1_centre - (self.bond.dx * 10) # y coordinate for corner 2

		a2_lower_corner_x = x2_centre + (self.bond.dy * 10) # x coordinate for corner 3
		a2_lower_corner_y = y2_centre + (self.bond.dx * 10) # y coordinate for corner 3
		a2_upper_corner_x = x2_centre - (self.bond.dy * 10) # x coordinate for corner 4
		a2_upper_corner_y = y2_centre - (self.bond.dx * 10) # y coordinate for corner 4

		bond_svg_string = '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' %(a1_upper_corner_x, a1_lower_corner_y, a1_lower_corner_x, a1_upper_corner_y, a2_lower_corner_x, a2_upper_corner_y, a2_upper_corner_x, a2_lower_corner_y)

		return bond_svg_string


class Molecule(molecule):

	def __str__(self):
		molecule_string = "atom no. = " + self.atom_no + "\nbond no. = " + self.bond_no
		return molecule_string

	def svg(self):

		atoms = 0
		bonds = 0
		svg_string = "" # empty string to fill all relevant info in
		svg_string = svg_string + header # putting header into the string

		while atoms < self.atom_no and bonds < self.bond_no: # final pass of merge sort
			if self.get_atom(atoms).z < self.get_bond(bonds).z:
				svg_string = svg_string + str(Atom(self.get_atom(atoms)).svg())
				atoms = atoms + 1
			else:
				svg_string = svg_string + str(Bond(self.get_bond(bonds)).svg())
				bonds = bonds + 1

		while atoms < self.atom_no:
			svg_string = svg_string + str(Atom(self.get_atom(atoms)).svg())
			atoms = atoms + 1


		while bonds < self.bond_no:
			svg_string = svg_string + str(Bond(self.get_bond(bonds)).svg())
			bonds = bonds + 1


		svg_string = svg_string + footer # adding footer into the string

		return svg_string # returning the filled string

	def parse(self, obj):
		file_content = obj.readlines()

		atom_str = file_content[3][1] + file_content[3][2]
		atom_num = int(atom_str)

		bond_str = file_content[3][4] + file_content[3][5]
		bond_num = int(bond_str)

		num_atom_file = atom_num + 4

		i = 4

		while i < num_atom_file:
			x_coord = file_content[i][3] + file_content[i][4] + file_content[i][5] + file_content[i][6] + file_content[i][7] + file_content[i][8] + file_content[i][9]
			x_num = float(x_coord)
			y_coord = file_content[i][13] + file_content[i][14] + file_content[i][15] + file_content[i][16] + file_content[i][17] + file_content[i][18] + file_content[i][19]
			y_num = float(y_coord)
			z_coord = file_content[i][23] + file_content[i][24] + file_content[i][25] + file_content[i][26] + file_content[i][27] + file_content[i][28] + file_content[i][29]
			z_num = float(z_coord)
			element = file_content[i][31]

			self.append_atom(element, x_num, y_num, z_num)

		#	print(str(x_num) + " " + str(y_num) + " " + str(z_num) + " " + element)
			i = i + 1

			#incrementing to start reading bonds

		num_bond_file = bond_num + i

		while i < num_bond_file:
			a1_str = file_content[i][1] + file_content[i][2]
			a1 = int(a1_str) -1 # removed decrement (-1)
			a2_str = file_content[i][4] + file_content[i][5]
			a2 = int(a2_str) -1 # removed decrement (-1)
			epair_str = file_content[i][7] + file_content[i][8]
			epair = int(epair_str)

			self.append_bond(a1, a2, epair)

		#	print(str(a1) + " " + str(a2) + " " + str(epair))

			i = i + 1
