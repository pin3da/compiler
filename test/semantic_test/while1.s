! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: main (start) 

 .global main
     save %sp, -72, %sp

! print (start)
! call flprint()
     sethi %hi(.L2), %o0
     or %o0, %lo(.L2), %o0
     call flprint
     nop
! print (end)

! assign (start)
     mov 1, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L3:

     ld [%fp + offset], %l0     ! push i
     mov 10, %l1      ! push constant value
     cmp %l1, %l0
     ble .L5     !<=
     mov 1, %l0
     mov 0, %l0
 .L5:
     cmp %l0, %g0     ! relop:= pop
     be .L4     ! if not relop: goto .L4
     nop
! write (start)
     ld [%fp + offset], %l0     ! push i
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l0, %o0
     call flwritei
     nop
! write (end)

! print (start)
! call flprint()
     sethi %hi(.L6), %o0
     or %o0, %lo(.L6), %o0
     call flprint
     nop
! print (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push i
     mov 1, %l0      ! push constant value
     add %l0, %l-1, %l-1     ! add
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

     ba  .L3     ! goto .L3
     nop

 .L4:

! while (end)

! print (start)
! call flprint()
     sethi %hi(.L7), %o0
     or %o0, %lo(.L7), %o0
     call flprint
     nop
! print (end)

.L1
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L2: .asciz "Contando a 10_NL_"
.L6: .asciz "_NL_"
.L7: .asciz "Adios_NL_"

