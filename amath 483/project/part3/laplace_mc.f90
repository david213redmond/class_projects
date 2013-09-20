
program laplace_mc

    use random_util, only: init_random_seed 
    use mc_walk

    implicit none
    real(kind=8) :: x0, y0 , u_true, u_mc, u_mc_total, u_sum_old, u_sum_new, error
    integer :: k, i0, j0, iabort, max_steps, seed1, n_mc, n_success, n_total

    ! initialize random seed
    seed1 = 12345
    call init_random_seed(seed1)
    
    ! initialize fields
    x0 = 0.9d0
    y0 = 0.6d0
    i0 = NINT((x0-ax)/dx)
    j0 = NINT((y0-ay)/dy)
    u_true = utrue(x0,y0)
    open(unit=25, file='mc_laplace_error.txt', status='unknown')

    ! shift (x0,y0) to a grid point if it wasn't already:
    x0 = ax + i0*dx
    y0 = ay + j0*dy

    ! begin calculations
    max_steps = 100*max(nx,ny)
    n_mc = 10
    call many_walks(i0, j0, max_steps, n_mc, u_mc, n_success)
    error = abs((u_mc - u_true) / u_true)
    u_mc_total = u_mc
    n_total = n_success

    ! first print
    print '("	",i5, e23.15, e15.6)', n_success, u_mc, error    
    write(25,'(i10,e23.15,e15.6)') n_total, u_mc_total, error


    ! rest of the calculations
    do k =1, 12
        u_sum_old = u_mc_total * n_total
        call many_walks(i0, j0, max_steps, n_mc, u_mc, n_success)
        u_sum_new = u_mc * n_success
        n_total = n_total + n_success
        u_mc_total = (u_sum_old + u_sum_new) / n_total
        error = abs((u_mc_total - u_true) / u_true)
        print '("	",i5, e23.15, e15.6)', n_total, u_mc_total, error
        write(25,'(i10,e23.15,e15.6)') n_total, u_mc_total, error
        n_mc = 2*n_mc
        enddo
    print'("Final approximation to u(x0,y0):", es22.14)', u_mc_total
    print'("Total number of random walks:", i8)', n_total

end program laplace_mc    