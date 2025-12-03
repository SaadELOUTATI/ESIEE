        AREA    |.text|, CODE, READONLY
        THUMB
        PRESERVE8

;================= LEDS (Port F) ====================

SYSCTL_PERIPH_GPIO  EQU     0x400FE108
GPIO_PORTF_BASE     EQU     0x40025000
GPIO_O_DIR          EQU     0x00000400
GPIO_O_DEN          EQU     0x0000051C
GPIO_O_DR2R         EQU     0x00000500

BROCHE4             EQU     0x10           ; PF4
BROCHE5             EQU     0x20           ; PF5
BROCHE4_5           EQU     0x30           ; PF4|PF5

        EXPORT  LEDS_INIT
        EXPORT  LEDS_ON
        EXPORT  LEDS_OFF
        EXPORT  LEDS_SWITCH
        EXPORT  LED4_ON
        EXPORT  LED5_ON

;================= LEDS_INIT ======================
LEDS_INIT
        PUSH    {R0, R5, R10, LR}
        LDR     R10, =SYSCTL_PERIPH_GPIO
        LDR     R5, [R10]
        ORR     R5, R5, #0x20              ; clock Port F
        STR     R5, [R10]
        NOP
        NOP
        NOP

        ; DIR = sortie
        LDR     R10, =GPIO_PORTF_BASE + GPIO_O_DIR
        LDR     R5, [R10]
        ORR     R5, R5, #BROCHE4_5
        STR     R5, [R10]

        ; DEN = digital enable
        LDR     R10, =GPIO_PORTF_BASE + GPIO_O_DEN
        LDR     R5, [R10]
        ORR     R5, R5, #BROCHE4_5
        STR     R5, [R10]

        
        LDR     R10, =GPIO_PORTF_BASE + GPIO_O_DR2R
        LDR     R5, [R10]
        ORR     R5, R5, #BROCHE4_5
        STR     R5, [R10]

        POP     {R0, R5, R10, LR}
        BX      LR

; Allumer PF4 et PF5
LEDS_ON
        PUSH    {R0, R10, LR}
        LDR     R10, =GPIO_PORTF_BASE + (BROCHE4_5 << 2)
        MOV     R0, #BROCHE4_5             ; <<— MOV (pas LDR =const)
        STR     R0, [R10]
        POP     {R0, R10, LR}
        BX      LR

; Éteindre PF4 et PF5
LEDS_OFF
        PUSH    {R0, R10, LR}
        LDR     R10, =GPIO_PORTF_BASE + (BROCHE4_5 << 2)
        MOV     R0, #0x00
        STR     R0, [R10]
        POP     {R0, R10, LR}
        BX      LR

; Inverser PF4 et PF5
LEDS_SWITCH
        PUSH    {R0, R10, LR}
        LDR     R10, =GPIO_PORTF_BASE + (BROCHE4_5 << 2)
        LDR     R0, [R10]
        EOR     R0, R0, #BROCHE4_5
        STR     R0, [R10]
        POP     {R0, R10, LR}
        BX      LR

; PF4 seulement
LED4_ON
        PUSH    {R0, R10, LR}
        LDR     R10, =GPIO_PORTF_BASE + (BROCHE4_5 << 2)
        MOV     R0, #BROCHE4               ; <<— MOV
        STR     R0, [R10]
        POP     {R0, R10, LR}
        BX      LR

; PF5 seulement
LED5_ON
        PUSH    {R0, R10, LR}
        LDR     R10, =GPIO_PORTF_BASE + (BROCHE4_5 << 2)
        MOV     R0, #BROCHE5               ; <<— MOV
        STR     R0, [R10]
        POP     {R0, R10, LR}
        BX      LR

        END
