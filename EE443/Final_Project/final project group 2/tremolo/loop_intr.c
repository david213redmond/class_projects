//loop_intr.c loop program using interrupts
#include "DSK6713_AIC23.h"	        //codec support
Uint32 fs=DSK6713_AIC23_FREQ_8KHZ;	//set sampling rate
#define DSK6713_AIC23_INPUT_MIC 0x0015
#define DSK6713_AIC23_INPUT_LINE 0x0011
#define fs 8000
Uint16 inputsource=DSK6713_AIC23_INPUT_MIC; // select input

short tremCarrier(int,int);
short phaser(int,short);

short buffer[8000]; 
int bufIndex = 0;	//the index of the current sample being modulated
int freq = 16;
int tremSelect = 1;	//signwave, squarewave, triangular, or saw toothed.
int tremWaveLength;	//the waveLength of an entire tremolo effect. 
int phaseDelay;

interrupt void c_int11()         //interrupt service routine
{
   short sample_data;	//input data
   short carrier;		//carrier data
   //constants
   tremWaveLength = fs/freq;
   phaseDelay = 100;

   //tremolo effect 
   sample_data = input_sample(); 
//   carrier = tremCarrier(1,tremWaveLength);
//   sample_data = carrier * sample_data;
   //phaser effect	
   sample_data = sample_data +  phaser(phaseDelay, sample_data)/4 + phaser(500, sample_data)/4 + phaser(1000, sample_data)/4;
   
   buffer[bufIndex++] = sample_data;
   output_sample(buffer[bufIndex-1]);   //output data
   if(bufIndex >= fs ){bufIndex = 0;}
   return;
}

void main()
{
  comm_intr();                 //init DSK, codec, McBSP
  while(1);                	   //infinite loop
}

//output the carrier signal that is required for the tremolo modulation.
short tremCarrier(int tremSelect, int waveSamplesLength){
	short carrier = 0;
	switch(tremSelect)
	{
		case 1:	//square wave
			if(bufIndex%waveSamplesLength < waveSamplesLength*3/4){carrier = 1;}
			else{carrier = 0;}
		// sine, triangular, saw toothed
	}
	return carrier;
}

short phaser(int delay, short sample){
	int dIndex = bufIndex - delay;
	short delayedSample;
	if(dIndex >=0){	
		delayedSample = buffer[dIndex];
	}else{
		delayedSample = buffer[8000 + dIndex];
	}

	if(sample == 0){
		delayedSample = 0;
	}
	return delayedSample;
}
 

