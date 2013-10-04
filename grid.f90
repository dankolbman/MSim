! grid.f90
! Dan Kolbman
! Initialize a 2d grid and place particles on it

program grid

  implicit none
  integer    ::  nPart, i    ! Number of particles
  real    :: pos(100, 2)     ! Positions for each particle
  nPart = 100
  pos  = gridInit( nPart, 1.0 )
 
  open (unit=3,file="results.dat",action="write",status="replace")

  ! Dump positions
  do i=1,nPart
    ! Write to file
    write (3,"(F7.5, A2, F7.5)")  pos(i,1), "  ", pos(i,2)
  end do
  ! Close file stream
  close(3)

  contains

  function gridInit( n, len ) result(pos)
    ! Initialize grid with n particles and length of len
    ! Return a position matrix of particles
  
    integer, intent(in)  :: n
    real,    intent(in)  :: len
    real :: pos(n,2)  ! Position matrix
    real    ::  latConst, nPart
    integer :: i, j, pnum, sideNum
  
    nPart = real(n)     ! Cast so we can sqrt
    sideNum = int( ceiling( sqrt( nPart ) ) )

    latConst = len/sideNum

    ! Loop over all grid points placing particles until all
    ! particles have been placed
    do i=1,sideNum
      do j=1,sideNum
        ! The number of the next particle in the matrix
        pnum = (i-1)*sideNum + j
        ! Get out if no more particles
        if (pnum > n) then
          exit
        else
          ! Set the position of the next particle
          pos( pnum, 1 ) = (i-1)*latConst + 0.5*latConst  ! x
          pos( pnum, 2 ) = (j-1)*latConst + 0.5*latConst  ! y

          ! Print to terminal
          !write(*,"(F6.5, F6.5)") pos(pnum,1), pos(pnum,2)
        end if
      end do
    end do

  end function gridInit


end program
