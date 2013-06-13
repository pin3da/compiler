! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: mrgsort (start) 

 .global mrgsort

! function: merge (start) 

 .global merge
     save %sp, -120, %sp

! assign (start)
     ld [%fp + offset], %l2     ! push p
     st %l2, [%fp + offset]     ! ptr1 := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l2     ! push q
     st %l2, [%fp + offset]     ! ptr2 := pop
! assign (end)

! assign (start)
     mov 0, %l2      ! push constant value
     st %l2, [%fp + offset]     ! nitems := pop
! assign (end)

! while (start)

 .L5:

     ld [%fp + offset], %l3     ! push ptr1
     ld [%fp + offset], %l4     ! push q
     ld [%fp + offset], %l4     ! push ptr2
     ld [%fp + offset], %l5     ! push r
     and %l4, %l3, %l3     ! and
     cmp %l3, %g0     ! relop:= pop
     be .L6     ! if not relop: goto .L6
     nop

! ifthenelse (start)
     ld [%fp + offset], %l3     ! push ptr1
     sll %l3, 2, %l3
     add %fp, %l3, %l3      ! index := pop
     ld [%l3 + offset], %l3     ! push n[index]      ld [%fp + offset], %l4     ! push ptr2
     sll %l4, 2, %l4
     add %fp, %l4, %l4      ! index := pop
     ld [%l4 + offset], %l4     ! push n[index]      cmp %l4, %l3
     ble .L9     !<=
     mov 1, %l3
     mov 0, %l3
 .L9:
     cmp %l3, g0     ! cond:= pop
     be .L7     ! if not cond: goto else
     nop

! assign (start)
     ld [%fp + offset], %l2     ! push nitems
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     ld [%fp + offset], %l2     ! push ptr1
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     ld [%l2 + offset], %l2     ! push n[index]      st %l2, [%l2 + offset]     ! temp[index] := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l2     ! push ptr1
     mov 1, %l3      ! push constant value
     add %l3, %l2, %l2     ! add
     st %l2, [%fp + offset]     ! ptr1 := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l2     ! push nitems
     mov 1, %l3      ! push constant value
     add %l3, %l2, %l2     ! add
     st %l2, [%fp + offset]     ! nitems := pop
! assign (end)
     ba .L8     ! if not cond: goto end:

 .L7:     ! else:

! assign (start)
     ld [%fp + offset], %l2     ! push nitems
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     ld [%fp + offset], %l2     ! push ptr2
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     ld [%l2 + offset], %l2     ! push n[index]      st %l2, [%l2 + offset]     ! temp[index] := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l2     ! push ptr2
     mov 1, %l3      ! push constant value
     add %l3, %l2, %l2     ! add
     st %l2, [%fp + offset]     ! ptr2 := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l2     ! push nitems
     mov 1, %l3      ! push constant value
     add %l3, %l2, %l2     ! add
     st %l2, [%fp + offset]     ! nitems := pop
! assign (end)

 .L8:     ! end:
! ifthenelse (end)

     ba  .L5     ! goto .L5
     nop

 .L6:

! while (end)

! assign (start)
     mov 0, %l2      ! push constant value
     st %l2, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L10:

     ld [%fp + offset], %l3     ! push i
     ld [%fp + offset], %l4     ! push nitems
     cmp %l4, %l3
     bl .L12     ! <
     mov 1, %l3
     mov 0, %l3
 .L12:
     cmp %l3, %g0     ! relop:= pop
     be .L11     ! if not relop: goto .L11
     nop

! assign (start)
     ld [%fp + offset], %l2     ! push p
     ld [%fp + offset], %l3     ! push i
     add %l3, %l2, %l2     ! add
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     ld [%fp + offset], %l2     ! push i
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     ld [%l2 + offset], %l2     ! push temp[index]      st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     ld [%fp + offset], %l2     ! push i
     mov 1, %l3      ! push constant value
     add %l3, %l2, %l2     ! add
     st %l2, [%fp + offset]     ! i := pop
! assign (end)

     ba  .L10     ! goto .L10
     nop

 .L11:

! while (end)

.L4
     ret
     restore

! function: merge (end) 

     save %sp, -72, %sp

! ifthen (start)
     ld [%fp + offset], %l0     ! push p
     ld [%fp + offset], %l1     ! push r
     cmp %l1, %l0
     bl .L3     ! <
     mov 1, %l0
     mov 0, %l0
 .L3:
     cmp %l0, g0     !cond:= pop
     be .L2     ! goto .L2
     nop

! assign (start)
     ld [%fp + offset], %l-1     ! push p
     ld [%fp + offset], %l0     ! push r
     add %l0, %l-1, %l-1     ! add
     mov 2, %l0      ! push constant value
     mov %l0, %o0
     call .div     ! div
     mov %l-1, %o0
     mov %o0, %l-1
     st %l-1, [%fp + offset]     ! q := pop
! assign (end)

! funcall (mrgsort) (start)
     ld [%fp + offset], %l0     ! push nums
     store %l0, %o0      ! arg0 :=pop
     ld [%fp + offset], %l0     ! push p
     store %l0, %o1      ! arg1 :=pop
     ld [%fp + offset], %l0     ! push q
     store %l0, %o2      ! arg2 :=pop
     call .mrgsort
     mov %l0, %o0     ! push mrgsort(arg0, arg3)
! funcall (end)

! funcall (mrgsort) (start)
     ld [%fp + offset], %l1     ! push nums
     store %l1, %o0      ! arg0 :=pop
     ld [%fp + offset], %l1     ! push q
     mov 1, %l2      ! push constant value
     add %l2, %l1, %l1     ! add
     store %l1, %o1      ! arg1 :=pop
     ld [%fp + offset], %l1     ! push r
     store %l1, %o2      ! arg2 :=pop
     call .mrgsort
     mov %l1, %o0     ! push mrgsort(arg0, arg3)
! funcall (end)

! funcall (merge) (start)
     ld [%fp + offset], %l2     ! push nums
     store %l2, %o0      ! arg0 :=pop
     ld [%fp + offset], %l2     ! push p
     store %l2, %o1      ! arg1 :=pop
     ld [%fp + offset], %l2     ! push q
     store %l2, %o2      ! arg2 :=pop
     ld [%fp + offset], %l2     ! push r
     store %l2, %o3      ! arg3 :=pop
     call .merge
     mov %l2, %o0     ! push merge(arg0, arg4)
! funcall (end)

 .L2:

! ifthen (end)

.L1
     ret
     restore

! function: mrgsort (end) 


! function: print_arr (start) 

 .global print_arr
     save %sp, -72, %sp

! assign (start)
     mov 0, %l2      ! push constant value
     st %l2, [%fp + offset]     ! i := pop
! assign (end)

! while (start)

 .L14:

     ld [%fp + offset], %l3     ! push i
     ld [%fp + offset], %l4     ! push nnums
     cmp %l4, %l3
     bl .L16     ! <
     mov 1, %l3
     mov 0, %l3
 .L16:
     cmp %l3, %g0     ! relop:= pop
     be .L15     ! if not relop: goto .L15
     nop
! write (start)
     ld [%fp + offset], %l3     ! push i
     sll %l3, 2, %l3
     add %fp, %l3, %l3      ! index := pop
     ld [%l3 + offset], %l3     ! push nums[index] !     expr := pop
!     write(expr)
!     call flwritei(int)
     mov %%l3, %o0
     call flwritei
     nop
! write (end)

! print (start)
! call flprint()
     sethi %hi(.L17), %o0
     or %o0, %lo(.L17), %o0
     call flprint
     nop
! print (end)

     ba  .L14     ! goto .L14
     nop

 .L15:

! while (end)

! print (start)
! call flprint()
     sethi %hi(.L18), %o0
     or %o0, %lo(.L18), %o0
     call flprint
     nop
! print (end)

.L13
     ret
     restore

! function: print_arr (end) 


! function: main (start) 

 .global main
     save %sp, -152, %sp

! assign (start)
     mov 0, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 17, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 1, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 33, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 2, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 9, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 3, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 103, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 4, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 63, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 5, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 64, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 6, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 202, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 7, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 5, %l2      ! push constant value
     sub %g0, %l2, %l2     ! Unary minus
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 8, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 73, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 9, %l2      ! push constant value
     sll %l2, 2, %l2
     add %fp, %l2, %l2      ! index := pop
     mov 9, %l2      ! push constant value
     st %l2, [%l2 + offset]     ! nums[index] := pop
! assign (end)

! assign (start)
     mov 0, %l2      ! push constant value
     st %l2, [%fp + offset]     ! i := pop
! assign (end)

! print (start)
! call flprint()
     sethi %hi(.L20), %o0
     or %o0, %lo(.L20), %o0
     call flprint
     nop
! print (end)

! funcall (print_arr) (start)
     ld [%fp + offset], %l3     ! push nums
     store %l3, %o0      ! arg0 :=pop
     mov 10, %l3      ! push constant value
     store %l3, %o1      ! arg1 :=pop
     call .print_arr
     mov %l3, %o0     ! push print_arr(arg0, arg2)
! funcall (end)

! funcall (mrgsort) (start)
     ld [%fp + offset], %l4     ! push nums
     store %l4, %o0      ! arg0 :=pop
     mov 0, %l4      ! push constant value
     store %l4, %o1      ! arg1 :=pop
     mov 9, %l4      ! push constant value
     store %l4, %o2      ! arg2 :=pop
     call .mrgsort
     mov %l4, %o0     ! push mrgsort(arg0, arg3)
! funcall (end)

! funcall (print_arr) (start)
     ld [%fp + offset], %l5     ! push nums
     store %l5, %o0      ! arg0 :=pop
     mov 10, %l5      ! push constant value
     store %l5, %o1      ! arg1 :=pop
     call .print_arr
     mov %l5, %o0     ! push print_arr(arg0, arg2)
! funcall (end)

.L19
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L17: .asciz " "
.L18: .asciz "_NL_"
.L20: .asciz "lista desordenada es:_NL_"

