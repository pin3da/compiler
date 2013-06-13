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

 .L1:

     ld [%fp + offset], %l0     ! push n
     mov 0, %l1      ! push constant value
!     >
     cmp %l1, %l0
     bg .L3
     mov 1, %l0
     mov 0, %l0
!     relop:= pop
!     if not relop: goto .L2

! assign (start)
     ld [%fp + offset], %l0     ! push r
     ld [%fp + offset], %l1     ! push n
!     mul
     mov %l1, %o0
     call .mul
     mov %l0, %o0
     mov %o0, %l0
     st %l0, [%fp + offset]     ! r := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l0     ! push n
     mov 1, %l1      ! push constant value
!     sub
     sub %l1, %l0, %l0
     st %l0, [%fp + offset]     ! n := pop
! assign (end)

! goto .L1

 .L2:

! while (end)

! return (start)
     ld [%fp + offset], %l1     ! push r
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: fact (end) 


! function: main (start) 

 .global main
     save %sp, -72, %sp

! print (start)
! call flprint()
     sethi %hi(.L4), %o0
     or %o0, %lo(.L4), %o0
     call flprint
     nop
! print (end)

! print (start)
! call flprint()
     sethi %hi(.L5), %o0
     or %o0, %lo(.L5), %o0
     call flprint
     nop
! print (end)

! read (start)
!     read(n)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l1
! read (end)
! write (start)

! funcall (fact) (start)
     ld [%fp + offset], %l1     ! push n
     store %l1, %o0      ! arg0 :=pop
     call .fact
     mov %l1, %o0     ! push fact(arg0, arg1)
! funcall (end)
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l1, %o0
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

.L4: .asciz "Hola. Soy un factorial sencillo._NL_"
.L5: .asciz "Entre n :"

