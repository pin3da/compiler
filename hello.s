! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: gcd (start) 

 .global gcd
     save %sp, -72, %sp

! assign (start)
     ld [%fp + offset], %l0     ! push y
!     g:= pop
! assign (end)

! while (start)

 .L1:

     ld [%fp + offset], %l1     ! push x
     mov 0, %l2       ! push constant value
!     >
!     relop:= pop
!     if not relop: goto .L2

! assign (start)
     ld [%fp + offset], %l3     ! push x
!     g:= pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l4     ! push y
     ld [%fp + offset], %l5     ! push y
     ld [%fp + offset], %l6     ! push x
!     div
     ld [%fp + offset], %l7     ! push x
!     mul
!     sub
!     x:= pop
! assign (end)

! assign (start)
     st %l0, [%fp -64]
     ld [%fp + offset], %l0     ! push g
!     y:= pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
     st %l1, [%fp -68]
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
     save %sp, -120, %sp

! assign (start)
     st %l2, [%fp -72]
     ld [%fp + offset], %l2     ! push x
     st %l3, [%fp -76]
     ld [%fp + offset], %l3     ! push y
     st %l4, [%fp -80]
     mov 2, %l4       ! push constant value
!     mul
!     add
!     index := pop
     st %l5, [%fp -84]
     ld [%fp + offset], %l5     ! push r
!     arr[index]:= pop
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
     ld [%fp + offset], %l6     ! push x
!     arg1 :=pop
     ld [%fp + offset], %l7     ! push y
!     arg2 :=pop
! funcall (end)
! push gcd()
!     r:= pop
! assign (end)
! write (start)
     st %l0, [%fp -88]
     ld [%fp + offset], %l0     ! push r
!     expr := pop
!     write(expr)
! call flwritei(int)
     mov %%l7, %o0
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

