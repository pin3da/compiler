! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: gcd (start) 

 .global gcd
     save %sp, -72, %sp

! assign (start)
     mov y, %l0      ! push y
!     g:= pop
! assign (end)

! while (start)

 .L1:

     mov x, %l1      ! push x
     mov 0, %l2       ! push constant value
!     >
     cmp %l2, %l1
     bg .L3
     mov 1, %l1
     mov 0, %l1
!     relop:= pop
!     if not relop: goto .L2

! assign (start)
     mov x, %l2      ! push x
!     g:= pop
! assign (end)

! assign (start)
     mov y, %l3      ! push y
     mov y, %l4      ! push y
     mov x, %l5      ! push x
!     div
     mov %l5, %o0
     call .div
     mov %l4, %o0
     mov %o0, %l4
     mov x, %l5      ! push x
!     mul
     mov %l5, %o0
     call .mul
     mov %l4, %o0
     mov %o0, %l4
!     sub
     sub %l4, %l3, %l3
!     x:= pop
! assign (end)

! assign (start)
     mov g, %l4      ! push g
!     y:= pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
     mov g, %l5      ! push g
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: gcd (end) 


! function: main (start) 

 .global main
