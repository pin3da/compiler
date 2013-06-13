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
     ld [%fp + offset], %l0     ! push x
     ld [%fp + offset], %l1     ! push x
     ld [%fp + offset], %l2     ! push y
     mov %l2, %o0
     call .div     ! div
     mov %l1, %o0
     mov %o0, %l1
     ld [%fp + offset], %l2     ! push y
     mov %l2, %o0
     call .mul     ! mul
     mov %l1, %o0
     mov %o0, %l1
     sub %l1, %l0, %l0     ! sub
     mov %l0, %o0     ! expr := pop
     jmp .L7     ! return(expr)
     nop
! return (end)

.L7
     ret
     restore

! function: mod (end) 

     save %sp, -72, %sp

! assign (start)
     mov 2, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L2:

     ld [%fp + offset], %l0     ! push i
     ld [%fp + offset], %l1     ! push n
     cmp %l1, %l0
     bl .L4     ! <
     mov 1, %l0
     mov 0, %l0
 .L4:
     cmp %l0, %g0     ! relop:= pop
     be .L3     ! if not relop: goto .L3
     nop

! ifthen (start)

! funcall (mod) (start)
     ld [%fp + offset], %l0     ! push n
     store %l0, %o0      ! arg0 :=pop
     ld [%fp + offset], %l0     ! push i
     store %l0, %o1      ! arg1 :=pop
     call .mod
     mov %l0, %o0     ! push mod(arg0, arg2)
! funcall (end)
     mov 0, %l1      ! push constant value
     cmp %l1, %l0
     be .L6     ! ==
     mov 1, %l0
     mov 0, %l0
 .L6:
     cmp %l0, g0     !cond:= pop
     be .L5     ! goto .L5
     nop

 .L5:

! ifthen (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push i
     mov 1, %l0      ! push constant value
     add %l0, %l-1, %l-1     ! add
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

     ba  .L2     ! goto .L2
     nop

 .L3:

! while (end)

! return (start)
     mov 1, %l0      ! push constant value
     mov %l0, %o0     ! expr := pop
     jmp .L1     ! return(expr)
     nop
! return (end)

.L1
     ret
     restore

! function: isprime (end) 


! function: main (start) 

 .global main
     save %sp, -72, %sp

! print (start)
! call flprint()
     sethi %hi(.L9), %o0
     or %o0, %lo(.L9), %o0
     call flprint
     nop
! print (end)

! read (start)
!     read(x)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l-1
! read (end)

! assign (start)

! funcall (isprime) (start)
     ld [%fp + offset], %l-1     ! push x
     store %l-1, %o0      ! arg0 :=pop
     call .isprime
     mov %l-1, %o0     ! push isprime(arg0, arg1)
! funcall (end)
     st %l-1, [%fp + offset]     ! r := pop
! assign (end)
! write (start)
     ld [%fp + offset], %l0     ! push x
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l0, %o0
     call flwritei
     nop
! write (end)

! ifthenelse (start)
     ld [%fp + offset], %l0     ! push r
     mov 1, %l1      ! push constant value
     cmp %l1, %l0
     be .L12     ! ==
     mov 1, %l0
     mov 0, %l0
 .L12:
     cmp %l0, g0     ! cond:= pop
     be .L10     ! if not cond: goto else
     nop

! print (start)
! call flprint()
     sethi %hi(.L13), %o0
     or %o0, %lo(.L13), %o0
     call flprint
     nop
! print (end)
     ba .L11     ! if not cond: goto end:

 .L10:     ! else:

! print (start)
! call flprint()
     sethi %hi(.L14), %o0
     or %o0, %lo(.L14), %o0
     call flprint
     nop
! print (end)

 .L11:     ! end:
! ifthenelse (end)

.L8
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L9: .asciz "Entre un numero_NL_"
.L13: .asciz " es primo_NL_"
.L14: .asciz " no es primo_NL_"

