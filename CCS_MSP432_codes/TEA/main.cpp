//Time Estimation Algorithm (TEA) embedded code

#include <msp.h>
#include <driverlib.h>
#include "Console.h"  //Can be replaced with UART driver
#include <temp_1187.h>
#include <conversion_functions.h>

int main(void)
{
    // ************************************   SETUP   ***********************************
    WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD; // Disable the watchdog timer
    Console::init(115200);     // initialize the console with baud rate 115200 bps
    Console::log("TEA init");

    int time = 0;
    int j = 0;
    float last_min_temp = 50.0; //[deg C]
    const int T_orb = 98; //Specify orbital period [min]

    __delay_cycles(20000000); //20s delay to allow for terminal initialization

    // ************************************   LOOP   ***********************************
    while (1)
    {

      //print current index
      float jf = static_cast<float>(j);
      char js[32];
      float_to_str(js, 32, 1, jf);
      if(j==0){
      Console::log("");
      Console::log("");
      Console::log("index:");
      Console::log(js);
      Console::log("time:");
      }

      //##### ESTIMATE TIME #####
      float avg_t = (therm_data_pX[j] + therm_data_mX[j] + therm_data_pY[j] + therm_data_mY[j])/4.0;

      if (avg_t < last_min_temp){
          time = 0;
          last_min_temp = avg_t;
      }
      else{
          time ++;
      }

      if (time == T_orb){
          time = 0;
          last_min_temp = avg_t;
      }

      //output the time estimate
      float timef = static_cast<float>(time);
      char times[32];
      float_to_str(times, 32, 3, timef);
      Console::log(times);


      //increment index (simulate incremental reception of temperature measurements)
      j++;
      if (j>therm_data_pX_size){
          j = 0;
      }

      //introduce delay
      __delay_cycles(1000000);

    }
}
