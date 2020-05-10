#include <avr\io.h>
#include <Atmega328P.h>
#define F_CPU 16000000
#include <avrlib.h>
#include <util\delay.h>

#include <inttypes.h>

int main(void)
{
	Usart_Init(250000);
	//Setzt die Datenflussrichtung vom Pin 5 vom Port B auf Output 
	SetRegister(PortB.DDR, (PIN5, DdrOutput));

	while (True)
	{
		//LED einschalten
		_delay_ms(1000);
		//LED Ausschalten
		_delay_ms(1000);
	}

	return 0;
}