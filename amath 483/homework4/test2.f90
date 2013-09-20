program test2

    use quadrature, only: trapezoid, f2p, error_table
    
    implicit none
    real(kind=8) :: a2,b2,k
    real(kind=8) :: int_true1, int_true2
    real(kind=8) :: int_trap
    integer :: nvals(12), i
    
    do i = 1,12
	nvals(i) = 5 * 2 ** (i-1)
        enddo
!printing the integrals for f2.

    a2 = 0.d0
    b2 = 2.d0
    k = 1000.d0
    int_true2 = (b2-a2) + (b2**4 - a2**4) / 4.d0 - (1.d0/k) * (cos(k*b2) - cos(k*a2))
    print 12, int_true2
12  format('true integral: ', e22.14)
    call error_table(f2p,a2,b2,nvals,int_true2)

end program test2
