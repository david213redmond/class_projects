! $UWHPSC/codes/fortran/newton/intersections.f90

program intersections

    use newton, only: solve
    use functions, only: g1g2, g1g2p
    
    implicit none
    real(kind=8) :: x, x0, fx
    real(kind=8) :: x0vals(4)
    integer :: iters, itest
    logical :: debug

    debug = .false.
    x0vals = (/-2.2d0,-1.6d0,-0.77d0,1.43d0/)
    
    do itest = 1,4
	x0 = x0vals(itest)

        print 11, x0
11      format('With the initial guess x0 = ', e22.15)

 	call solve(g1g2, g1g2p, x0, x, iters, debug)

        print 12, x, iters
12      format('	 solver returns x = ', e22.15, ' after', i3, ' iterations')

        fx = g1g2(x)

        if (abs(fx) > 1d-14) then
            print 13, x
13          format('*** Unexpected result: x = ', e22.15)
            endif
		print *, ' '  ! blank line
        enddo

end program intersections
