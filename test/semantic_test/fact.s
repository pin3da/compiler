! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: fact (start) 

 .global fact
     save %sp, -64, %sp

! ifthenelse (start)
     ld [%fp + offset], %l0     ! push n
     mov 1, %l1      ! push constant value
!     ==
     cmp %l1, %l0
     be .L1
     mov 1, %l0
     mov 0, %l0
!     cond:= pop
!     if not cond: goto else

! return (start)
     mov 1, %l1      ! push constant value
!     expr := pop
!     return(expr)
! return (end)
! goto end:
! else:

! return (start)
     ld [%fp + offset], %l2     ! push n

! funcall (fact) (start)
     ld [%fp + offset], %l3     ! push n
     mov 1, %l4      ! push constant value
!     sub
     sub %l4, %l3, %l3
     store %l3, %o0      ! arg0 :=pop
     call .fact
     mov %l3, %o0     ! push fact(arg0, arg1)
! funcall (end)
!     mul
     mov %l3, %o0
     call .mul
     mov %l2, %o0
     mov %o0, %l2
!     expr := pop
!     return(expr)
! return (end)
! end:
! ifthenelse (end)

 .Ln:
     ret
     restore

! function: fact (end) 


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

! read (start)
!     read(x)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l2
! read (end)

! assign (start)

! funcall (fact) (start)
     ld [%fp + offset], %l1     ! push x
     store %l1, %o0      ! arg0 :=pop
     call .fact
     mov %l1, %o0     ! push fact(arg0, arg1)
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

.L2: .asciz "Entre un numero_NL_"

