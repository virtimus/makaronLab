;@refs:https://youtu.be/xBjQVxVxOxc?t=205

PORTB = $6000 
PORTA = $6001 
; data direction registers
DDRB = $6002
DDRA = $6003

E  = %10000000
RW = %01000000
RS = %00100000

    .org $8000

reset:
    lda #%11111111 ; store direction bits for port B
    sta DDRB

    lda #%11100000 ; store direction bits for port A
    sta DDRA

    lda #%00111000 ; set 8 bit mode; 2-line display; 5x8 font
    jsr lcd_instruction
    lda #%0001110 ; display on; cursor on; blink off
    jsr lcd_instruction
    lda #%0000110 ; increment and shift cursor; dont shift display
    jsr lcd_instruction

    lda #"H"
    jsr print_char
    lda #"E"
    jsr print_char
    lda #"L"
    jsr print_char
    lda #"O"
    jsr print_char

loop:
    jmp loop

lcd_instruction:
    sta PORTB
    lda #0
    sta PORTA
    lda #E
    sta PORTA
    lda #0
    sta PORTA
    rts

print_char:
    sta PORTB
    lda #RS  ; set RS ; clear RW/E bits
    sta PORTA
    lda #(RS | E) ; set E bit to send instruction
    sta PORTA
    lda #RS  ;  clear RW/E bits
    sta PORTA

    .org $fffc
    .word reset
    .word $0000