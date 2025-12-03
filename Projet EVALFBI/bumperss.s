        AREA    |.text|, CODE, READONLY
        THUMB
        PRESERVE8

;================= BUMPERS (Port E) =================

SYSCTL_PERIPH_GPIO  EQU     0x400FE108
GPIO_PORTE_BASE     EQU     0x40024000
GPIO_O_DIR          EQU     0x00000400
GPIO_O_DEN          EQU     0x0000051C
GPIO_I_PUR          EQU     0x00000510

BROCHE0             EQU     0x01           ; PE0
BROCHE1             EQU     0x02           ; PE1
BROCHE0_1           EQU     0x03           ; PE0+PE1

        EXPORT  BUMPERS_INIT
        EXPORT  READ_BUMPER1
        EXPORT  READ_BUMPER2
        EXPORT  READ_BUMPERS

;================= BUMPERS_INIT ======================
BUMPERS_INIT
        LDR     R10, =SYSCTL_PERIPH_GPIO
		LDR     R11, [R10]
		ORR     R11, R11, #0x10
		STR     R11, [R10]
        LDR     R11, [R10]                ; synchro clock
        NOP
        NOP
        NOP

        ; pull-up sur PE0..1
        LDR     R10, =GPIO_PORTE_BASE + GPIO_I_PUR
        MOV     R11, #BROCHE0_1
        STR     R11, [R10]

        ; digital enable
        LDR     R10, =GPIO_PORTE_BASE + GPIO_O_DEN
        MOV     R11, #BROCHE0_1
        STR     R11, [R10]

        ; direction = input
        LDR     R10, =GPIO_PORTE_BASE + GPIO_O_DIR
        MOV     R11, #0x00
        STR     R11, [R10]

        BX      LR
		
;================= READ_BUMPER1 ======================
; PE0 : retourne Z=1 si appuyé (niveau 0)
READ_BUMPER1
        LDR     R10, =GPIO_PORTE_BASE + (BROCHE0 << 2)
        LDR     R12, [R10]
        CMP     R12, #0x00
        BX      LR

;================= READ_BUMPER2 ======================

; PE1 : Z=1 si appuyé
READ_BUMPER2
        LDR     R10, =GPIO_PORTE_BASE + (BROCHE1 << 2)
        LDR     R12, [R10]
        CMP     R12, #0x00
        BX      LR

;================= READ_BUMPERS ======================

; PE0&PE1 : Z=1 si les deux à 0
READ_BUMPERS
        LDR     R10, =GPIO_PORTE_BASE + (BROCHE0_1 << 2)
        LDR     R12, [R10]
        CMP     R12, #0x00
        BX      LR

        END
