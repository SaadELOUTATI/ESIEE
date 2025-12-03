        AREA |.text|, CODE, READONLY
        EXPORT __main
        IMPORT MOTEUR_INIT
        IMPORT MOTEUR_GAUCHE_AVANT
        IMPORT MOTEUR_DROIT_AVANT
        IMPORT MOTEUR_GAUCHE_ARRIERE
        IMPORT MOTEUR_DROIT_ARRIERE
        IMPORT MOTEUR_GAUCHE_ON
        IMPORT MOTEUR_DROIT_ON
        IMPORT MOTEUR_GAUCHE_OFF
        IMPORT MOTEUR_DROIT_OFF
        IMPORT BUMPERS_INIT
        IMPORT READ_BUMPER1
        IMPORT READ_BUMPER2
        IMPORT LEDS_INIT
        IMPORT LEDS_ON
        IMPORT LEDS_OFF
        IMPORT LED4_ON
        IMPORT LED5_ON
        IMPORT SWITCH_INIT
        IMPORT READ_SWITCH1
        IMPORT READ_SWITCH2

;=====================================================
; Variables : indicateur de clignotement (0 = off, 1 = on)
;=====================================================
        AREA |.bss|, NOINIT, READWRITE
flag_cligno   SPACE 4

;=====================================================
; Programme principal
;=====================================================
        AREA |.text|, CODE, READONLY
__main
        BL MOTEUR_INIT
        BL BUMPERS_INIT
        BL LEDS_INIT
        BL SWITCH_INIT
        BL LEDS_OFF

;---------------------------------------------
; Attente du clic sur switch 1 pour démarrer
;---------------------------------------------
attente_start
        BL READ_SWITCH1
        BEQ start_robot
        B attente_start

;---------------------------------------------
; Lancement de la marche normale
;---------------------------------------------
start_robot
        BL MOTEUR_GAUCHE_AVANT
        BL MOTEUR_DROIT_AVANT
        BL MOTEUR_GAUCHE_ON
        BL MOTEUR_DROIT_ON
        MOV R4, #0                  ; flag_cligno = 0
        LDR R5, =flag_cligno
        STR R4, [R5]

main_loop
        
        BL READ_SWITCH2
        BEQ toggle_cligno

        ; Gestion LEDs (si flag_cligno = 1 ? clignote rapide)
        LDR R5, =flag_cligno
        LDR R4, [R5]
        CMP R4, #1
        BNE no_cligno
        BL LEDS_ON
        BL WAIT_URGENCE
        BL LEDS_OFF
        BL WAIT_URGENCE
        B skip_leds
no_cligno
        BL LEDS_OFF
skip_leds

        ; Vérifie bumpers
        BL READ_BUMPER1
        BEQ bumper_gauche
        BL READ_BUMPER2
        BEQ bumper_droit

        B main_loop

;---------------------------------------------
; Toggle clignotement (switch 2)
;---------------------------------------------
toggle_cligno
        LDR R5, =flag_cligno
        LDR R4, [R5]
        CMP R4, #0
        BEQ set_on
        MOV R4, #0
        STR R4, [R5]
        B wait_release2

set_on
        MOV R4, #1
        STR R4, [R5]

wait_release2
        ; attendre que switch 2 soit relâché pour éviter rebond
        BL READ_SWITCH2
        BEQ wait_release2
        B main_loop


;---------------------------------------------
; Réactions bumpers + clignotement directionnel
;---------------------------------------------
bumper_gauche
        BL MOTEUR_GAUCHE_OFF
        BL MOTEUR_DROIT_OFF
        BL WAIT

        ; recule
        BL MOTEUR_GAUCHE_ARRIERE
        BL MOTEUR_DROIT_ARRIERE
        BL MOTEUR_GAUCHE_ON
        BL MOTEUR_DROIT_ON
        BL WAIT_RECULE
        BL MOTEUR_GAUCHE_OFF
        BL MOTEUR_DROIT_OFF
        BL WAIT

        ; allume clignotant gauche (LED4)
cligno_gauche
        BL LED5_ON
        BL WAIT_CLIGNO_LENT
        BL LEDS_OFF
        BL WAIT_CLIGNO_LENT
        ; répéter pendant la rotation
        BL MOTEUR_DROIT_AVANT
        BL MOTEUR_GAUCHE_ARRIERE
        BL MOTEUR_GAUCHE_ON
        BL MOTEUR_DROIT_ON
        BL WAIT_TOURNE
        BL MOTEUR_GAUCHE_OFF
        BL MOTEUR_DROIT_OFF
        BL LEDS_OFF

        ; reprend la marche
        BL MOTEUR_GAUCHE_AVANT
        BL MOTEUR_DROIT_AVANT
        BL MOTEUR_GAUCHE_ON
        BL MOTEUR_DROIT_ON
        B main_loop


bumper_droit
        BL MOTEUR_GAUCHE_OFF
        BL MOTEUR_DROIT_OFF
        BL WAIT

        ; recule
        BL MOTEUR_GAUCHE_ARRIERE
        BL MOTEUR_DROIT_ARRIERE
        BL MOTEUR_GAUCHE_ON
        BL MOTEUR_DROIT_ON
        BL WAIT_RECULE
        BL MOTEUR_GAUCHE_OFF
        BL MOTEUR_DROIT_OFF
        BL WAIT

        ; allume clignotant droit (LED5)
cligno_droit
        BL LED4_ON
        BL WAIT_CLIGNO_LENT
        BL LEDS_OFF
        BL WAIT_CLIGNO_LENT
        ; répéter pendant la rotation
        BL MOTEUR_GAUCHE_AVANT
        BL MOTEUR_DROIT_ARRIERE
        BL MOTEUR_GAUCHE_ON
        BL MOTEUR_DROIT_ON
        BL WAIT_TOURNE
        BL MOTEUR_GAUCHE_OFF
        BL MOTEUR_DROIT_OFF
        BL LEDS_OFF

        ; reprend la marche
        BL MOTEUR_GAUCHE_AVANT
        BL MOTEUR_DROIT_AVANT
        BL MOTEUR_GAUCHE_ON
        BL MOTEUR_DROIT_ON
        B main_loop


;---------------------------------------------
; Temporisations
;---------------------------------------------
WAIT
        LDR R7, =0x3FFFFF
wait1   SUBS R7, #1
        BNE wait1
        BX LR

WAIT_TOURNE
        LDR R1, =0x15FFFFF
wait_turn
        SUBS R1, #1
        BNE wait_turn
        BX LR

WAIT_RECULE
        LDR R2, =0x4FFFFF
wait_back
        SUBS R2, #1
        BNE wait_back
        BX LR

WAIT_URGENCE
        LDR R3, =0x0FFFFF
wait_urg
        SUBS R3, #1
        BNE wait_urg
        BX LR

WAIT_CLIGNO_LENT
        LDR R0, =0x4FFFFF      ; clignotement plus lent
wait_slow
        SUBS R0, #1
        BNE wait_slow
        BX LR

        END
