! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: mf (start) 

 .global mf
     ! Lenght can not be calculated
     save %sp, -472, %sp

! assign (start)
     mov 10, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! a := pop
! assign (end)

! assign (start)
     mov 10, %l-1      ! push constant value
     mov 5, %l0      ! push constant value
     add %l0, %l-1, %l-1     ! add
     st %l-1, [%fp + offset]     ! b := pop
! assign (end)

.L1
     ret
     restore

! function: mf (end) 


! function: main (start) 

 .global main
     save %sp, -72, %sp

! funcall (mf) (start)
     mov 5, %l0      ! push constant value
     store %l0, %o0      ! arg0 :=pop
     mov 12, %l0      ! push constant value
     store %l0, %o1      ! arg1 :=pop
     sethi %hi(.L3), %g1
     or %g1, %lo(.L3), %g1
     ld [%g1], %l0
     store %l0, %o2      ! arg2 :=pop
     call .mf
     mov %l0, %o0     ! push mf(arg0, arg3)
! funcall (end)

! assign (start)
     mov 5, %l0      ! push constant value
     st %l0, [%fp + offset]     ! a := pop
! assign (end)

.L2
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

     .L3: .float "1.3"

