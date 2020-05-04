#ifndef __MACRODEFS_14__
#define __MACRODEFS_14__

#define count0  0
#define count1  0,0
#define count2  0,0,0
#define count3  0,0,0,0
#define count4  0,0,0,0,0
#define count5  0,0,0,0,0,0
#define count6  0,0,0,0,0,0,0
#define count7  0,0,0,0,0,0,0,0
#define count8  0,0,0,0,0,0,0,0,0

#define Pad( a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11 ... ) a11
#define PadNum(...) Pad(__VA_ARGS__, 0,1,2,3,4,5,6,7)



#define cat(x,y) x ## y
#define xcat(x,y) cat(x,y)
#define REPEAT0(x)
#define REPEAT1(x) x
#define REPEAT2(x) x ## x
#define REPEAT3(x) REPEAT1(x) ## REPEAT2(x)
#define REPEAT4(x) REPEAT2(x) ## REPEAT2(x)
#define REPEAT5(x) REPEAT3(x) ## REPEAT2(x)
#define REPEAT6(x) REPEAT3(x) ## REPEAT3(x)
#define REPEAT7(x) REPEAT5(x) ## REPEAT2(x)
#define REPEAT8(x) REPEAT4(x) ## REPEAT4(x)

#define bizarre 0x ## 00

#define countN( n )  xcat( count, n )

#define REPEAT_N(x,n) xcat(REPEAT, n)(x)
#define join(x,y) x ## , ## y
#define xjoin(x,y) join( x, y)
#define PadLeft(x,y) REPEAT_N(0,PadNum(join( xcat(count,x), xcat(count,y))))

//#define bitmask(width, position) xcat( 0, xcat( b , xcat( PadLeft(width, position), xcat( REPEATN(1, width), REPEATN(0, position)))))
#define bitmask(width, position) xcat( 0, xcat( b , xcat( PadLeft(width, position), xcat( REPEAT_N(1, width), REPEAT_N(0, position)))))

#endif
