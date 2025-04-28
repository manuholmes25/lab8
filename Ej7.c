//*****************************************************************************
//
// Ej7.c - Secuencia cíclica de 3 LEDs conectados a PL0, PL1 y PL2
// EK-TM4C1294XL
//
//*****************************************************************************

#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"

//*****************************************************************************
//
// Error routine
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif

//*****************************************************************************
//
// Main program
//
//*****************************************************************************
int
main(void)
{
    //
    // Configurar el reloj del sistema:
    // - Oscilador principal con cristal de 25MHz
    // - Uso de PLL
    // - Frecuencia del sistema a 120MHz
    //
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | 
                        SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);

    //
    // 1. Habilitar el periférico GPIO del puerto L
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);

    //
    // 2. Esperar a que el puerto L esté listo
    //
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOL)) {}

    //
    // 3. Configurar PL0, PL1 y PL2 como salidas digitales
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTL_BASE, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2);

    //
    // 4. Bucle infinito para secuencia de LEDs
    //
    while(1)
    {
        //
        // Encender LED en PL0 (Rojo)
        //
        GPIOPinWrite(GPIO_PORTL_BASE, GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTL_BASE, GPIO_PIN_1 | GPIO_PIN_2, 0x0);
        SysCtlDelay((120000000/3) * 10); // 10 segundos

        //
        // Encender LED en PL1 (Amarillo)
        //
        GPIOPinWrite(GPIO_PORTL_BASE, GPIO_PIN_1, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTL_BASE, GPIO_PIN_0 | GPIO_PIN_2, 0x0);
        SysCtlDelay((120000000/3) * 10); // 10 segundos

        //
        // Encender LED en PL2 (Verde)
        //
        GPIOPinWrite(GPIO_PORTL_BASE, GPIO_PIN_2, GPIO_PIN_2);
        GPIOPinWrite(GPIO_PORTL_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0x0);
        SysCtlDelay((120000000/3) * 10); // 10 segundos
    }
}

