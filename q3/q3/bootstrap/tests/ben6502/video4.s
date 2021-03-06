;@refs:https://youtu.be/FY3zTUaykVo?t=458
PORTB = $6000 
PORTA = $6001 
; data direction registers
DDRB = $6002
DDRA = $6003

    .org $8000

reset:
    lda #%11111111 ; store direction bits for port B
    sta DDRB

    lda #%11100000 ; store direction bits for port A
    sta DDRA

    lda #$50
    sta PORTB

loop:
    ror
    sta PORTB

    jmp loop

    .org $fffc
    .word reset
    .word $0000