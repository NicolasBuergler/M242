/**
* @file: Atmega328P.h
*
* automatically generated; do not edit
*/

#ifndef __Atmega328P_h__
#define __Atmega328P_h__

#include <avr/sfr_defs.h>
#include <avr/common.h>
#include <inttypes.h>

/**
* bitfield SE
*/
#define SMCR_SE_mask 0x01
#define SMCR_SE_pos 0
#define SMCR_SE_width 1

/**
* bitfield SM
*/
#define SMCR_SM_mask 0x0E
#define SMCR_SM_pos 1
#define SMCR_SM_width 3

typedef enum
{
    Idle=0,
    AdcNoiseRed=1,
    PowerDown=2,
    PowerSave=3,
    StandBy=6,
    ExtStandBy=7,
} SleepMode;

/**
* bitfield IVCE
*/
#define MCUCR_IVCE_mask 0x01
#define MCUCR_IVCE_pos 0
#define MCUCR_IVCE_width 1

/**
* bitfield IVSEL
*/
#define MCUCR_IVSEL_mask 0x02
#define MCUCR_IVSEL_pos 1
#define MCUCR_IVSEL_width 1

/**
* bitfield PUD
*/
#define MCUCR_PUD_mask 0x10
#define MCUCR_PUD_pos 4
#define MCUCR_PUD_width 1

/**
* bitfield BODSE
*/
#define MCUCR_BODSE_mask 0x20
#define MCUCR_BODSE_pos 5
#define MCUCR_BODSE_width 1

/**
* bitfield BODS
*/
#define MCUCR_BODS_mask 0x40
#define MCUCR_BODS_pos 6
#define MCUCR_BODS_width 1

typedef struct GPIO_T_tag
{
    volatile uint8_t PIN;
    volatile uint8_t DDR;
    volatile uint8_t PORT;
} GPIO_T;
/**
* bitfield 0
*/
#define PIN_0_mask 0x01
#define PIN_0_pos 0
#define PIN_0_width 1

/**
* bitfield _1
*/
#define PIN_1_mask 0x02
#define PIN_1_pos 1
#define PIN_1_width 1

/**
* bitfield _2
*/
#define PIN_2_mask 0x04
#define PIN_2_pos 2
#define PIN_2_width 1

/**
* bitfield _3
*/
#define PIN_3_mask 0x08
#define PIN_3_pos 3
#define PIN_3_width 1

/**
* bitfield _4
*/
#define PIN_4_mask 0x10
#define PIN_4_pos 4
#define PIN_4_width 1

/**
* bitfield _5
*/
#define PIN_5_mask 0x20
#define PIN_5_pos 5
#define PIN_5_width 1

/**
* bitfield _6
*/
#define PIN_6_mask 0x40
#define PIN_6_pos 6
#define PIN_6_width 1

/**
* bitfield _7
*/
#define PIN_7_mask 0x80
#define PIN_7_pos 7
#define PIN_7_width 1

typedef enum
{
    DdrInput=0,
    DdrOutput=1,
} DataDirection_T;

typedef struct TCNT8_T_tag
{
    volatile uint8_t TCCRA;
    volatile uint8_t TCCRB;
    volatile uint8_t TCNT;
    volatile uint8_t OCRA;
    volatile uint8_t OCRB;
} TCNT8_T;
/**
* bitfield WGM
*/
#define TCCRA_WGM_mask 0x03
#define TCCRA_WGM_pos 0
#define TCCRA_WGM_width 2

/**
* bitfield COMB
*/
#define TCCRA_COMB_mask 0x30
#define TCCRA_COMB_pos 4
#define TCCRA_COMB_width 2

/**
* bitfield COMA
*/
#define TCCRA_COMA_mask 0xC0
#define TCCRA_COMA_pos 6
#define TCCRA_COMA_width 2

typedef enum
{
    Normal=0,
    PwmNormal=1,
    ClrTmrOnCmpMatch=2,
    FastPwm=3,
} WaveFormGenerationModes;

/**
* bitfield CS
*/
#define TCCRB_CS_mask 0x07
#define TCCRB_CS_pos 0
#define TCCRB_CS_width 3

/**
* bitfield WGM
*/
#define TCCRB_WGM_mask 0x08
#define TCCRB_WGM_pos 3
#define TCCRB_WGM_width 1

/**
* bitfield Reserved
*/
#define TCCRB_Reserved_mask 0x30
#define TCCRB_Reserved_pos 4
#define TCCRB_Reserved_width 2

/**
* bitfield FOCB
*/
#define TCCRB_FOCB_mask 0x40
#define TCCRB_FOCB_pos 6
#define TCCRB_FOCB_width 1

/**
* bitfield FOCA
*/
#define TCCRB_FOCA_mask 0x80
#define TCCRB_FOCA_pos 7
#define TCCRB_FOCA_width 1

typedef enum
{
    CS_Off=0,
    CS_Div1=1,
    CS_Div8=2,
    CsT1_Div64=3,
    CsT1_Div256=4,
    CsT1_Div1024=5,
    CsT1_T0Falling=6,
    CsT1_T0Raising=7,
    CsT2_Div32=3,
    CsT2_Div64=4,
    CsT2_Div128=5,
    CsT2_Div256=6,
    CsT2_Div1024=7,
} ClkSelect;

typedef struct TCNT16_T_tag
{
    volatile uint8_t TCCRA;
    volatile int8_t TCCRB;
    volatile uint8_t TCCRC;
    volatile uint8_t Reserved;
    volatile uint16_t TCNT;
    volatile uint16_t ICR;
    volatile uint16_t OCRA;
    volatile uint16_t ORCB;
} TCNT16_T;
/**
* bitfield WGM
*/
#define TCCRA1_WGM_mask 0x03
#define TCCRA1_WGM_pos 0
#define TCCRA1_WGM_width 2

/**
* bitfield COM1B
*/
#define TCCRA1_COM1B_mask 0x30
#define TCCRA1_COM1B_pos 4
#define TCCRA1_COM1B_width 2

/**
* bitfield COM1A
*/
#define TCCRA1_COM1A_mask 0xC0
#define TCCRA1_COM1A_pos 6
#define TCCRA1_COM1A_width 2

/**
* bitfield CS
*/
#define TCCRB1_CS_mask 0x07
#define TCCRB1_CS_pos 0
#define TCCRB1_CS_width 3

/**
* bitfield WGM
*/
#define TCCRB1_WGM_mask 0x30
#define TCCRB1_WGM_pos 4
#define TCCRB1_WGM_width 2

/**
* bitfield ICES1
*/
#define TCCRB1_ICES1_mask 0x40
#define TCCRB1_ICES1_pos 6
#define TCCRB1_ICES1_width 1

/**
* bitfield ICNC1
*/
#define TCCRB1_ICNC1_mask 0x80
#define TCCRB1_ICNC1_pos 7
#define TCCRB1_ICNC1_width 1

/**
* bitfield FOC1B
*/
#define TCCRC1_FOC1B_mask 0x40
#define TCCRC1_FOC1B_pos 6
#define TCCRC1_FOC1B_width 1

/**
* bitfield FOC1A
*/
#define TCCRC1_FOC1A_mask 0x80
#define TCCRC1_FOC1A_pos 7
#define TCCRC1_FOC1A_width 1

/**
* bitfield TOV
*/
#define TIFR_TOV_mask 0x01
#define TIFR_TOV_pos 0
#define TIFR_TOV_width 1

/**
* bitfield OCFA
*/
#define TIFR_OCFA_mask 0x02
#define TIFR_OCFA_pos 1
#define TIFR_OCFA_width 1

/**
* bitfield OCFB
*/
#define TIFR_OCFB_mask 0x04
#define TIFR_OCFB_pos 2
#define TIFR_OCFB_width 1

/**
* bitfield ICF
*/
#define TIFR_ICF_mask 0x20
#define TIFR_ICF_pos 5
#define TIFR_ICF_width 1

typedef struct USART_T_tag
{
    volatile uint8_t UCSRA;
    volatile uint8_t UCSRB;
    volatile uint8_t UCSRC;
    volatile uint8_t Reserved;
    volatile uint16_t UBBR;
    volatile uint8_t UDR;
} USART_T;
/**
* bitfield RXC
*/
#define UCSRA_RXC_mask 0x80
#define UCSRA_RXC_pos 7
#define UCSRA_RXC_width 1

/**
* bitfield TXC
*/
#define UCSRA_TXC_mask 0x40
#define UCSRA_TXC_pos 6
#define UCSRA_TXC_width 1

/**
* bitfield UDRE
*/
#define UCSRA_UDRE_mask 0x20
#define UCSRA_UDRE_pos 5
#define UCSRA_UDRE_width 1

/**
* bitfield FE
*/
#define UCSRA_FE_mask 0x10
#define UCSRA_FE_pos 4
#define UCSRA_FE_width 1

/**
* bitfield DOR
*/
#define UCSRA_DOR_mask 0x08
#define UCSRA_DOR_pos 3
#define UCSRA_DOR_width 1

/**
* bitfield UPE
*/
#define UCSRA_UPE_mask 0x04
#define UCSRA_UPE_pos 2
#define UCSRA_UPE_width 1

/**
* bitfield U2X
*/
#define UCSRA_U2X_mask 0x02
#define UCSRA_U2X_pos 1
#define UCSRA_U2X_width 1

/**
* bitfield MPCM
*/
#define UCSRA_MPCM_mask 0x02
#define UCSRA_MPCM_pos 1
#define UCSRA_MPCM_width 1

/**
* bitfield TXB8
*/
#define UCSRB_TXB8_mask 0x01
#define UCSRB_TXB8_pos 0
#define UCSRB_TXB8_width 1

/**
* bitfield RXB8
*/
#define UCSRB_RXB8_mask 0x02
#define UCSRB_RXB8_pos 1
#define UCSRB_RXB8_width 1

/**
* bitfield UCSZ2
*/
#define UCSRB_UCSZ2_mask 0x04
#define UCSRB_UCSZ2_pos 2
#define UCSRB_UCSZ2_width 1

/**
* bitfield TXEN
*/
#define UCSRB_TXEN_mask 0x08
#define UCSRB_TXEN_pos 3
#define UCSRB_TXEN_width 1

/**
* bitfield RXEN
*/
#define UCSRB_RXEN_mask 0x10
#define UCSRB_RXEN_pos 4
#define UCSRB_RXEN_width 1

/**
* bitfield UDRIEN
*/
#define UCSRB_UDRIEN_mask 0x20
#define UCSRB_UDRIEN_pos 5
#define UCSRB_UDRIEN_width 1

/**
* bitfield TXCIEN
*/
#define UCSRB_TXCIEN_mask 0x40
#define UCSRB_TXCIEN_pos 6
#define UCSRB_TXCIEN_width 1

/**
* bitfield RXCIEN
*/
#define UCSRB_RXCIEN_mask 0x80
#define UCSRB_RXCIEN_pos 7
#define UCSRB_RXCIEN_width 1

/**
* bitfield UCPOL
*/
#define UCSRC_UCPOL_mask 0x01
#define UCSRC_UCPOL_pos 0
#define UCSRC_UCPOL_width 1

/**
* bitfield UCSZ01
*/
#define UCSRC_UCSZ01_mask 0x06
#define UCSRC_UCSZ01_pos 1
#define UCSRC_UCSZ01_width 2

/**
* bitfield USBS
*/
#define UCSRC_USBS_mask 0x08
#define UCSRC_USBS_pos 3
#define UCSRC_USBS_width 1

/**
* bitfield UPM
*/
#define UCSRC_UPM_mask 0x30
#define UCSRC_UPM_pos 4
#define UCSRC_UPM_width 2

/**
* bitfield UMSEL
*/
#define UCSRC_UMSEL_mask 0xC0
#define UCSRC_UMSEL_pos 6
#define UCSRC_UMSEL_width 2

typedef enum
{
    NoParityCheck=0,
    EvenParity=2,
    OddParity=3,
} UART_ParityMode;

typedef enum
{
    Asynchronous=0,
    Synchronous=1,
    SpiMaster=3,
} UART_ModeSelect;

/**
* bitfield UBRR
*/
#define UBBR_UBRR_mask 0x0FFF
#define UBBR_UBRR_pos 0
#define UBBR_UBRR_width 12

typedef struct ADC_T_tag
{
    volatile uint16_t Data;
    volatile uint8_t Adcsra;
    volatile uint8_t Adcsrb;
    volatile uint8_t Admux;
    volatile uint8_t Reserved;
    volatile uint8_t Didr0;
    volatile uint8_t Didr1;
} ADC_T;
/**
* bitfield ADPS
*/
#define ADCSRA_ADPS_mask 0x07
#define ADCSRA_ADPS_pos 0
#define ADCSRA_ADPS_width 3

/**
* bitfield ADIE
*/
#define ADCSRA_ADIE_mask 0x08
#define ADCSRA_ADIE_pos 3
#define ADCSRA_ADIE_width 1

/**
* bitfield ADIF
*/
#define ADCSRA_ADIF_mask 0x10
#define ADCSRA_ADIF_pos 4
#define ADCSRA_ADIF_width 1

/**
* bitfield ADATE
*/
#define ADCSRA_ADATE_mask 0x20
#define ADCSRA_ADATE_pos 5
#define ADCSRA_ADATE_width 1

/**
* bitfield ADSC
*/
#define ADCSRA_ADSC_mask 0x40
#define ADCSRA_ADSC_pos 6
#define ADCSRA_ADSC_width 1

/**
* bitfield ADEN
*/
#define ADCSRA_ADEN_mask 0x80
#define ADCSRA_ADEN_pos 7
#define ADCSRA_ADEN_width 1

typedef enum
{
    AdcDiv2=1,
    AdcDiv4=2,
    AdcDiv8=3,
    AdcDiv16=4,
    AdcDiv32=5,
    AdcDiv64=6,
    AdcDiv128=7,
} AdcPrescaler;

/**
* bitfield ADTS
*/
#define ADCSRB_ADTS_mask 0x07
#define ADCSRB_ADTS_pos 0
#define ADCSRB_ADTS_width 3

/**
* bitfield Reserved345
*/
#define ADCSRB_Reserved345_mask 0x38
#define ADCSRB_Reserved345_pos 3
#define ADCSRB_Reserved345_width 3

/**
* bitfield ACME
*/
#define ADCSRB_ACME_mask 0x40
#define ADCSRB_ACME_pos 6
#define ADCSRB_ACME_width 1

/**
* bitfield Reserved7
*/
#define ADCSRB_Reserved7_mask 0x80
#define ADCSRB_Reserved7_pos 7
#define ADCSRB_Reserved7_width 1

typedef enum
{
    FreeRunning=0,
    AnalogComparator=1,
    ExtInterrupt=2,
    Tc0Compare=3,
    Tc0Overflow=4,
    Tc1Compare=5,
    Tc1Overflow=6,
    Tc1Capture=6,
} AD_AutoTriggerSource;

/**
* bitfield MUX
*/
#define ADMUX_MUX_mask 0x0F
#define ADMUX_MUX_pos 0
#define ADMUX_MUX_width 4

/**
* bitfield Reserve
*/
#define ADMUX_Reserve_mask 0x10
#define ADMUX_Reserve_pos 4
#define ADMUX_Reserve_width 1

/**
* bitfield ADLAR
*/
#define ADMUX_ADLAR_mask 0x20
#define ADMUX_ADLAR_pos 5
#define ADMUX_ADLAR_width 1

/**
* bitfield REFS
*/
#define ADMUX_REFS_mask 0xC0
#define ADMUX_REFS_pos 6
#define ADMUX_REFS_width 2

typedef enum
{
    MuxAdc0=0,
    MuxAdc1=1,
    MuxAdc2=2,
    MuxAdc3=3,
    MuxAdc4=4,
    MuxAdc5=5,
    MuxAdc6=6,
    MuxAdc7=7,
    MuxTemp=8,
    Mux11V=14,
    MuxGnd=15,
} AnalogChannelSelection;

/**
* bitfield ADC0D
*/
#define DIDR0_ADC0D_mask 0x01
#define DIDR0_ADC0D_pos 0
#define DIDR0_ADC0D_width 1

/**
* bitfield ADC1D
*/
#define DIDR0_ADC1D_mask 0x02
#define DIDR0_ADC1D_pos 1
#define DIDR0_ADC1D_width 1

/**
* bitfield ADC2D
*/
#define DIDR0_ADC2D_mask 0x04
#define DIDR0_ADC2D_pos 2
#define DIDR0_ADC2D_width 1

/**
* bitfield ADC3D
*/
#define DIDR0_ADC3D_mask 0x08
#define DIDR0_ADC3D_pos 3
#define DIDR0_ADC3D_width 1

/**
* bitfield ADC4D
*/
#define DIDR0_ADC4D_mask 0x10
#define DIDR0_ADC4D_pos 4
#define DIDR0_ADC4D_width 1

/**
* bitfield ADC5D
*/
#define DIDR0_ADC5D_mask 0x20
#define DIDR0_ADC5D_pos 5
#define DIDR0_ADC5D_width 1

/**
* bitfield Reserved67
*/
#define DIDR0_Reserved67_mask 0xC0
#define DIDR0_Reserved67_pos 6
#define DIDR0_Reserved67_width 2

/**
* bitfield AIN0D
*/
#define DIDR1_AIN0D_mask 0x01
#define DIDR1_AIN0D_pos 0
#define DIDR1_AIN0D_width 1

/**
* bitfield AIN1D
*/
#define DIDR1_AIN1D_mask 0x02
#define DIDR1_AIN1D_pos 1
#define DIDR1_AIN1D_width 1

/**
* bitfield TOIE
*/
#define TIMSK_TOIE_mask 0x01
#define TIMSK_TOIE_pos 0
#define TIMSK_TOIE_width 1

/**
* bitfield OCIEA
*/
#define TIMSK_OCIEA_mask 0x02
#define TIMSK_OCIEA_pos 1
#define TIMSK_OCIEA_width 1

/**
* bitfield OCIEB
*/
#define TIMSK_OCIEB_mask 0x04
#define TIMSK_OCIEB_pos 2
#define TIMSK_OCIEB_width 1

/**
* bitfield ICIE
*/
#define TIMSK_ICIE_mask 0x20
#define TIMSK_ICIE_pos 5
#define TIMSK_ICIE_width 1

#define PortB (*((volatile GPIO_T*)0x00000023))
#define PortC (*((volatile GPIO_T*)0x00000026))
#define PortD (*((volatile GPIO_T*)0x00000029))
#define Tifr0 (*((volatile uint8_t*)0x00000035))
#define Tifr1 (*((volatile uint8_t*)0x00000036))
#define Tifr2 (*((volatile uint8_t*)0x00000037))
#define Tcnt0 (*((volatile TCNT8_T*)0x00000044))
#define Smcr (*((volatile uint8_t*)0x00000053))
#define Mcucr (*((volatile uint8_t*)0x00000055))
#define Timsk0 (*((volatile uint8_t*)0x0000006E))
#define Timsk1 (*((volatile uint8_t*)0x0000006F))
#define Timsk2 (*((volatile uint8_t*)0x00000070))
#define Adc (*((volatile ADC_T*)0x00000078))
#define Tcnt1 (*((volatile TCNT16_T*)0x00000080))
#define Tcnt2 (*((volatile TCNT8_T*)0x000000B0))
#define Usart (*((volatile USART_T*)0x000000C0))
#endif
