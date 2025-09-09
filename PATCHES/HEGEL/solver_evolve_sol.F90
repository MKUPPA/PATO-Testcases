! -*-f90-*-
!-----------------------------------------------------------------------------!
! HEGEL (High fidElity tool for maGnEtogas-dynamics simuLations)
!
! Copyright (c) 2019-2020, Center for Hypersonics and Entry Systems Studies (CHESS),
! University of Illinois at Urbana-Champaign
!
! All rights reserved.
!-----------------------------------------------------------------------------!
!> This module provides subroutines to advance the solution with or w/o coupling
!
!> @file solver_evolve_sol.F90
!> @brief module providing subroutines to evolve the numerical solution with or w/o coupling
!> @author Alessandro Munafo` (CHESS, University of Illinois at Urbana-Champaign, munafo@illinois.edu)
!
  submodule(class_solver) evolve_sol

#include"hegel_config.h"

    implicit none

    contains 

      !---------------------------------------------------!
      !> This subroutine evolves the solution in case of no coupling
      module subroutine evolve_sol_uncoupled(this)

        class(solver), intent(inout) :: this   !< solver 

        !===================!
        ! Advance solution of one time-step
        call this%integrator%evolve(this%simulation, this%mesh, this%fluid, this%radiation, this%flowfield, this%res) 

        !===================!
        ! Update convergence history file. In doing that residual is normalized and the iteration counter updated 
        call this%update_conv_file()

        !===================!
        ! Peform I/O operations or modify mesh
        call this%manager()

      end subroutine evolve_sol_uncoupled

      !---------------------------------------------------!
      !> This subroutine evolves the solution in case of coupling
      module subroutine evolve_sol_coupled(this)

        class(solver), intent(inout) :: this   !< solver 

        real(kind=hpc_8)             :: dt, time, time_old
        logical                      :: done_coupling

        !===================!
        ! Advance solution solution of time-step
        ! Get current time
        time_old = this%simulation%get_time()

        ! Perform coupling loop
        done_coupling = .false.
        coupling_loop : do 
        
           ! Set action for implicit coupling
           ! Save checkpoint according to the value of writing action
#ifdef HEGEL_HAVE_PRECICE           
           if (this%code_coupler%is_action_required(this%write_it_checkp)) then
              call this%code_coupler%save_old_state(this%mesh, this%fluid, this%flowfield)
              call this%code_coupler%mark_action_fulfilled(this%write_it_checkp)
           endif

           ! Read data
           call this%code_coupler%read_data(this%mesh, this%fluid)  
#else
           call safe_exit(ERR_STR//"'solver%evolve_sol_coupled()', procedure invoked w/o liking with preCICE")
#endif
           ! Evolve solution of one-time-step
           call this%integrator%evolve(this%simulation, this%mesh, this%fluid, this%radiation, this%flowfield, this%res)

           ! Get used time-step
           time = this%simulation%get_time()
           dt   = time - time_old
            
#ifdef HEGEL_HAVE_PRECICE           
           ! Write data     
           call this%fluid%set_ghost_states(this%simulation, this%mesh, this%flowfield)
           call this%code_coupler%write_data(dt, this%mesh, this%fluid, this%flowfield)
               
           ! Advance coupler by passing used time-step 
           call this%code_coupler%evolve(dt) 
               
           ! Reload checkpoint according to the value of reading action
           if (this%code_coupler%is_action_required(this%read_it_checkp)) then
              ! Reset time
              time = time_old 
              call this%simulation%set_time(time)
              call this%code_coupler%reload_old_state(this%mesh, this%fluid, this%flowfield)
              call this%code_coupler%mark_action_fulfilled(this%read_it_checkp)
           else
              done_coupling = .true.  
           endif  
#else
           done_coupling = .true.
           call safe_exit(ERR_STR//"'solver%evolve_sol_coupled()', procedure invoked w/o liking with preCICE")
#endif
           ! Check if coupling is completed (e.g., needed for implicit coupling)
           if (done_coupling) exit coupling_loop 

        enddo coupling_loop 

        !===================!
        ! Update convergence history file. In doing that residual is normalized and the iteration counter updated 
        call this%update_conv_file()

        !===================!
        ! Peform I/O operations or modify mesh
        call this%manager()

      end subroutine evolve_sol_coupled

      !---------------------------------------------------!
      !> This subroutine evolves the solution in case of steady-state coupling
      module subroutine evolve_sol_coupled_steady(this)

        class(solver), intent(inout) :: this   !< solver 

        integer(kind=hpc_4)          :: s_ID, e_ID
        integer(kind=hpc_4)          :: it, max_nb_it
        real(kind=hpc_8)             :: dt, time, time_old, lim
        logical                      :: done_coupling
        character(len=s_str)         :: max_it_str

        !===================!
        ! Advance solution solution of time-step
        ! Get current time
        time_old = this%simulation%get_time()

        s_ID = this%svarID_conv
        e_ID = this%evarID_conv

        ! Get steady-state coupling convergence parameters
#ifdef HEGEL_HAVE_PRECICE           
        call this%code_coupler%get_steady_conv_data(max_nb_it, lim)
#else
        max_nb_it = 10; lim = -3.d0
#endif
        write(max_it_str,'(i4)')max_nb_it
        max_it_str = adjustl(max_it_str)

        ! Perform coupling loop
        done_coupling = .false.
        coupling_loop : do 
        
           ! Set action for implicit coupling
           ! Save checkpoint according to the value of writing action

!    ---------------------- VLM - I want to enable steady coupling with implicit coupling in HEGEL
! #ifdef HEGEL_HAVE_PRECICE           
!            if (this%code_coupler%is_action_required(this%write_it_checkp)) then
!               call safe_exit(ERR_STR//"'solver%evolve_sol_coupled_steady()' implicit coupling not available for steady-state mode")
!            endif
!    ---------------------- VLM - I want to enable steady coupling with implicit coupling in HEGEL
           if (this%code_coupler%is_action_required(this%write_it_checkp)) then
              call this%code_coupler%save_old_state(this%mesh, this%fluid, this%flowfield)
              call this%code_coupler%mark_action_fulfilled(this%write_it_checkp)
           endif

           ! Read data
           call this%code_coupler%read_data(this%mesh, this%fluid)  
! #else
!            call safe_exit(ERR_STR//"'solver%evolve_sol_coupled_steady()' preCICE coupled not available")
! #endif
           ! Evolve solution of one-time-step till convergence is not reached or number of iterations is exceeded
           it = ZERO_INT
           ! this%res(:) = ZERO
           ! I am enforcing to do at least one iter if the previous residual meet the precision goal
           ! flow_loop : do while(((maxval(this%res(s_ID:e_ID)).ge.lim).and.(it.lt.max_nb_it)).or.(it.le.ZERO_INT))
           flow_loop : do while(it.lt.max_nb_it)

              call this%simulation%set_time(time_old)
              ! call this%get_sol_L2_norm()

              call this%integrator%evolve(this%simulation, this%mesh, this%fluid, this%radiation, this%flowfield, this%res)
              it = it + 1
              
              ! this%res(s_ID:e_ID) = this%res(s_ID:e_ID) - this%L2_norm(s_ID:e_ID)

              ! if (it.eq.1) this%res0(s_ID:e_ID) = this%res(s_ID:e_ID)
              call this%update_conv_file()
              
              ! Exit loop if number of iterations is excedded 
              ! if (it.ge.max_nb_it) then 
              ! call this%simulation%logger_print_msg(WAR_STR//"'solver%evolve_sol_coupled_steady()' "// & 
              !                                       & "number of flow iterations exceeded limit ("//trim(max_it_str)//")")

              ! exit flow_loop

              ! write(*,*) "Test 1", ((maxval(this%res(s_ID:e_ID)).ge.lim).and.(it.lt.max_nb_it))
              ! write(*,*) "Test 1-1", (maxval(this%res(s_ID:e_ID)).ge.lim)
              ! write(*,*) "Test 1-2", (it.lt.max_nb_it)
              ! write(*,*) "Test 2-2", (it.le.ZERO_INT)
              ! write(*,*) "Test ---", ((maxval(this%res(s_ID:e_ID)).ge.lim).and.(it.lt.max_nb_it)).or.(it.le.ZERO_INT)

              ! endif
              ! if ((maxval(this%res(s_ID:e_ID)).ge.lim).and.(it.lt.max_nb_it)) then
              !    ! call this%simulation%logger_print_msg(WAR_STR//" I am reloading old time")
              !    call this%simulation%set_time(time_old)
              ! end if

           enddo flow_loop 

           ! Get used time-step
           ! write(*,*) "What is the fucking time ?", this%simulation%get_time()
           time = this%simulation%get_time()
           dt   = time - time_old
            
#ifdef HEGEL_HAVE_PRECICE   
           ! Write data   
           call this%fluid%set_ghost_states(this%simulation, this%mesh, this%flowfield)
           call this%code_coupler%write_data(dt, this%mesh, this%fluid, this%flowfield)
               
           ! Advance coupler by passing used time-step 
           call this%code_coupler%evolve(dt)

           ! Reload checkpoint according to the value of reading action
           if (this%code_coupler%is_action_required(this%read_it_checkp)) then
              ! Reset time
              time = time_old 
              call this%simulation%set_time(time)
              call this%code_coupler%reload_old_state(this%mesh, this%fluid, this%flowfield)
              call this%code_coupler%mark_action_fulfilled(this%read_it_checkp)
           else
              done_coupling = .true.  
           endif   
               
!    ---------------------- VLM - I want to enable steady coupling with implicit coupling in HEGEL
! Reload checkpoint according to the value of reading action
!   if (this%code_coupler%is_action_required(this%read_it_checkp)) then
!      call safe_exit(ERR_STR//"'solver%evolve_sol_coupled_steady()' implicit coupling not available for steady-state mode")
!   endif   

         !   done_coupling = .true.  
!    ---------------------- VLM - I want to enable steady coupling with implicit coupling in HEGEL
 
#else
           done_coupling = .true.
           call safe_exit(ERR_STR//"'solver%evolve_sol_coupled_steady()' preCICE coupled not available")
#endif
           ! Check if coupling is completed (e.g., needed for implicit coupling)
           if (done_coupling) exit coupling_loop 

        enddo coupling_loop 

        !===================!
        ! Peform I/O operations or modify mesh
        call this%manager()

      end subroutine evolve_sol_coupled_steady

  end submodule evolve_sol
!-----------------------------------------------------------------------------!
