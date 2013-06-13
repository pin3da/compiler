! Creado por mpascal.py
! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)

     .section ".text"

! program

! function: main (start) 

 .global main
     save %sp, -64, %sp

! print (start)
! call flprint()
     sethi %hi(.L1), %o0
     or %o0, %lo(.L1), %o0
     call flprint
     nop
! print (end)

 .Ln:
     mov 0, %o0 ! solamente aparece en main
     call _exit ! solamente aparece en main
     nop ! solamente aparece en main
     ret
     restore

! function: main (end) 


     .section ".rodata"

.L1: .asciz "Hola Mundo_NL_"

