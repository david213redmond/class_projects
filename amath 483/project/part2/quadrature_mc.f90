
module quadrature_mc

contains

real(kind=8) function quad_mc(g, a, b, ndim, npoints)
    real(kind=8), external :: g
    real(kind=8), intent(in), dimension(ndim) :: a, b
    integer, intent(in) :: ndim, npoints
    
    ! fields
    real(kind=8) :: Vol, g_sum
    real(kind=8), dimension(ndim) :: x
    real(kind=8) :: r(ndim, npoints)
    integer :: j, k
    
    ! initiate random numbers
    call random_number(r)

    Vol = product(b-a)
    g_sum = 0.d0
    x = 0.d0
    do k = 1, npoints
        do j = 1, ndim
            x(j) = a(j) + r(k,j) * (b(j) - a(j))        
            enddo
        g_sum = g_sum + g(x,n_dim)
        enddo
    quad_mc = Vol * g_sum /npoints
end function quad_mc

end module quadrature_mc
