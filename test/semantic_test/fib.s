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
     or %l1, %l0, %l0     ! or
     cmp %l0, g0     ! cond:= pop
     be .L2     ! if not cond: goto else
     nop
     ba .L3     ! if not cond: goto end:

 .L2:     ! else:

 .L3:     ! end:
! ifthenelse (end)

.L1
     ret
     restore

! function: fib (end) 


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
     st %o0, %%l-1
! read (end)

! assign (start)

! funcall (fib) (start)
     ld [%fp + offset], %l-1     ! push x
     store %l-1, %o0      ! arg0 :=pop
     call .fib
     mov %l-1, %o0     ! push fib(arg0, arg1)
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

.L4
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L5: .asciz "Entre un nuemro_NL_"

