! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: gcd (start) 

 .global gcd
     save %sp, -72, %sp

! assign (start)
     ld [%fp + offset], %l-1     ! push y
     st %l-1, [%fp + offset]     ! g := pop
! assign (end)

! while (start)

 .L1:

     ld [%fp + offset], %l0     ! push x
     mov 0, %l1      ! push constant value
!     >
     cmp %l1, %l0
     bg .L3
     mov 1, %l0
     mov 0, %l0
!     relop:= pop
!     if not relop: goto .L2

! assign (start)
     ld [%fp + offset], %l0     ! push x
     st %l0, [%fp + offset]     ! g := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l0     ! push y
     ld [%fp + offset], %l1     ! push y
     ld [%fp + offset], %l2     ! push x
!     div
     mov %l2, %o0
     call .div
     mov %l1, %o0
     mov %o0, %l1
     ld [%fp + offset], %l2     ! push x
!     mul
     mov %l2, %o0
     call .mul
     mov %l1, %o0
     mov %o0, %l1
!     sub
     sub %l1, %l0, %l0
     st %l0, [%fp + offset]     ! x := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l0     ! push g
     st %l0, [%fp + offset]     ! y := pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
     ld [%fp + offset], %l1     ! push g
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: gcd (end) 


! function: main (start) 

 .global main
     save %sp, -80, %sp

! print (start)
! call flprint()
     sethi %hi(.L4), %o0
     or %o0, %lo(.L4), %o0
     call flprint
     nop
! print (end)

! read (start)
!     read(x)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l1
! read (end)

! read (start)
!     read(y)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l0
! read (end)

! assign (start)

! funcall (gcd) (start)
     ld [%fp + offset], %l-1     ! push x
     store %l-1, %o0      ! arg0 :=pop
     ld [%fp + offset], %l-1     ! push y
     store %l-1, %o1      ! arg1 :=pop
     call .gcd
     mov %l-1, %o0     ! push gcd(arg0, arg2)
! funcall (end)
     st %l-1, [%fp + offset]     ! r := pop
! assign (end)
! write (start)
     ld [%fp + offset], %l0     ! push r
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l0, %o0
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

.L4: .asciz "Entre dos numeros_NL_"

