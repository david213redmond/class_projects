% DSK_FIR67.M
% MATLAB function to write FIR filter coefficients
% in format suitable for use in C6713 DSK programs
% fir.c and firprn.c
% written by Donald Reay
%
function makeCoeff(coeff)
%
coefflen=length(coeff);
fname = input('enter filename for coefficients ','s');
fid = fopen(fname,'wt');
fprintf(fid,'// %s\n',fname);
fprintf(fid,'// this file was generated automatically using function makeCoeff\n',fname);
fprintf(fid,'\n#define N %d\n',coefflen);
fprintf(fid,'\nshort coeffs[N] = { \n');
% j is used to count coefficients written to current line
% in output file
j=0;
% i is used to count through coefficients
for i=1:coefflen  
% if six coeffs have been written to current line
% then start new line
  if j>5    
    j=0; 
    fprintf(fid,'\n');  
  end  
% if this is the last coefficient then simply write
% its value to the current line
% else write coefficient value, followed by comma
  if i==coefflen
   fprintf(fid,'%i',coeff(i));
  else
    fprintf(fid,'%i,',coeff(i));  
    j=j+1;
  end
end
fprintf(fid,'\n};\n');
fclose(fid);          
