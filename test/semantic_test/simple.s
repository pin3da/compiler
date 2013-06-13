! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: fact (start) 

 .global fact
     save %sp, -72, %sp

! assign (start)
     mov 1, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! r := pop
! assign (end)

! while (start)

 .L2:

     ld [%fp + offset], %l0     ! push n
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
     ld [%fp + offset], %l-1     ! push r
     ld [%fp + offset], %l0     ! push n
     mov %l0, %o0
     call .mul     ! mul
     mov %l-1, %o0
     mov %o0, %l-1
     st %l-1, [%fp + offset]     ! r := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push n
     mov 1, %l0      ! push constant value
     sub %l0, %l-1, %l-1     ! sub
     st %l-1, [%fp + offset]     ! n := pop
! assign (end)

     ba  .L2     ! goto .L2
     nop

 .L3:

! while (end)

! return (start)
     ld [%fp + offset], %l0     ! push r
     mov %l0, %o0     ! expr := pop
     jmp .L1     ! return(expr)
     nop
! return (end)

.L1
     ret
     restore

! function: fact (end) 


! function: main (start) 

 .global main
     save %sp, -72, %sp

! print (start)
! call flprint()
     sethi %hi(.L6), %o0
     or %o0, %lo(.L6), %o0
     call flprint
     nop
! print (end)

! print (start)
! call flprint()
     sethi %hi(.L7), %o0
     or %o0, %lo(.L7), %o0
     call flprint
     nop
! print (end)

! read (start)
!     read(n)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l-1
! read (end)
! write (start)

! funcall (fact) (start)
     ld [%fp + offset], %l-1     ! push n
     store %l-1, %o0      ! arg0 :=pop
     call .fact
     mov %l-1, %o0     ! push fact(arg0, arg1)
! funcall (end)
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l-1, %o0
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

.L6: .asciz "Hola. Soy un factorial sencillo._NL_"
.L7: .asciz "Entre n :"

