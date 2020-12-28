//const int INT24_MAX = 8388607;
//#include "bitset.h"

typedef unsigned char BYTE;

class IntVar
{
protected:
	short bits;
    unsigned char value[3];

public:
    IntVar(short bits){
    	this->bits = bits;
    }

    operator auto() const {
    	return  (bits<=8)?(BYTE)value[0]
			:(bits<=16)?(value[1] <<  8) | value[0]
			:(bits<=32)?(value[2] << 16) | (value[1] <<  8) | value[0]
			:0;
    }

    IntVar(const IntVar& val )
    {
        *this   = val;
    }



 /*   operator int() const
    {
        / * Sign extend negative quantities * /
        if( value[2] & 0x80 ) {
            return (0xff << 24) | (value[2] << 16)
                                | (value[1] <<  8)
                                |  value[0];
        } else {
            return (value[2] << 16)
                 | (value[1] <<  8)
                 |  value[0];
        }
    }*/

    IntVar& operator= (const IntVar& input)
    {
        value[0]   = input.value[0];
        value[1]   = input.value[1];
        value[2]   = input.value[2];

        return *this;
    }

    IntVar& operator= (const int input)
    {
        value[0]   = ((unsigned char*)&input)[0];
        value[1]   = ((unsigned char*)&input)[1];
        value[2]   = ((unsigned char*)&input)[2];

        return *this;
    }

    IntVar operator+ (const IntVar& val) const
    {
        return IntVar( (int)*this + (int)val );
    }

    IntVar operator- (const IntVar& val) const
    {
        return IntVar( (int)*this - (int)val );
    }

    IntVar operator* (const IntVar& val) const
    {
        return IntVar( (int)*this * (int)val );
    }

    IntVar operator/ (const IntVar& val) const
    {
        return IntVar( (int)*this / (int)val );
    }

    IntVar& operator+= (const IntVar& val)
    {
        *this   = *this + val;
        return *this;
    }

    IntVar& operator-= (const IntVar& val)
    {
        *this   = *this - val;
        return *this;
    }

    IntVar& operator*= (const IntVar& val)
    {
        *this   = *this * val;
        return *this;
    }

    IntVar& operator/= (const IntVar& val)
    {
        *this   = *this / val;
        return *this;
    }

    IntVar operator>> (const int val) const
    {
        return IntVar( (int)*this >> val );
    }

    IntVar operator<< (const int val) const
    {
        return IntVar( (int)*this << val );
    }

    operator bool() const
    {
        return (int)*this != 0;
    }

    bool operator! () const
    {
        return !((int)*this);
    }

    IntVar operator- ()
    {
        return IntVar( -(int)*this );
    }

    bool operator== (const IntVar& val) const
    {
        return (int)*this == (int)val;
    }

    bool operator!= (const IntVar& val) const
    {
        return (int)*this != (int)val;
    }

    bool operator>= (const IntVar& val) const
    {
        return (int)*this >= (int)val;
    }

    bool operator<= (const IntVar& val) const
    {
        return (int)*this <= (int)val;
    }

    /* Define all operations you need below.. */


};

