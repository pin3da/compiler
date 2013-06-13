! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: main (start) 

 .global main
     save %sp, -72, %sp

! print (start)
! call flprint()
     sethi %hi(.L1), %o0
     or %o0, %lo(.L1), %o0
     call flprint
     nop
! print (end)

! assign (start)
     mov 1, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L2:

     ld [%fp + offset], %l0     ! push i
     mov 10, %l1      ! push constant value
!     <=
     cmp %l1, %l0
     ble .L4
     mov 1, %l0
     mov 0, %l0
!     relop:= pop
!     if not relop: goto .L3
! write (start)
     ld [%fp + offset], %l1     ! push i
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l1, %o0
     call flwritei
     nop
! write (end)

! print (start)
! call flprint()
     sethi %hi(.L5), %o0
     or %o0, %lo(.L5), %o0
     call flprint
     nop
! print (end)

! assign (start)
     ld [%fp + offset], %l0     ! push i
     mov 1, %l1      ! push constant value
!     add
     add %l1, %l0, %l0
     st %l0, [%fp + offset]     ! i := pop
! assign (end)

! goto .L2

 .L3:

! while (end)

! print (start)
! call flprint()
     sethi %hi(.L6), %o0
     or %o0, %lo(.L6), %o0
     call flprint
     nop
! print (end)

 .Ln:
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L1: .asciz "Contando a 10_NL_"
.L5: .asciz "_NL_"
.L6: .asciz "Adios_NL_"

