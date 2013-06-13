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

 .L2:

     ld [%fp + offset], %l0     ! push x
     mov 0, %l1      ! push constant value
     cmp %l1, %l0
     bg .L4     ! >
     mov 1, %l0
     mov 0, %l0
 .L4:
     cmp %l0, %g0     ! relop:= pop
     be .L3     ! if not relop: goto .L3
     nop

! assign (start)
     ld [%fp + offset], %l-1     ! push x
     st %l-1, [%fp + offset]     ! g := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push y
     ld [%fp + offset], %l0     ! push y
     ld [%fp + offset], %l1     ! push x
     mov %l1, %o0
     call .div     ! div
     mov %l0, %o0
     mov %o0, %l0
     ld [%fp + offset], %l1     ! push x
     mov %l1, %o0
     call .mul     ! mul
     mov %l0, %o0
     mov %o0, %l0
     sub %l0, %l-1, %l-1     ! sub
     st %l-1, [%fp + offset]     ! x := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push g
     st %l-1, [%fp + offset]     ! y := pop
! assign (end)

     ba  .L2     ! goto .L2
     nop

 .L3:

! while (end)

! return (start)
     ld [%fp + offset], %l0     ! push g
     mov %l0, %o0     ! expr := pop
     jmp .L1     ! return(expr)
     nop
! return (end)

.L1
     ret
     restore

! function: gcd (end) 


! function: main (start) 

 .global main
     save %sp, -80, %sp

! print (start)
! call flprint()
     sethi %hi(.L6), %o0
     or %o0, %lo(.L6), %o0
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

! read (start)
!     read(y)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l-1
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

.L5
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L6: .asciz "Entre dos numeros_NL_"

