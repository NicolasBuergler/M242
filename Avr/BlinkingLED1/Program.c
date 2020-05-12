#include <avr\io.h>
#include <Atmega328P.h>
#define F_CPU 16000000
#include <avrlib.h>
#include <util\delay.h>

#include <inttypes.h>

int main(void)
{
	Usart_Init(250000);
	Bool ledOn = False;
	//Setzt die Datenflussrichtung vom Pin 5 vom Port B auf Output 
	SetRegister(PortB.DDR, (PIN5, DdrInput), PortB.DDR, (PIN4, DdrOutput), PortB.DDR, (PIN3, DdrOutput));
	SetRegister(PortB.PORT, (PIN3, ledOn), (PIN4, 0));


	while (True)
	{
		ledOn = !ledOn;
		UpdateRegister(PortB.PORT, (PIN3, ledOn));
		_delay_ms(1000);
	}

	return 0;
}