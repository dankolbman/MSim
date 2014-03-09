/*
 *  Calculates the radial distribution function g(r) for
 *  file of particle positions.
 *  Dan Kolbman, 2014
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_PART 5000
// Calculates the cube of a number
#define Cube(x) ((x) * (x) * (x))

void gr(FILE *fin, FILE *fout, int numPart, double radSep, double size, int numBins){
	int line;
	double dr;		// One shell radius increment 
	double rho;		// Density
	double gofr[numBins];
	int i, j;		// Iterating vars
	double dx, dy, dz, dist;
	double x[numPart], y[numPart], z[numPart];
	
	//printf("C> Begin C version of g(r)\n");
	rho = numPart/size;	// Calculate density
	
	dr = 0.5*size/numBins;

	for (i=0; i < numBins; i++){
		gofr[i] = 0;
	}

	for(line = 0; line < numPart; line++){
		fscanf(fin, "%lf %lf %lf\n", &x[line], &y[line], &z[line]);
	}

	for(i=0; i<numPart-1;i++){
		for(j=i+1; j<numPart;j++){
			dx = x[i] - x[j];
			dx = dx - size*round(dx/size);

			dy = y[i] - y[j];
			dy = dy - size*round(dy/size);
			
			dz = z[i] - z[j];
			dz = dz - size*round(dz/size);
			
			dist = sqrt( dx*dx + dy*dy + dz*dz);
			if(dist < 0.5*size){
				gofr[(int)(dist/dr)] += 2.0;
			}
		}
	}
	for(i=0;i < numBins; i++){
		gofr[i] /= (4.0/3.0)*M_PI*(Cube(i+1) - Cube(i))*Cube(dr)*rho;
		fprintf(fout, "%0.16f %0.32f\n", (i+0.5)*dr/radSep, gofr[i]/numPart);
	}
	printf("C> Wrote g(r)\n");
}

int main(int argc, char **argv){
	FILE *fin, *fout;	// File streams
	char *fileIn, *fileOut;	// File names
	char fileInName[] = "in.dat";
	char fileOutName[] = "out.dat";
	int numPart = 400;
	double radSep = 0.112725;
	double size = 1;
	int numBins = 150;

	fileIn = fileInName;
	fileOut = fileOutName;
	if(argc == 1){			// Use defualts fin = fopen(fileIn, "r");
		fout = fopen(fileOut, "w");
	}
	else{
		if(argc >= 2){ 		// Use given input file
			fileIn = argv[1];
			fin = fopen(fileIn, "r");
			if(fin == NULL){
				printf("!! Can't open %s\n", argv[1]);
				exit(0);
			}
			fout = fopen(fileOut, "w");
		}
		if(argc >= 3){		// Use given output file
			fileOut = argv[2];
			fout = fopen(fileOut, "w");
			if(fout == NULL){
				printf("C> Making file %s\n", fileOut);
				exit(0);
			}
		}
		if(argc >= 4){		// Use particle number
			sscanf(argv[3],"%d",&numPart);
		}
		if(argc >= 5){		// Use box size
			sscanf(argv[4],"%lf",&radSep);
		}
		if(argc >= 6){		// Use box size
			sscanf(argv[5],"%lf",&size);
		}
		if(argc >= 7){		// Use box size
			sscanf(argv[6],"%d",&numBins);
		}
	}
	//printf("Running with in=%s, out=%s, numPart=%d, radSep=%f size=%f, bins=%d\n", fileIn, fileOut, numPart, radSep, size, numBins);
	gr(fin, fout, numPart, radSep, size, numBins);
	fclose(fin);
	fclose(fout);
	return 0;
}
