! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

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
     jmp .L1     ! return(expr)
     nop
! return (end)

.L1
     ret
     restore

! function: mod (end) 


! function: factor (start) 

 .global factor
     save %sp, -72, %sp

! assign (start)
     mov 1, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! nfacts := pop
! assign (end)

! assign (start)
     mov 0, %l-1      ! push constant value
     sll %l-1, 2, %l-1
     add %fp, %l-1, %l-1      ! index := pop
     mov 1, %l-1      ! push constant value
     st %l-1, [%l-1 + offset]     ! stor[index] := pop
! assign (end)

! assign (start)
     mov 2, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L3:

     ld [%fp + offset], %l0     ! push i
     ld [%fp + offset], %l1     ! push n
     cmp %l1, %l0
     ble .L5     !<=
     mov 1, %l0
     mov 0, %l0
 .L5:
     cmp %l0, %g0     ! relop:= pop
     be .L4     ! if not relop: goto .L4
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
     be .L7     ! ==
     mov 1, %l0
     mov 0, %l0
 .L7:
     cmp %l0, g0     !cond:= pop
     be .L6     ! goto .L6
     nop

! assign (start)
     ld [%fp + offset], %l-1     ! push nfacts
     mov 1, %l0      ! push constant value
     add %l0, %l-1, %l-1     ! add
     st %l-1, [%fp + offset]     ! nfacts := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push i
     mov 1, %l0      ! push constant value
     sub %l0, %l-1, %l-1     ! sub
     sll %l-1, 2, %l-1
     add %fp, %l-1, %l-1      ! index := pop
     ld [%fp + offset], %l-1     ! push i
     st %l-1, [%l-1 + offset]     ! stor[index] := pop
! assign (end)

 .L6:

! ifthen (end)

! assign (start)
     ld [%fp + offset], %l-1     ! push i
     mov 1, %l0      ! push constant value
     add %l0, %l-1, %l-1     ! add
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

     ba  .L3     ! goto .L3
     nop

 .L4:

! while (end)

! return (start)
     ld [%fp + offset], %l0     ! push nfacts
     mov %l0, %o0     ! expr := pop
     jmp .L2     ! return(expr)
     nop
! return (end)

.L2
     ret
     restore

! function: factor (end) 


! function: print_arr (start) 

 .global print_arr
     save %sp, -72, %sp

! assign (start)
     mov 0, %l-1      ! push constant value
     st %l-1, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L9:

     ld [%fp + offset], %l0     ! push i
     ld [%fp + offset], %l1     ! push nelem
     cmp %l1, %l0
     bl .L11     ! <
     mov 1, %l0
     mov 0, %l0
 .L11:
     cmp %l0, %g0     ! relop:= pop
     be .L10     ! if not relop: goto .L10
     nop
! write (start)
     ld [%fp + offset], %l0     ! push i
     sll %l0, 2, %l0
     add %fp, %l0, %l0      ! index := pop
     ld [%l0 + offset], %l0     ! push a[index] !     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l0, %o0
     call flwritei
     nop
! write (end)

! print (start)
! call flprint()
     sethi %hi(.L12), %o0
     or %o0, %lo(.L12), %o0
     call flprint
     nop
! print (end)

! ifthen (start)

! funcall (mod) (start)
     ld [%fp + offset], %l0     ! push i
     store %l0, %o0      ! arg0 :=pop
     mov 5, %l0      ! push constant value
     store %l0, %o1      ! arg1 :=pop
     call .mod
     mov %l0, %o0     ! push mod(arg0, arg2)
! funcall (end)
     mov 0, %l1      ! push constant value
     ld [%fp + offset], %l1     ! push i
     mov 0, %l2      ! push constant value
     and %l1, %l0, %l0     ! and
     cmp %l0, g0     !cond:= pop
     be .L13     ! goto .L13
     nop

! print (start)
! call flprint()
     sethi %hi(.L14), %o0
     or %o0, %lo(.L14), %o0
     call flprint
     nop
! print (end)

 .L13:

! ifthen (end)

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

.L8
     ret
     restore

! function: print_arr (end) 


! function: main (start) 

 .global main
     save %sp, -4168, %sp

! print (start)
! call flprint()
     sethi %hi(.L16), %o0
     or %o0, %lo(.L16), %o0
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

! funcall (factor) (start)
     ld [%fp + offset], %l-1     ! push x
     store %l-1, %o0      ! arg0 :=pop
     ld [%fp + offset], %l-1     ! push results
     store %l-1, %o1      ! arg1 :=pop
     call .factor
     mov %l-1, %o0     ! push factor(arg0, arg2)
! funcall (end)
     st %l-1, [%fp + offset]     ! nfs := pop
! assign (end)

! funcall (print_arr) (start)
     ld [%fp + offset], %l0     ! push results
     store %l0, %o0      ! arg0 :=pop
     ld [%fp + offset], %l0     ! push nfs
     store %l0, %o1      ! arg1 :=pop
     call .print_arr
     mov %l0, %o0     ! push print_arr(arg0, arg2)
! funcall (end)

.L15
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L12: .asciz " "
.L14: .asciz "_NL_"
.L16: .asciz "Enter a number_NL_"

