#include <msp.h>
#include <driverlib.h>
#include "Console.h"

#define red BIT0
#define green BIT1
#define blue BIT2

int main(void)
{
    // Disable the watchdog timer
    WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD;

    // initialize the console
    Console::init( 9600 );     // baud rate: 115200 bps

    // Configure Pin P1.0 as output for LED1 and turn it off initially
    P1->DIR |= red;
    P1->OUT &= ~red;

    // Configure Pin P2.0 as output for LED2 and turn it off initially
    P2->DIR |= red;
    P2->OUT &= ~red;
    P2->DIR |= green;
    P2->OUT &= ~green;
    P2->DIR |= blue;
    P2->OUT &= ~blue;

    // Configure Pin P1.1 as input for button1
    P1->DIR &= ~BIT1;
    P1->REN |= BIT1;
    P1->OUT |= BIT1;

    // Configure Pin P1.4 as input for button2
    P1->DIR &= ~BIT4;
    P1->REN |= BIT4;
    P1->OUT |= BIT4;

    Console::log("Hello World");
    while (1)
    {
        // Check if button1 is pressed
        if (!(P1->IN & BIT1))
        {
            // Toggle LED1
            P1->OUT ^= red;
            // Delay
            __delay_cycles(500000);
            Console::log("1");
        }

        // Check if button2 is pressed
        if (!(P1->IN & BIT4))
        {
            // Increment the color state
            int color = (color + 1) % 4;

            // Set the LED2 color based on the state
            switch (color)
            {
                case 0: // Red
                    P2->OUT &= ~green;
                    P2->OUT &= ~blue;
                    P2->OUT |= red;
                    break;
                case 1: // Green
                    P2->OUT &= ~red;
                    P2->OUT &= ~blue;
                    P2->OUT |= green;
                    break;
                case 2: // Blue
                    P2->OUT &= ~red;
                    P2->OUT &= ~green;
                    P2->OUT |= blue;
                    break;
                case 3: // Off
                    P2->OUT &= ~red;
                    P2->OUT &= ~green;
                    P2->OUT &= ~blue;
                    break;
            }

            // Delay
            __delay_cycles(500000);
            Console::log("2");
        }
    }
}
