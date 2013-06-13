! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: isprime (start) 

 .global isprime

! function: mod (start) 

 .global mod
     save %sp, -64, %sp

! return (start)
     ld [%fp + offset], %l4     ! push x
     ld [%fp + offset], %l5     ! push x
     ld [%fp + offset], %l6     ! push y
!     div
     mov %l6, %o0
     call .div
     mov %l5, %o0
     mov %o0, %l5
     ld [%fp + offset], %l6     ! push y
!     mul
     mov %l6, %o0
     call .mul
     mov %l5, %o0
     mov %o0, %l5
!     sub
     sub %l5, %l4, %l4
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: mod (end) 

     save %sp, -72, %sp

! assign (start)
     mov 2, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L1:

     ld [%fp + offset], %l0     ! push i
     ld [%fp + offset], %l1     ! push n
!     <
     cmp %l1, %l0
     bl .L3
     mov 1, %l0
     mov 0, %l0
!     relop:= pop
!     if not relop: goto .L2

! ifthen (start)

! funcall (mod) (start)
     ld [%fp + offset], %l1     ! push n
     store %l1, %o0      ! arg0 :=pop
     ld [%fp + offset], %l1     ! push i
     store %l1, %o1      ! arg1 :=pop
     call .mod
     mov %l1, %o0     ! push mod(arg0, arg2)
! funcall (end)
     mov 0, %l2      ! push constant value
!     ==
     cmp %l2, %l1
     be .L4
     mov 1, %l1
     mov 0, %l1
!     cond:= pop
!     if not cond: goto end

! return (start)
     mov 0, %l2      ! push constant value
!     expr := pop
!     return(expr)
! return (end)
! end:
! ifthen (end)

! assign (start)
     ld [%fp + offset], %l2     ! push i
     mov 1, %l3      ! push constant value
!     add
     add %l3, %l2, %l2
     st %l2, [%fp + offset]     ! i := pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
     mov 1, %l3      ! push constant value
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: isprime (end) 


! function: main (start) 

 .global main
     save %sp, -72, %sp

! print (start)
! call flprint()
     sethi %hi(.L5), %o0
     or %o0, %lo(.L5), %o0
     call flprint
     nop
! print (end)

! read (start)
!     read(x)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l4
! read (end)

! assign (start)

! funcall (isprime) (start)
     ld [%fp + offset], %l3     ! push x
     store %l3, %o0      ! arg0 :=pop
     call .isprime
     mov %l3, %o0     ! push isprime(arg0, arg1)
! funcall (end)
     st %l3, [%fp + offset]     ! r := pop
! assign (end)
! write (start)
     ld [%fp + offset], %l4     ! push x
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l4, %o0
     call flwritei
     nop
! write (end)

! ifthenelse (start)
     ld [%fp + offset], %l4     ! push r
     mov 1, %l5      ! push constant value
!     ==
     cmp %l5, %l4
     be .L6
     mov 1, %l4
     mov 0, %l4
!     cond:= pop
!     if not cond: goto else

! print (start)
! call flprint()
     sethi %hi(.L7), %o0
     or %o0, %lo(.L7), %o0
     call flprint
     nop
! print (end)
! goto end:
! else:

! print (start)
! call flprint()
     sethi %hi(.L8), %o0
     or %o0, %lo(.L8), %o0
     call flprint
     nop
! print (end)
! end:
! ifthenelse (end)

 .Ln:
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L5: .asciz "Entre un numero_NL_"
.L7: .asciz " es primo_NL_"
.L8: .asciz " no es primo_NL_"

