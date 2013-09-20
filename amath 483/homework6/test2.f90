
program test2

    use mpi

    use quadrature, only: trapezoid
    use functions, only: f, fevals_proc, k

    implicit none
    real(kind=8) :: a,b,int_true, int_approx, int_sub,  dx_sub
    real(kind=8), dimension(2) :: ab_sub

    integer :: j, proc_num, num_procs, ierr, n, nsub, fevals_total
    integer, dimension(MPI_STATUS_SIZE) :: status

    call MPI_INIT(ierr)
    call MPI_COMM_SIZE(MPI_COMM_WORLD, num_procs, ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, proc_num, ierr)

    ! All processes set these values so we don't have to broadcast:
    k = 1.d3   ! functions module variable 
    a = 0.d0
    b = 2.d0
    int_true = (b-a) + (b**4 - a**4) / 4.d0 - (1.d0/k) * (cos(k*b) - cos(k*a))
    n = 1000

    ! Each process keeps track of number of fevals:
    fevals_proc = 0
    if (proc_num==0) then
        print '("Using ",i3," processes")', num_procs
        print '("true integral: ", es22.14)', int_true
        print *, " "  ! blank line
        fevals_total = 0
        int_approx = 0.d0
        nsub = num_procs - 1
        dx_sub = (b-a) / nsub
        do j=1,nsub
            ab_sub(1) = a + (j-1)*dx_sub
            ab_sub(2) = a + j*dx_sub
            call MPI_SEND(ab_sub, 2, MPI_DOUBLE_PRECISION, j, j, MPI_COMM_WORLD, ierr)
            enddo
        do j=1,nsub
            call MPI_RECV(int_sub, 1, MPI_DOUBLE_PRECISION, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, status, ierr)     
            int_approx = int_approx + int_sub
            enddo
        endif


    if (proc_num /= 0) then
        call MPI_RECV(ab_sub, 2, MPI_DOUBLE_PRECISION,  0, MPI_ANY_TAG, MPI_COMM_WORLD, status, ierr)
        j = status(MPI_TAG)
        int_sub = trapezoid(f, ab_sub(1), ab_sub(2),n)
        call MPI_SEND(int_sub, 1, MPI_DOUBLE_PRECISION, 0, j, MPI_COMM_WORLD, ierr)
        endif

    print '("fevals by Process ",i3," :      ",i8)',proc_num, fevals_proc
    call MPI_BARRIER(MPI_COMM_WORLD,ierr) ! wait for all process to print
    
    call MPI_REDUCE(fevals_proc, fevals_total,1,MPI_DOUBLE_PRECISION,MPI_SUM,0, MPI_COMM_WORLD,ierr) 

    if (proc_num==0) then
        print '("Trapezoid approximation with ",i8," total points: ",es22.14)',&
            nsub*n, int_approx
        print '("Total number of fevals: ",i10)', fevals_total
        endif

    call MPI_FINALIZE(ierr)

end program test2
