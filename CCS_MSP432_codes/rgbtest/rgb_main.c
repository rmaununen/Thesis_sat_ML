#include "msp.h"

#define red BIT0
#define green BIT1
#define blue BIT2

int main(void)
{
    // Disable the watchdog timer
    WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD;

    // Configure Pin P2.0 as output for LED2 and turn it off initially
    P2->DIR |= red;
    P2->OUT &= ~red;
    P2->DIR |= green;
    P2->OUT &= ~green;
    P2->DIR |= blue;
    P2->OUT &= ~blue;

    while (1)
    {
        // Toggle LED2
        P2->OUT ^= red;
        // Delay
        __delay_cycles(2000000);

        P2->OUT ^= red;
        P2->OUT ^= green;
        // Delay
        __delay_cycles(2000000);

        P2->OUT ^= green;
        P2->OUT ^= blue;
        // Delay
        __delay_cycles(2000000);

        P2->OUT ^= red;
        // Delay
        __delay_cycles(2000000);

        P2->OUT ^= red;
        P2->OUT ^= green;
        // Delay
        __delay_cycles(2000000);

        P2->OUT ^= red;
        P2->OUT ^= blue;
        // Delay
        __delay_cycles(2000000);

        P2->OUT ^= green;
        // Delay
        __delay_cycles(2000000);

        P2->OUT ^= red;
        P2->OUT ^= green;
        P2->OUT ^= blue;
        // Delay
        __delay_cycles(2000000);

    }

}
