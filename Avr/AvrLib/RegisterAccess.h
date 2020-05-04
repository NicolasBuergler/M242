#ifndef _REG_ACCESS_H_
#define _REG_ACCESS_H_


#define BitMask_1    0x01
#define BitMask_2    0x03
#define BitMask_3    0x07
#define BitMask_4    0x0F
#define BitMask_5    0x1F
#define BitMask_6    0x3F
#define BitMask_7    0x7F
#define BitMask_8    0xFF




/**
* concatenation
*/
#define __concat( x, y )    x ## y
#define concat( x, y)    __concat( x, y)

/** 
* count arguments
*/
#define __COUNT__(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, ...) a17
#define ARG_COUNT( ... ) __COUNT__(__VA_ARGS__,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1)

/**
* multiple or; this comes handy in when we need to compute the bitmask of several register fields
*/
#define __or(a1, a2, a3, a4, a5, a6, a7, a8, ... )	(a1|a2|a3|a4|a5|a6|a7|a8)
#define OR(...)	__or( __VA_ARGS__, 0,0,0,0,0,0,0,0 )





#define BitMask(width,pos)    (concat(BitMask_, width)<<pos)


// die nachfolgenden zwei macros entsprechen der Musterlösung für die Übungen
#define ReadRegister( reg, width, pos)	((reg & BitMask(width,pos))>>pos)



#define ModifyRegister( reg, width, pos, value)    reg = (((reg)&~BitMask(width, pos))|((value<<pos)&BitMask(width, pos )))

#define ReadRegisterField(reg, field ) ReadRegister( reg, concat(field,width), concat(field,pos))

#define ModRegField( reg, ... ) __modifyRegField(reg, OR(GetBitmask(__VA_ARGS__)), OR(GetValue(__VA_ARGS__)))
#define __modifyRegField(reg, bitmask, values ) reg = (uint8_t)(((reg)&~(bitmask)) |((bitmask)&(values)))


#define GetValue(...) concat( GetValue_, ARG_COUNT(__VA_ARGS__))(__VA_ARGS__)
#define GetValue_1(field) __getValue field
#define __getValue(name, value) ((value)<<concat(name,_pos))
#define GetValue_2(field1, field2) GetValue_1(field1), GetValue_1(field2)
#define GetValue_3(field1, field2, field3) GetValue_1(field1), GetValue_2(field2, field3)
#define GetValue_4(field1, field2, field3, field4) GetValue_1(field1), GetValue_3(field2, field3, field4)
#define GetValue_5(field1, field2, field3, field4, field5) GetValue_1(field1), GetValue_4(field2, field3, field4, field5)
#define GetValue_6(field1, field2, field3, field4, field5, field6) GetValue_1(field1), GetValue_5(field2, field3, field4, field5, field6)
#define GetValue_7(field1, field2, field3, field4, field5, field6, field7) GetValue_1(field1), GetValue_6(field2, field3, field4, field5, field6)


#define GetBitmask(...) concat( GetBitmask_, ARG_COUNT(__VA_ARGS__))(__VA_ARGS__)
#define GetBitmask_1(field) __getBitmask field
#define __getBitmask(name, value) BitMask(concat(name,_width), concat(name, _pos))
#define GetBitmask_2(field1, field2 ) GetBitmask_1(field1), GetBitmask_1(field2)
#define GetBitmask_3(field1, field2, field3 ) GetBitmask_1(field1), GetBitmask_2(field2, field3)
#define GetBitmask_4(field1, field2, field3, field4 ) GetBitmask_1(field1), GetBitmask_3(field2, field3, field4)
#define GetBitmask_5(field1, field2, field3, field4, field5 ) GetBitmask_1(field1), GetBitmask_4(field2, field3, field4, field5)
#define GetBitmask_6(field1, field2, field3, field4, field5, field6 ) GetBitmask_1(field1), GetBitmask_5(field2, field2, field3, field4, field5, field6)
#define GetBitmask_7(field1, field2, field3, field4, field5, field6, field7 ) GetBitmask_1(field1), GetBitmask_6(field2, field2, field3, field4, field5, field6, field7)




/**
* now comes the real hardware description
*/
// fields of port
// data direction

#define DdrInput 0	
#define DdrOutput 1

#define DataDirection(port) concat(DDR,port)

// pin descriptions; this is trivial but i want to be consistent!
#define Pin0_width 1
#define Pin0_pos 0

#define Pin1_width 1
#define Pin1_pos 1

#define Pin2_width 1
#define Pin2_pos 2

#define Pin3_width 1
#define Pin3_pos 3

#define Pin4_width 1
#define Pin4_pos 4

#define Pin5_width 1
#define Pin5_pos 5

#define Pin6_width 1
#define Pin6_pos 6

#define Pin7_width 1
#define Pin7_pos 7


#endif