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
!     div
     mov %l2, %o0
     call .div
     mov %l1, %o0
     mov %o0, %l1
     ld [%fp + offset], %l2     ! push y
!     mul
     mov %l2, %o0
     call .mul
     mov %l1, %o0
     mov %o0, %l1
!     sub
     sub %l1, %l0, %l0
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: mod (end) 


! function: factor (start) 

 .global factor
     save %sp, -72, %sp

! assign (start)
     mov 1, %l0      ! push constant value
     st %l0, [%fp + offset]     ! nfacts := pop
! assign (end)

! assign (start)
     mov 0, %l0      ! push constant value
     sll %l0, 2, %l0
     add %fp, %l0, %l0      ! index := pop
     mov 1, %l0      ! push constant value
     st %l0, [%l0 + offset]     ! stor[index] := pop
! assign (end)

! assign (start)
     mov 2, %l0      ! push constant value
     st %l0, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L1:

     ld [%fp + offset], %l1     ! push i
     ld [%fp + offset], %l2     ! push n
!     <=
     cmp %l2, %l1
     ble .L3
     mov 1, %l1
     mov 0, %l1
!     relop:= pop
!     if not relop: goto .L2

! ifthen (start)

! funcall (mod) (start)
     ld [%fp + offset], %l2     ! push n
     store %l2, %o0      ! arg0 :=pop
     ld [%fp + offset], %l2     ! push i
     store %l2, %o1      ! arg1 :=pop
     call .mod
     mov %l2, %o0     ! push mod(arg0, arg2)
! funcall (end)
     mov 0, %l3      ! push constant value
!     ==
     cmp %l3, %l2
     be .L4
     mov 1, %l2
     mov 0, %l2
!     cond:= pop
!     if not cond: goto end

! assign (start)
     ld [%fp + offset], %l2     ! push nfacts
     mov 1, %l3      ! push constant value
!     add
     add %l3, %l2, %l2
     st %l2, [%fp + offset]     ! nfacts := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l2     ! push i
     mov 1, %l3      ! push constant value
!     sub
     sub %l3, %l2, %l2
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     ld [%fp + offset], %l2     ! push i
     st %l2, [%l2 + offset]     ! stor[index] := pop
! assign (end)
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
     ld [%fp + offset], %l3     ! push nfacts
!     expr := pop
!     return(expr)
! return (end)

 .Ln:
     ret
     restore

! function: factor (end) 


! function: print_arr (start) 

 .global print_arr
     save %sp, -72, %sp

! assign (start)
     mov 0, %l3      ! push constant value
     st %l3, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L5:

     ld [%fp + offset], %l4     ! push i
     ld [%fp + offset], %l5     ! push nelem
!     <
     cmp %l5, %l4
     bl .L7
     mov 1, %l4
     mov 0, %l4
!     relop:= pop
!     if not relop: goto .L6
! write (start)
     ld [%fp + offset], %l5     ! push i
     sll %l5, 2, %l5
     add %fp, %l5, %l5      ! index := pop
     ld [%l5 + offset], %l5     ! push a[index] !     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l5, %o0
     call flwritei
     nop
! write (end)

! print (start)
! call flprint()
     sethi %hi(.L8), %o0
     or %o0, %lo(.L8), %o0
     call flprint
     nop
! print (end)

! ifthen (start)

! funcall (mod) (start)
     ld [%fp + offset], %l5     ! push i
     store %l5, %o0      ! arg0 :=pop
     mov 5, %l5      ! push constant value
     store %l5, %o1      ! arg1 :=pop
     call .mod
     mov %l5, %o0     ! push mod(arg0, arg2)
! funcall (end)
     mov 0, %l6      ! push constant value
     ld [%fp + offset], %l6     ! push i
     mov 0, %l7      ! push constant value
!     and
     and %l6, %l5, %l5
!     cond:= pop
!     if not cond: goto end

! print (start)
! call flprint()
     sethi %hi(.L9), %o0
     or %o0, %lo(.L9), %o0
     call flprint
     nop
! print (end)
! end:
! ifthen (end)

! assign (start)
     ld [%fp + offset], %l5     ! push i
     mov 1, %l6      ! push constant value
!     add
     add %l6, %l5, %l5
     st %l5, [%fp + offset]     ! i := pop
! assign (end)

! goto .L5

 .L6:

! while (end)

 .Ln:
     ret
     restore

! function: print_arr (end) 


! function: main (start) 

 .global main
     save %sp, -4168, %sp

! print (start)
! call flprint()
     sethi %hi(.L10), %o0
     or %o0, %lo(.L10), %o0
     call flprint
     nop
! print (end)

! read (start)
!     read(x)
! call flreadi(int)
     call flreadi
     nop
     st %o0, %%l5
! read (end)

! assign (start)

! funcall (factor) (start)
     ld [%fp + offset], %l4     ! push x
     store %l4, %o0      ! arg0 :=pop
     ld [%fp + offset], %l4     ! push results
     store %l4, %o1      ! arg1 :=pop
     call .factor
     mov %l4, %o0     ! push factor(arg0, arg2)
! funcall (end)
     st %l4, [%fp + offset]     ! nfs := pop
! assign (end)

! funcall (print_arr) (start)
     ld [%fp + offset], %l5     ! push results
     store %l5, %o0      ! arg0 :=pop
     ld [%fp + offset], %l5     ! push nfs
     store %l5, %o1      ! arg1 :=pop
     call .print_arr
     mov %l5, %o0     ! push print_arr(arg0, arg2)
! funcall (end)

 .Ln:
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L8: .asciz " "
.L9: .asciz "_NL_"
.L10: .asciz "Enter a number_NL_"

