! main.f90
! Dan Kolbman
! Run a simulation, print files

program main

  use grid

  implicit none integer    ::  nPart, i    ! Number of particles
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
end program
