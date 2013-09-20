
module mc_walk

    implicit none
    real(kind=8), parameter :: ax = 0.0d0
    real(kind=8), parameter :: bx = 1.0d0
    real(kind=8), parameter :: ay = 0.4d0
    real(kind=8), parameter :: by = 1.0d0
    integer, parameter :: nx = 19
    integer, parameter :: ny = 11
    real(kind=8), parameter :: dx = (bx - ax) / (nx+1)
    real(kind=8), parameter :: dy = (by - ay) / (ny+1)
    logical :: debug

contains

function utrue(x, y)

    ! True solution for comparison, if known.

    implicit none
    real(kind=8), intent(in) :: x,y
    real(kind=8) :: utrue

    utrue = x**2 - y**2

end function utrue

function uboundary(x, y)

    ! Return u(x,y) assuming (x,y) is a boundary point.

    implicit none
    real(kind=8), intent(in) :: x,y
    real(kind=8) :: uboundary

    if ((x-ax)*(x-bx)*(y-ay)*(y-by) .ne. 0.d0) then
        print *, "*** Error -- called uboundary at non-boundary point"
        stop
        endif

    uboundary = utrue(x,y)   ! assuming we know this

end function uboundary
    
subroutine random_walk(i0, j0, max_steps, ub, iabort)
    implicit none
    integer, intent(in) :: i0, j0, max_steps
    integer, intent(out) :: iabort
    real(kind=8), intent(out) :: ub
    real(kind=8) ,allocatable :: r(:)
    integer :: index, i, j, istep
    real(kind=8) :: xb, yb

!python code

!   """
!   Take one random walk starting at (i0,j0) until we reach the boundary or
!   exceed max_steps steps.
!   Return the value at the boundary point reached, or nan if we failed.
!   """

!   starting point.
    debug = .false.
    i = i0
    j = j0
    ub = 0.d0

!   generate as many random numbers as we could possibly need
!   for this walk, since this is much faster than generating one at a time:
    allocate(r(max_steps))
    call random_number(r)
    do istep = 1,max_steps
        if (r(istep) < 0.25d0) then
            i = i-1   ! step left
        else if (r(istep) < 0.5d0) then
            i = i+1   ! step right
        else if (r(istep) < 0.75d0) then
            j = j-1   ! step down
        else
            j = j+1   ! step up
            endif
        
!        if plot_walk:
!            plot_step(iold,jold, i,j, istep)

        ! check if we hit the boundary:

        if (i*j*(nx+1-i)*(ny+1-j) == 0) then
            xb = ax + i*dx
            yb = ay + j*dy
            ub = uboundary(xb, yb)

!            if plot_walk:
!                plot_ub(xb,yb,ub)
            if (debug) then
                print '("Hit boundary at (",es22.14,",",es22.14,") after ", i3, "steps, ub = ", es22.14)'&
                        ,xb,yb,istep, ub
                endif
            iabort = 0
            goto 99! end the walk
            endif
        if (istep == max_steps) then
            if (debug) then
                print '("Did not hit boundary after", i3, "steps")', max_steps
                endif
            !if plot_walk:
            !    text(0, -0.2, "Did not hit boundary after %i steps" \
            !            % max_steps, fontsize=20)
            !    draw()
            !    time.sleep(2)
            iabort = 1
            endif
        enddo 
99 continue ! end of program            
end subroutine random_walk

subroutine many_walks(i0, j0, max_steps, n_mc, u_mc, n_success)
    
    integer, intent(in) :: i0, j0, max_steps,n_mc
    integer, intent(out) :: n_success
    real(kind=8), intent(out) :: u_mc 
    real(kind=8) :: ub, ub_sum
    integer :: k, iabort

    ub_sum = 0.d0   ! to accumulate boundary values reached from all walks
    n_success = 0    ! to keep track of how many walks reached boundary

    do k = 1,n_mc
        call random_walk(i0, j0, max_steps, ub,iabort)
        if (iabort == 0) then
            ub_sum = ub_sum + ub
            n_success = n_success + 1    
            endif
        enddo
    u_mc = ub_sum / n_success    ! average over successful walks

end subroutine many_walks

end module mc_walk
