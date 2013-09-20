! $UWHPSC/codes/fortran/newton/functions.f90

module quadrature_omp

contains

real(kind=8) function trapezoid(f,a,b,n)
    use omp_lib
    implicit none
    real(kind=8), external :: f
    real(kind=8), intent(in) :: a
    real(kind=8), intent(in) :: b
    integer, intent(in) :: n

    real(kind=8) :: h
    real(kind=8), dimension(n) :: xj
    real(kind=8), dimension(n) :: fj
    real(kind=8) :: area
    integer :: i

    h = (b-a)/(n-1)
    area = 0.d0
    !$omp parallel do
    do i = 1,n
	xj(i) = a + (i-1) * (b-a)/(n-1)
	fj(i) = f(xj(i))
        area = area + h*fj(i)
	enddo
    !$omp end parallel do

    area = area -0.5d0 * h * (fj(1) + fj(n))
    trapezoid = area
end function trapezoid

real(kind=8) function f1(x)
    implicit none
    real(kind=8), intent(in) :: x
    f1 = 1.d0 + x**3.d0
end function f1

real(kind=8) function f2(x)
    implicit none
    real(kind=8), intent(in) :: x
    f2 = 1.d0 + x**3 + sin(50*x)
end function f2

real(kind=8) function f2p(x)
    implicit none
    real(kind=8), intent(in) :: x
    f2p = 1.d0 + x**3 + sin(1000*x)
end function f2p

subroutine error_table(f,a,b,nvals,int_true)
    implicit none
    real(kind=8), external :: f
    real(kind=8), intent(in) :: a,b,int_true
    integer,dimension(:), intent(in) :: nvals	

    real(kind=8) :: int_trap, error, last_error, ratio
    integer :: n,i,nval_i	
    n = size(nvals)

    print 11
11  format('       n         trapezoid            error       ratio')
    last_error = 0.d0
    do i=1,n
	nval_i = nvals(i)
	int_trap = trapezoid(f,a,b,nval_i)
	error = abs(int_trap - int_true)
        ratio = last_error / error
        last_error = error 
	print 12, nval_i, int_trap, error, ratio
12      format(i8,'  ', e22.14,'  ', e10.3,'  ', e10.3,'  ')  
	enddo
    
end subroutine error_table
 
end module quadrature_omp
