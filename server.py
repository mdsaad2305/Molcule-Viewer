from http.server import HTTPServer, BaseHTTPRequestHandler;

import sys
import urllib
from molsql import Database
import io
import MolDisplay
import json



public_files = [ '/index.html', '/add.html', '/sdf.html', '/select.html', '/style.css', '/script.js', '/retrieve.js' ];

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):

        if self.path in public_files: 
            self.send_response( 200 ); 
            if self.path == '/style.css':
                self.send_header( "Content-type", "text/css")
            #elif self.path == '/molecules.png':
             #   self.send_header( "Content-type", "image/png")
            else:
                self.send_header( "Content-type", "text/html" )

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read()
            fp.close()

            # create and send headers
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) )
	
        elif self.path == "/select_molecule":
            
            data = db.conn.execute( "SELECT NAME FROM Molecules;" ).fetchall()
            mol_list = []
            print(len(molecule_list))
            for i in range(len(molecule_list)):
                row = []
                row.append(data[i][0])
                row.append(molecule_list[i].atom_no)
                row.append(molecule_list[i].bond_no)
                mol_list.append(row)
            
            print(mol_list)
#            content = json.dumps(data)
            content = json.dumps(mol_list)
            self.send_response( 200 )
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            

        else:
            # if the requested URL is not one of the public_files
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )



    def do_POST(self):

        if self.path == "/add":
            # code to handle sdf_upload

            my_content = int(self.headers['content-length'])
            post_data = self.rfile.read(my_content)

            params = urllib.parse.parse_qs(post_data.decode('utf-8')) # decoding to get dictionary

            element_name =  params.get('element_name')[0] # getting element name

            element_no =  params.get('element_no')[0] # getting element number

            element_code =  params.get('element_code')[0] # getting element code

            colour_one =  params.get('colour1')[0] # getting 1st colour

            colour_two =  params.get('colour2')[0] # getting 2nd colour

            colour_three =  params.get('colour3')[0] # getting 3rd colour

            radius =  params.get('radius')[0] # getting radius

            # adding element to the Elements table

            db['Elements'] = (int(element_no), element_code, element_name, colour_one, colour_two, colour_three, radius) 

            self.send_response( 200 ); # response is good

            self.end_headers() # ending headers
        elif self.path == "/remove":
            my_content = int(self.headers['content-length'])

            post_data = self.rfile.read(my_content)

            params = urllib.parse.parse_qs(post_data.decode('utf-8')) # decoding the dictionary

            #print(params)

            element_no =  params.get('element_no')[0]            

            db.delete_element(element_no) # removing element

            self.send_response( 200 );

            self.end_headers()
        elif self.path == "/sdf":
            molecule = MolDisplay.Molecule()
            my_content = int(self.headers['content-length'])
            post_data = self.rfile.read(my_content)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            file_content =  params.get(' filename', [''])[0] 
            file_name =  params.get(' name', [''])[0] 
            my_file = io.StringIO(file_content)
            #print(file_content)
            #print(file_name)
            #print(params)
            for i in range(3):
                trash = my_file.readline() # skipping 4 lines
                #print(trash)
            db.add_molecule(file_name, my_file)
            my_file.seek(0) # rewinding the file pointer to the start of the file
            for i in range(3):
                trash = my_file.readline()
            molecule.parse(my_file) # parsing the file to get the single molecule
            molecule_list.append(molecule) # adding molecule to the list
            #print(molecule.atom_no)
            self.send_response( 200 )
            self.end_headers()
        elif self.path == "/option_selected":
            MolDisplay.radius = db.radius() # getting a dictionary containing radius of all elements in the table
            MolDisplay.element_name = db.element_name() # getting a dictionary containing element code and element names
            MolDisplay.header += db.radial_gradients()
            my_content = int(self.headers['content-length'])
            post_data = self.rfile.read(my_content)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            print(params)
            mol_name = params.get('molecule', [''])[0]
            display_mol = MolDisplay.Molecule()
            display_mol = db.load_mol(mol_name)
            display_mol.sort()
            #print(display_mol.atom_no)
            print(display_mol.svg())

            self.send_response(200)
            self.end_headers()
            self.wfile.write(display_mol.svg().encode('utf-8'))




        else:
            print(self.path)
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )






httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )

db = Database(reset=True)

db.create_tables()

#molecule = MolDisplay.Molecule()

molecule_list = []

httpd.serve_forever()