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
!     relop:= pop
!     if not relop: goto .L2

! assign (start)
     ld [%fp + offset], %l1     ! push x
     st %l1, [%fp + offset]     ! g := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l1     ! push y
     ld [%fp + offset], %l2     ! push y
     ld [%fp + offset], %l3     ! push x
!     div
     ld [%fp + offset], %l4     ! push x
!     mul
!     sub
     st %l1, [%fp + offset]     ! x := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l4     ! push g
     st %l4, [%fp + offset]     ! y := pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
     ld [%fp + offset], %l5     ! push g
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: gcd (end) 


! function: main (start) 

 .global main
     save %sp, -120, %sp

! assign (start)
     ld [%fp + offset], %l5     ! push x
     ld [%fp + offset], %l6     ! push y
     mov 2, %l7      ! push constant value
!     mul
!     add
     sll %l7, 2, %l7
     add %fp, %l7, %l7      ! index := pop
     ld [%fp + offset], %l7     ! push r
     st %l5, [%l7 + offset]     ! arr[index] := pop
! assign (end)

! print (start)
! call flprint()
     sethi %hi(.L3), %o0
     or %o0, %lo(.L3), %o0
     call flprint
     nop
! print (end)

! read (start)
!     read(x)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l7
! read (end)

! read (start)
!     read(y)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l6
! read (end)

! assign (start)

! funcall (gcd) (start)
     ld [%fp + offset], %l5     ! push x
     store %l5, %o0      ! arg0 :=pop
     ld [%fp + offset], %l5     ! push y
     store %l5, %o1      ! arg1 :=pop
     call .gcd
     mov %l5, %o0     ! push gcd(arg0, arg2)
! funcall (end)
     st %l5, [%fp + offset]     ! r := pop
! assign (end)
! write (start)
     ld [%fp + offset], %l6     ! push r
!     expr := pop
!     write(expr)
! call flwritei(int)
     mov %%l6, %o0
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

.L3: .asciz "Entre dos numeros_NL_"

