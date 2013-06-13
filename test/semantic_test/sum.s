! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: sum (start) 

 .global sum
     save %sp, -72, %sp

! assign (start)
     mov 0, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! s := pop
! assign (end)

! assign (start)
     mov 0, %l-1      ! push constant value
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

! assign (start)
     ld [%fp + offset], %l-1     ! push s
     ld [%fp + offset], %l0     ! push i
     sll %l0, 2, %l0
     add %fp, %l0, %l0      ! index := pop
     ld [%l0 + offset], %l0     ! push a[index]      add %l0, %l-1, %l-1     ! add
     st %l-1, [%fp + offset]     ! s := pop
! assign (end)

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
     ld [%fp + offset], %l0     ! push s
     mov %l0, %o0     ! expr := pop
     jmp .L1     ! return(expr)
     nop
! return (end)

.L1
     ret
     restore

! function: sum (end) 


! function: main (start) 

 .global main
     save %sp, -4080, %sp

! print (start)
! call flprint()
     sethi %hi(.L6), %o0
     or %o0, %lo(.L6), %o0
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

! ifthenelse (start)
     ld [%fp + offset], %l-1     ! push n
     mov 0, %l0      ! push constant value
     ld [%fp + offset], %l0     ! push n
     mov 1000, %l1      ! push constant value
     and %l0, %l-1, %l-1     ! and
     cmp %l-1, g0     ! cond:= pop
     be .L7     ! if not cond: goto else
     nop

! assign (start)
     mov 0, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L9:

     ld [%fp + offset], %l0     ! push i
     ld [%fp + offset], %l1     ! push n
     cmp %l1, %l0
     bl .L11     ! <
     mov 1, %l0
     mov 0, %l0
 .L11:
     cmp %l0, %g0     ! relop:= pop
     be .L10     ! if not relop: goto .L10
     nop

! assign (start)
     ld [%fp + offset], %l-1     ! push i
     sll %l-1, 2, %l-1
     add %fp, %l-1, %l-1      ! index := pop
     ld [%fp + offset], %l-1     ! push i
     st %l-1, [%l-1 + offset]     ! x[index] := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push i
     mov 1, %l0      ! push constant value
     add %l0, %l-1, %l-1     ! add
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

     ba  .L9     ! goto .L9
     nop

 .L10:

! while (end)

! assign (start)

! funcall (sum) (start)
     ld [%fp + offset], %l-1     ! push x
     store %l-1, %o0      ! arg0 :=pop
     ld [%fp + offset], %l-1     ! push n
     store %l-1, %o1      ! arg1 :=pop
     call .sum
     mov %l-1, %o0     ! push sum(arg0, arg2)
! funcall (end)
     st %l-1, [%fp + offset]     ! s := pop
! assign (end)
! write (start)
     ld [%fp + offset], %l0     ! push s
!     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l0, %o0
     call flwritei
     nop
! write (end)
     ba .L8     ! if not cond: goto end:

 .L7:     ! else:

! print (start)
! call flprint()
     sethi %hi(.L12), %o0
     or %o0, %lo(.L12), %o0
     call flprint
     nop
! print (end)

 .L8:     ! end:
! ifthenelse (end)

.L5
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L6: .asciz "Entre un numero n : "
.L12: .asciz "Valor malo de n_NL_"

