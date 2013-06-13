! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: gcd (start) 

 .global gcd
     save %sp, --96, %sp

! assign (start)
!     push y
!     g:= pop
! assign (end)

! while (start)

 .L1:

!     push x
!     >
!     relop:= pop
!     if not relop: goto .L2

! assign (start)
!     push x
!     g:= pop
! assign (end)

! assign (start)
!     push y
!     push y
!     push x
!     div
!     push x
!     mul
!     sub
!     x:= pop
! assign (end)

! assign (start)
!     push g
!     y:= pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
!     push g
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: gcd (end) 


! function: main (start) 

 .global main
     save %sp, --96, %sp

! assign (start)
!     push x
!     push y
!     mul
!     add
!     index := pop
!     push r
!     arr[index]:= pop
! assign (end)

! print (start)
! print (end)

! read (start)
!     read(x)
! read (end)

! read (start)
!     read(y)
! read (end)

! assign (start)

! funcall (gcd) (start)
!     push x
!     arg1 :=pop
!     push y
!     arg2 :=pop
! funcall (end)
! push gcd()
!     r:= pop
! assign (end)
! write (start)
!     push r
!     expr := pop
!     write(expr)
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

