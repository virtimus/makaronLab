#pragma once
#ifndef WQ_6502_H
#define WQ_6502_H

#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

	#include <m6502.h>

	//extern uint8_t ROM[];

		

    #define M6502_PIN_A0 0
    #define M6502_PIN_D0 16
    #define M6502_PIN_RW 24
    #define M6502_PIN_SYNC 25
    #define M6502_PIN_IRQ 26
    #define M6502_PIN_NMI 27
    #define M6502_PIN_RDY 28
    #define M6502_PIN_RES 30

	//pins order on api level
	#define CPINS_RDY 1
	//#define CPINS_A23 31;
	#define CPINS_RESB 32
	#define CPINS_PHI2O 33
	//#define CPINS_PHI2I 35;
	#define CPINS_A0 8
	#define CPINS_D0 39

	#define CPINS_PHI2 35 //PHI2


/*	struct wq6502_CPins {
		using siType = spaghetti::SocketItemType;
		using ioType = spaghetti::IOSocketsType;
		static const C65Pin VPB  {0, "VPB"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin RDY  {1, "RDY"  ,ioType::eInputs,  siType::eInput};
		static const C65Pin PHI1O{2, "PHI1O",ioType::eInputs,  siType::eOutput};
		static const C65Pin IRQB {3, "IRQB" ,ioType::eInputs,  siType::eInput};
		static const C65Pin MLB  {4, "MLB"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin NMIB {5, "NMIB" ,ioType::eInputs,  siType::eInput};
		static const C65Pin SYNC {6, "SYNC" ,ioType::eInputs,  siType::eOutput};
		static const C65Pin VDD  {7, "VDD"  ,ioType::eInputs,  siType::eInput};
		static const C65Pin A0   {8, "A0"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A1   {9, "A1"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A2   {10,"A2"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A3   {11,"A3"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A4   {12,"A4"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A5   {13,"A5"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A6   {14,"A6"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A7   {15,"A7"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A8   {16,"A8"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A9   {17,"A9"   ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A10  {18,"A10"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A11  {19,"A11"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A12  {20,"A12"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A13  {21,"A13"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A14  {22,"A14"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A15  {23,"A15"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A16  {24,"A16"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A17  {25,"A17"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A18  {26,"A18"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A19  {27,"A19"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A20  {28,"A20"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A21  {29,"A21"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A22  {30,"A22"  ,ioType::eInputs,  siType::eOutput};
		static const C65Pin A23  {31,"A23"  ,ioType::eInputs,  siType::eOutput};

		static const C65Pin RESB {32,"RESB" ,ioType::eOutputs, siType::eInput};
		static const C65Pin PHI2O{33,"PHI2O",ioType::eOutputs, siType::eOutput};
		static const C65Pin SOB  {34,"SOB"  ,ioType::eOutputs, siType::eInput};
		static const C65Pin PHI2 {35,"PHI2" ,ioType::eOutputs, siType::eInput};
		static const C65Pin BE   {36,"BE"   ,ioType::eOutputs, siType::eInput};
		static const C65Pin NC   {37,"NC"   ,ioType::eOutputs, siType::eOutput};
		static const C65Pin RWB  {38,"RWB"  ,ioType::eOutputs, siType::eOutput};
		static const C65Pin D0   {39,"D0"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D1   {40,"D1"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D2   {41,"D2"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D3   {42,"D3"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D4   {43,"D4"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D5   {44,"D5"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D6   {45,"D6"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D7   {46,"D7"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D8   {47,"D8"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D9   {48,"D9"   ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D10  {49,"D10"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D11  {50,"D11"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D12  {51,"D12"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D13  {52,"D13"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D14  {53,"D14"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin D15  {54,"D15"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP0  {55,"NP0"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP1  {56,"NP1"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP2  {57,"NP2"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP3  {58,"NP3"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP4  {59,"NP4"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP5  {60,"NP5"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP6  {61,"NP6"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin NP7  {62,"NP7"  ,ioType::eOutputs, siType::eDynamic};
		static const C65Pin VSS  {63,"VSS"  ,ioType::eOutputs, siType::eInput};

		static const C65Pin all[] = {
				VPB,  RDY,   PHI1O, IRQB, MLB, NMIB, SYNC, VDD, A0, A1, A2, A3, A4, A5, A6, A7, A8,  A9,  A10, A11, A12, A13, A14, A15, A16, A17, A18, A19, A20, A21, A22, A23,
				RESB, PHI2O, SOB,   PHI2, BE,  NC,   RWB,  D0,  D1, D2, D3, D4, D5, D6, D7, D8, D9,  D10, D11, D12, D13, D14, D15, NP0, NP1, NP2, NP3, NP4, NP5, NP6, NP7, VSS
		};

		static const int allSize = 64;
	}*/
	typedef struct wq6502Info_t { 
		size_t iv;
		uint64_t pins;
		m6502_t cpu;
		uint8_t RAM[1<<16];
		uint8_t ROM[32768]; 
		m6502_desc_t cpu_desc;
		bool prevClock;
		bool prevResb;

	 } wq6502Info_t;

	void wq6502_init(wq6502Info_t* info);
	uint64_t wq6502_calc(size_t iv,uint64_t pv);

//https://stackoverflow.com/questions/3456446/a-good-c-equivalent-of-stl-vector
#define DECLARE_DYN_ARRAY(T) \
    typedef struct \
    { \
        T *buf; \
        size_t n; \
        size_t reserved; \
    } T ## Array;

#define DYN_ARRAY(T) T ## Array

#define DYN_ADD(array, value, errorLabel) DYN_ADD_REALLOC(array, value, errorLabel, realloc)

#define DYN_ADD_REALLOC(array, value, errorLabel, realloc) \
    { \
        if ((array).n >= (array).reserved) \
        { \
            if (!(array).reserved) (array).reserved = 10; \
            (array).reserved *= 2; \
            void *ptr = realloc((array).buf, sizeof(*(array).buf)*(array).reserved); \
            if (!ptr) goto errorLabel; \
            (array).buf = ptr; \
        } \
        (array).buf[(array).n++] = value; \
    }


#endif// WQ_6502_H
