program test1

    use quadrature, only: trapezoid, f1, f2, error_table
    
    implicit none
    real(kind=8) :: a1,b1,a2,b2,k
    real(kind=8) :: int_true1, int_true2
    real(kind=8) :: int_trap
    integer :: nvals(7)
    
    a1 = 0.d0
    b1 = 2.d0
    int_true1 = (b1-a1) + (b1**4.d0 -a1**4.d0) / 4.d0    
    
!printing the integrals for f1.
    print 11,int_true1
11  format('true integral: ', e22.14)
    nvals = (/5, 10, 20, 40, 80, 160, 320/)
    call error_table(f1,a1,b1,nvals,int_true1)

!printing the integrals for f2.

    a2 = 0.d0
    b2 = 2.d0
    k = 50.d0
    int_true2 = (b2-a2) + (b2**4 - a2**4) / 4.d0 - (1.d0/k) * (cos(k*b2) - cos(k*a2))
    print 12, int_true2
12  format('true integral: ', e22.14)
    nvals = (/5, 10, 20, 40, 80, 160, 320/)
    call error_table(f2,a2,b2,nvals,int_true2)

end program test1
