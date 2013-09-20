
OBJECTS = random_util.o mc_walk.o laplace_mc.o
FFLAGS = 

.PHONY: test plot clean clobber

plot: plot.exe plot_mc_laplace_error.py
	./plot.exe
	python plot_mc_laplace_error.py

plot.exe: $(OBJECTS)
	gfortran $(FFLAGS) $(OBJECTS) -o plot.exe

%.o : %.f90
	gfortran $(FFLAGS) -c  $< 

clean:
	rm -f *.o *.exe *.mod *.txt *.png

