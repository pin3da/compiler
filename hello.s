! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: gcd (start) 

 .global gcd
     save %sp, -72, %sp

! assign (start)
 mov y, %%l0 !     push y
!     g:= pop
! assign (end)

! while (start)

 .L1:

 mov x, %%l1 !     push x
!     >
!     relop:= pop
!     if not relop: goto .L2

! assign (start)
 mov x, %%l2 !     push x
!     g:= pop
! assign (end)

! assign (start)
 mov y, %%l3 !     push y
 mov y, %%l4 !     push y
 mov x, %%l5 !     push x
!     div
 mov x, %%l6 !     push x
!     mul
!     sub
!     x:= pop
! assign (end)

! assign (start)
 mov g, %%l7 !     push g
!     y:= pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
     st %l0, [%fp -64]
 mov g, %%l0 !     push g
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
     st %l1, [%fp -68]
 mov x, %%l1 !     push x
     st %l2, [%fp -72]
 mov y, %%l2 !     push y
!     mul
!     add
!     index := pop
     st %l3, [%fp -76]
 mov r, %%l3 !     push r
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
! call flreadf()
     call flreadf
     nop
     st %o0, result
! read (end)

! read (start)
!     read(y)
! call flreadf()
     call flreadf
     nop
     st %o0, result
! read (end)

! assign (start)

! funcall (gcd) (start)
     st %l4, [%fp -80]
 mov x, %%l4 !     push x
!     arg1 :=pop
     st %l5, [%fp -84]
 mov y, %%l5 !     push y
!     arg2 :=pop
! funcall (end)
! push gcd()
!     r:= pop
! assign (end)
! write (start)
     st %l6, [%fp -88]
 mov r, %%l6 !     push r
!     expr := pop
!     write(expr)
! call flwritef(float)
     mov val, %o0
     call flwritef
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

