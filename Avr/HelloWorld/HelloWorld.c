#include <avr\io.h>
#include <Atmega328P.h>
#define F_CPU 16000000
#include <avrlib.h>
#include <util\delay.h>

#include <inttypes.h>

int main(void)
{
	Usart_Init(250000);

	while (True)
	{
		TRACE("Hello World");
		_delay_ms(1000);
	}
	
	return 0;
}