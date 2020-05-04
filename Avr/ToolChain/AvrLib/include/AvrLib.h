/***
 * AvrLib.h
 *
 * Supporting functions for the course ICT M242
 *
 */


#ifndef AVRLIB_H_
#define AVRLIB_H_

 /**************************************************************************************/
 /*                   type definitions                                                 */
 /**************************************************************************************/

#define TRACE(traceStr,...)
#define countof(array)      (sizeof(array)/sizeof(array[0]))


/**************************************************************************************/
/*                   type definitions                                                 */
/**************************************************************************************/


typedef enum
{
	False = 0,
	True = 1
} Bool;

typedef enum
{
    Priority_High,
    Priority_Medium,
    Priority_Low,
    Priority_VeryLow
} Priority;


typedef enum
{
	 PacketType_Undefined = 0,
	 PacketType_LiftSimulatorButton = 2,
	 PacketType_TestCommand = 3,
	 PacketType_TraceMassagePadLen = 0xA8,
	 PacketType_TraceMessage = 0xA5,
} AvrPacketType;


 typedef struct AvrMessage_tag
 {
	 AvrPacketType MsgType;
	 uint8_t Length;
	 uint8_t Payload[8];
 }AvrMessage;


 /**
* @brief Item um Information zwischen verschiedenen Komponenten des Systems auszutauschen.
*
*
*/
 typedef struct Message_tag
 {
     uint8_t Priority;				///< Definiert die Priorität; je kleiner die Zahl, desto grösser die Priorität;
                                    ///  Es sind vier Prioritäten defniert
     uint8_t Id;					///< Id der Meldung
     union
     {
         struct
         {
             uint8_t MsgParamLow;			///< lower byte[0] des Meldungs-Parameters
             uint8_t MsgParamHigh;			///< upper byte[1] des Meldungs-Paramsters
         };
         void* Ptr;                         ///< man kann die Parameter auch als Pointer interpretieren
     };
 }Message;

 /**
 * @brief Prototyp einer Zustandsfunktion
 */
 typedef void (*StateHandler)(const Message* msg);


 /**
* @brief Repräsentiert eine Zustandsmaschine
*
* Eine oder mehrere Zustandsmaschinen können im Framework registriert werden. Beim Auftreten einer Meldung werden alle
* Zustandsmaschinen, welche auf diese *EventSource* registriert sind, notifiziert
*/
 typedef struct Fsm_tag
 {
     struct Fsm_tag* Next;			///< nächste registrierte Zustanndsmaschine; internal use only!
     uint8_t RxMask;			    ///< Maske, welche angibt, welche *Prioritäyten* bearbeitet werden sollen
     StateHandler CurrentState;		///< Funktion, welche den aktuellen Zustand representiert
 }Fsm;



/**************************************************************************************/
/*                   Funktion Prototypes                                              */
/**************************************************************************************/

/**
* @brief Registriert eine Zustandsmaschine im Framework
* @param fsm Zustandsmaschine, welche registriert werden soll
*/
void RegisterFsm(Fsm* fsm);

/**
* @brief Funktion für das Ausführen eine *Zustandübergangs*
*
* @param fsm Zuststandsmaschine, welche den Zustandsübergang ausführen soll
* @param state Funktion, welche den neuen Zustand implementiert
*/
void SetState(Fsm* fsm, StateHandler state);


/**
* @brief Funktion zum Senden einer Meldung
*
* @param prio Priorität, mit welcher die Meldung bearbeitet werden soll
* @param id Id der Meldung
* @param msgLow low byte des Meldungs-Parameters
* @param msgHigh upper byte des Meldungs-Parameters
*/
void SendMessage(uint8_t prio, uint8_t id, uint8_t msgLow, uint8_t msgHigh);

/**
* @brief Funktion um ein event an die registrierten Zustandsmaschinen zu verteilen
*
* @return Status welcher angibt, ob die Meldungsqueue leer war;
*  - False: es war keine Meldung in der Queue;
*  - True: eine Meldung wurde dispatched.
* Der return wert kann sinnvoll sein, um den Prozessor in den sleep mode zu stellen.
*/
Bool DispatchEvent(void);

/**
* @brief initialize port D to use the uart
*/
void Usart_Init(uint32_t baudrate);

/**
* Don't bother about these implementations; you should not use them directly;
* that's up to the build process!
*/
void Usart_Trace0(uint16_t id );
void Usart_Trace1(uint16_t id, uint8_t val);
void Usart_Trace2(uint16_t id, uint8_t val1, uint8_t val2);
void Usart_Trace3(uint16_t id, uint8_t val1, uint8_t val2, uint8_t val3);
void Usart_Trace4(uint16_t id, uint8_t val1, uint8_t val2, uint8_t val3, uint8_t val4);

/**
* @brief Put one charactor to the Uart
*
* This might be useful in case we are very time critical with tracing!
*/
void Usart_PutChar(char ch);

/**
* @brief Guarantee exclusive access!
*/
void EnterAtomic(void);

void LeaveAtomic(void);


#endif /* AVRLIB_H_ */
