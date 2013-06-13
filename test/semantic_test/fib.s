! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: fib (start) 

 .global fib
     save %sp, -64, %sp

! ifthenelse (start)
     ld [%fp + offset], %l0     ! push n
     mov 0, %l1      ! push constant value
     ld [%fp + offset], %l1     ! push n
     mov 1, %l2      ! push constant value
!     or
     or %l1, %l0, %l0
!     cond:= pop
!     if not cond: goto else

! return (start)
     ld [%fp + offset], %l1     ! push n
!     expr := pop
!     return(expr)
! return (end)
! goto end:
! else:

! return (start)

! funcall (fib) (start)
     ld [%fp + offset], %l2     ! push n
     mov 1, %l3      ! push constant value
!     sub
     sub %l3, %l2, %l2
     store %l2, %o0      ! arg0 :=pop
     call .fib
     mov %l2, %o0     ! push fib(arg0, arg1)
! funcall (end)

! funcall (fib) (start)
     ld [%fp + offset], %l3     ! push n
     mov 2, %l4      ! push constant value
!     sub
     sub %l4, %l3, %l3
     store %l3, %o0      ! arg0 :=pop
     call .fib
     mov %l3, %o0     ! push fib(arg0, arg1)
! funcall (end)
!     add
     add %l3, %l2, %l2
!     expr := pop
!     return(expr)
! return (end)
! end:
! ifthenelse (end)

 .Ln:
     ret
     restore

! function: fib (end) 


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

! read (start)
!     read(x)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l2
! read (end)

! assign (start)

! funcall (fib) (start)
     ld [%fp + offset], %l1     ! push x
     store %l1, %o0      ! arg0 :=pop
     call .fib
     mov %l1, %o0     ! push fib(arg0, arg1)
! funcall (end)
     st %l1, [%fp + offset]     ! r := pop
! assign (end)
! write (start)
     ld [%fp + offset], %l2     ! push r
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l2, %o0
     call flwritei
     nop
! write (end)

 .Ln:
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L1: .asciz "Entre un nuemro_NL_"

