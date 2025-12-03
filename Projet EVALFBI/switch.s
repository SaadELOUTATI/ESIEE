        AREA    |.text|, CODE, READONLY
        EXPORT  SWITCH_INIT
        EXPORT  READ_SWITCH1
        EXPORT  READ_SWITCH2

;================= CONSTANTES =======================
SYSCTL_PERIPH_GPIO  EQU     0x400FE108      ; SYSCTL_RCGC2_R (Clock gating)
GPIO_PORTD_BASE     EQU     0x40007000      ; Base Port D (APB)
GPIO_O_DEN          EQU     0x0000051C      ; Digital Enable
GPIO_I_PUR          EQU     0x00000510      ; Pull-Up
BROCHE6             EQU     0x40            ; PD6 = bouton 1
BROCHE7             EQU     0x80            ; PD7 = bouton 2
BROCHE6_7           EQU     0xC0            ; PD6 et PD7 ensemble

;================= SWITCH_INIT ======================
SWITCH_INIT
        ; Active l’horloge du port D
        LDR     R0, =SYSCTL_PERIPH_GPIO
        LDR     R1, [R0]
        ORR     R1, R1, #0x00000008         ; bit 3 = port D
        STR     R1, [R0]
        NOP
        NOP
        NOP

        ; Active le Pull-Up sur PD6 et PD7
        LDR     R0, =GPIO_PORTD_BASE
        ADD     R0, R0, #GPIO_I_PUR
        LDR     R1, [R0]
        ORR     R1, R1, #BROCHE6_7
        STR     R1, [R0]

        ; Active la fonction numérique
        LDR     R0, =GPIO_PORTD_BASE
        ADD     R0, R0, #GPIO_O_DEN
        LDR     R1, [R0]
        ORR     R1, R1, #BROCHE6_7
        STR     R1, [R0]

        BX      LR

;================= READ_SWITCH1 ======================
; Retourne dans le drapeau Z le résultat du test (Z=1 si pressé)
READ_SWITCH1
        LDR     R0, =GPIO_PORTD_BASE + (BROCHE6 << 2)
        LDR     R1, [R0]
        CMP     R1, #0x00           ; Si PD6 = 0 -> bouton appuyé
        BX      LR

;================= READ_SWITCH2 ======================
; Retourne dans le drapeau Z le résultat du test (Z=1 si pressé)
READ_SWITCH2
        LDR     R0, =GPIO_PORTD_BASE + (BROCHE7 << 2)
        LDR     R1, [R0]
        CMP     R1, #0x00           ; Si PD7 = 0 -> bouton appuyé
        BX      LR

        END
