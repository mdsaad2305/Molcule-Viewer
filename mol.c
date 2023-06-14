#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "mol.h"

/*This function sets the values in the atom*/
void atomset( atom *atom, char element[3], double *x, double *y, double *z ){
    atom->x = *x; // copying the x value into atom
    atom->y = *y; // copying the y value into atom
    atom->z = *z; // copying the z value into atom
    strcpy(atom->element, element); // copying the string into atom
}

/*This function retrieves the values in the given atom*/
void atomget( atom *atom, char element[3], double *x, double *y, double *z ){
    *x = atom->x; // copying the x value from atom
    *y = atom->y; // copying the y value from atom
    *z = atom->z; // copying the z value from atom
    strcpy(element, atom->element); // copying the string from atom
}


// this function computes the values of all the variables contained inside the bond
void compute_coords( bond *bond ){

    double z1, z2;

    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;
    z1 = bond->atoms[bond->a1].z;
    z2 = bond->atoms[bond->a2].z;
    bond->z = (z1+z2)/2.0;

    double xDiff = bond->x1 - bond->x2;
    double yDiff = bond->y1 - bond->y2;
//    double zDiff = z1 - z2;

    bond->len = sqrt((xDiff*xDiff) + (yDiff*yDiff));

    bond->dx = (bond->x2 - bond->x1)/ bond->len;
    bond->dy = (bond->y2 - bond->y1)/ bond->len;
}


/*This function sets the values in the bond*/
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom
**atoms, unsigned char *epairs ){

    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs; // copying the number of electron pairs between the atoms into the bond

    bond->atoms = *atoms;

    compute_coords(bond);

}

/*This function retrieves the values from the given bond*/
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom
**atoms, unsigned char *epairs ){

    *a1 = bond->a1; // copying the first atom from the give bond
    *a2 = bond->a2; // copying the second atom from the given bond
    *epairs = bond->epairs; // copying the number of electron pairs between the atoms from the given bond

    *atoms = bond->atoms;
}

/*This function returns the address of an area large enough to hold a molecule*/
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){

    molecule * molptr = malloc(sizeof(molecule)); // allocating space for new molecule

    molptr->atom_max = atom_max; // assigning value for atom_max
    molptr->atom_no = 0; // assigning atom_no value to 0 since there are no atoms yet
    molptr->atoms = malloc(sizeof(atom)*atom_max); // allocating space for atom_max number of atoms
    molptr->atom_ptrs = malloc(sizeof(atom*)*atom_max); // allocating space for atom_max number of atom pointers
    for(int i = 0; i < atom_max; i++){
        molptr->atom_ptrs[i] = NULL; // initializing all atom pointers to NULL
    }

    molptr->bond_max = bond_max; // assigning value for bond_max
    molptr->bond_no = 0; // assigning value for bond max nu
    molptr->bonds = malloc(sizeof(bond)*bond_max); // allocating enough space for bonds
    molptr->bond_ptrs = malloc(sizeof(bond*)*bond_max); // allocating enough space for bond pointers
    for(int j = 0; j < bond_max; j++){
        molptr->bond_ptrs[j] = NULL; // initializing all pointers to NULL
    }

    return molptr; // returning the molecule pointer
}


/*This function copies the molecule given in the argument and returns the address of the copy*/
molecule *molcopy(molecule *src) {

    molecule *molptr = molmalloc(src->atom_max, src->bond_max);

    molptr->atom_no = src->atom_no; // copying the atom number
    molptr->bond_no = src->bond_no; // copying the bond number

    for(int k = 0; k < src->atom_no; k++){
        molptr->atoms[k].x = src->atoms[k].x;
        molptr->atoms[k].y = src->atoms[k].y;
        molptr->atoms[k].z = src->atoms[k].z;
        strcpy(molptr->atoms[k].element, src->atoms[k].element);
    }

    for(int k = 0; k < src->bond_no; k++){
        molptr->bonds[k].a1  = src->bonds[k].a1;
        molptr->bonds[k].a2  = src->bonds[k].a2;
        molptr->bonds[k].epairs = src->bonds[k].epairs;

        molptr->bonds[k].atoms = malloc(sizeof(atom)*molptr->atom_max);
        molptr->bonds[k].atoms = molptr->atoms;
       
       // molptr->bonds[k].atoms = src->bonds[k].atoms;
//        memcpy(molptr->bonds[k].atoms, src->bonds[k].atoms, sizeof(atom)*4000);
        molptr->bonds[k].x1 = src->bonds[k].x1;
        molptr->bonds[k].x2 = src->bonds[k].x2;
        molptr->bonds[k].y1 = src->bonds[k].y1;
        molptr->bonds[k].y2 = src->bonds[k].y2;
        molptr->bonds[k].len = src->bonds[k].len;
        molptr->bonds[k].dx = src->bonds[k].dx;
        molptr->bonds[k].dy = src->bonds[k].dy;

    }

    int i = 0;
    int j = 0;

    while(i < src->atom_max){
        molptr->atom_ptrs[i] = &(molptr->atoms[i]); // pointers to atoms
        i++;
    }

    while(j < src->bond_max){
        molptr->bond_ptrs[j] = &(molptr->bonds[j]); // pointers to bonds
        j++;
    }


    return molptr; // returning copied molecule address
}

/*This function frees all the memory which was dynamically allocated in the molecule given in its argument*/
void molfree( molecule *ptr ){

    free(ptr->atoms); // freeing atoms
    free(ptr->atom_ptrs); // freeing atom pointers

    free(ptr->bonds); // freeing bonds
    free(ptr->bond_ptrs); // freeing bond pointers
    free(ptr); // freeing the molecule

}


/*This function adds an atom to the the given molecule*/
void molappend_atom( molecule *molecule, atom *atom ){


    if(molecule->atom_no == molecule->atom_max){ // checking if atom number is equal to atom max
        switch(molecule->atom_max){
            case 0:
            molecule->atom_max += 1; // if atom max is 0, increment it by 1
            break;

            default:
            molecule->atom_max *= 2; // else multiply it by 2
        }
    }

    molecule->atoms = realloc(molecule->atoms, sizeof(struct atom)*molecule->atom_max); // reallocating memory for atoms
    molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*)*molecule->atom_max); // reallocating memory for bonds

    int i = 0;
    while(i < molecule->atom_no){
        molecule->atom_ptrs[i] = &molecule->atoms[i]; // pointers are initialized after realloc, so pointing them to atoms again
        i++;
    }

    molecule->atoms[molecule->atom_no] = *atom; // adding the atom given in the argument to the molecule
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no]; // adding a pointer pointing towards the added atom

    molecule->atom_no += 1; // incrementing atom number by 1

}

/*This function adds a bond to the given molecule*/
void molappend_bond( molecule *molecule, bond *bond ){


    if(molecule->bond_no == molecule->bond_max){ // checking if bond number is equal to bond max
        switch(molecule->bond_max){
            case 0:
            molecule->bond_max += 1; // if bond max is 0, increment it by 1
            break;

            default:
            molecule->bond_max *= 2; // else multiply it by 2
        }
    }

    molecule->bonds = realloc(molecule->bonds, sizeof(struct bond)*molecule->bond_max); // reallocating space to bonds
    molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*)*molecule->bond_max); // reallocating space to bond pointers

    int i = 0;
    while(i < molecule->bond_no){
        molecule->bond_ptrs[i] = &molecule->bonds[i]; // pointers are initialized after realloc, so pointing them to bonds again
        i++;
    }

    molecule->bonds[molecule->bond_no] = *bond; // adding the bond give in the argument to the molecule
    molecule->bonds[molecule->bond_no].a1 = bond->a1; // DOUBT
    molecule->bonds[molecule->bond_no].a2 = bond->a2; // DOUBT
    molecule->bonds[molecule->bond_no].atoms = bond->atoms; // DOUBT
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no]; // adding pointer pointing towards added bond


    molecule->bond_no += 1;

}

/*This function sorts the atom pointers and bond pointers in the molecule according to its z value in inceasing order*/
void molsort( molecule *molecule ) {

    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), compare_atom); // sorting atom pointers
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), bond_comp); // sorting bond pointers

}

/*compare function for qsort using atoms */
int compare_atom(const void *a, const void* b){

    struct atom* x, *y;
    x = *(struct atom**)a;
    y = *(struct atom**)b;

    if(x->z > y->z){
        return 1; // return 1 if previous element greater than next element
    } else if(x->z == y->z){
        return 0; // return 0 if both elements are same
    } else{
        return -1; // else return -1
    }

}

/*Compare function in qsort using bonds*/
// int compare_bond(const void *a, const void* b){
//     struct bond*x, *y;
//     x = *(struct bond**)a;
//     y = *(struct bond**)b;

//     double first, second;

//     first = ((x->a1->z)+(x->a2->z))/2; // taking average z values of the atoms
//     second = ((y->a1->z)+(y->a2->z))/2; // takignaverage z values of the atoms

//     if(first > second){
//         return 1; // if previous element greater than next element return 1
//     } else if(first == second){
//         return 0; // return 0 if both elements are similar
//     } else{
//         return -1; // return -1 otherwise
//     }
// }

// this function is an updated compare bond function
int bond_comp( const void *a, const void *b ){
    struct bond*x, *y;
    x = *(struct bond**)a;
    y = *(struct bond**)b;

    double first, second;

    first = x->z; // taking average z values of the atoms
    second = y->z; // takignaverage z values of the atoms

    if(first > second){
        return 1; // if previous element greater than next element return 1
    } else if(first == second){
        return 0; // return 0 if both elements are similar
    } else{
        return -1; // return -1 otherwise
    }
}

/*This function rotates deg degrees around the x axis*/
void xrotation( xform_matrix xform, unsigned short deg ){

    double rad = deg*(3.141592/180); // converting degrees to radians

    xform_matrix[0][0] = 1;
	xform_matrix[0][1] = 0;
	xform_matrix[0][2] = 0;
	xform_matrix[1][0] = 0;
	xform_matrix[1][1] = cos(rad);
	xform_matrix[1][2] = -sin(rad);
	xform_matrix[2][0] = 0;
	xform_matrix[2][1] = sin(rad);
	xform_matrix[2][2] = cos(rad);

}

/*This function rotates deg degrees around the y axis*/
void yrotation( xform_matrix xform, unsigned short deg ){

    double rad = deg*(3.141592/180);  // converting degrees to radians

	xform_matrix[0][0] = cos(rad);
	xform_matrix[0][1] = 0;
	xform_matrix[0][2] = sin(rad);
	xform_matrix[1][0] = 0;
	xform_matrix[1][1] = 1;
	xform_matrix[1][2] = 0;
	xform_matrix[2][0] = -sin(rad);
	xform_matrix[2][1] = 0;
	xform_matrix[2][2] = cos(rad);

}

/*This function rotates deg degrees around the z axis*/
void zrotation( xform_matrix xform, unsigned short deg ){

    double rad = deg*(3.141592/180);  // converting degrees to radians

    xform_matrix[0][0] = cos(rad);
	xform_matrix[0][1] = -sin(rad);
	xform_matrix[0][2] = 0;
	xform_matrix[1][0] = sin(rad);
	xform_matrix[1][1] = cos(rad);
	xform_matrix[1][2] = 0;
	xform_matrix[2][0] = 0;
	xform_matrix[2][1] = 0;
	xform_matrix[2][2] = 1;
}

/*This function performs matrix multiplaction on all atoms present in the molecule with the matrix in the argument*/
void mol_xform( molecule *molecule, xform_matrix matrix ){

    for(int i = 0; i < molecule->atom_no; i++){

        double x = molecule->atoms[i].x; // assigning x value
        double y = molecule->atoms[i].y; // assigning y value
        double z = molecule->atoms[i].z; // assigning z value
        molecule->atoms[i].x = x*matrix[0][0] + y*matrix[0][1] + z*matrix[0][2]; // matrix multiplication
        molecule->atoms[i].y = x*matrix[1][0] + y*matrix[1][1] + z*matrix[1][2]; // matrix multiplication
        molecule->atoms[i].z = x*matrix[2][0] + y*matrix[2][1] + z*matrix[2][2]; // matrix multiplication
    }

    for(int i = 0; i < molecule->bond_no; i++){
        compute_coords(&molecule->bonds[i]);
    }
}


/*Functions for testing*/
// void displayAtom(atom *atom){
//     printf("element: %s", atom->element);
//     printf("x: %f y: %f z: %f\n", atom->x, atom->y, atom->z);
// }

// void displayBond(bond *bond){
//     printf("element: %s\n", bond->atoms[bond->a1]);
//     printf("x: %f y: %f z: %f\n\n", bond->x1, bond->y1, bond->atoms[bond->a1]->z);

//     printf("element: %s\n", bond->a2->element);
//     printf("x: %f y: %f z: %f\n\n", bond->a2->x, bond->a2->y, bond->a2->z);

//     printf("%u\n", bond->epairs);
// }

