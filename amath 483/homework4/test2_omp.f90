!This is the parallel version of homework 4
program test2_omp
    use omp_lib
    use quadrature_omp, only: trapezoid, f2p, error_table
    
    implicit none
    real(kind=8) :: a2,b2,k
    real(kind=8) :: int_true1, int_true2
    real(kind=8) :: int_trap
    integer:: i, nvals(12)

    ! Specify number of threads to use:
    !$ call omp_set_num_threads(2)
    !$omp parallel
    !$omp parallel do
    do i = 1,12
	nvals(i) = 5 * 2 ** (i-1)
        enddo
    !$omp end parallel do
    !$omp end parallel
!printing the integrals for f2.

    a2 = 0.d0
    b2 = 2.d0
    k = 1000.d0
    int_true2 = (b2-a2) + (b2**4 - a2**4) / 4.d0 - (1.d0/k) * (cos(k*b2) - cos(k*a2))
    print 12, int_true2
12  format('true integral: ', e22.14)
    call error_table(f2p,a2,b2,nvals,int_true2)
    
end program test2_omp
