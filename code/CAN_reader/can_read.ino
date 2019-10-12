#define CAN_500KBPS 16
#include <mcp_can.h>
#include <SPI.h>

const int SPI_CS_PIN = 9;

MCP_CAN CAN(SPI_CS_PIN);

void setup(){

  Serial.begin(9600);

  while(CAN_OK != CAN.begin(CAN_500KBPS))
  {
    delay(100);
  }
}

void loop(){

  unsigned char len = 0;
  unsigned char buf[8];

  if(CAN_MSGAVAIL == CAN.checkReceive())
  {
    CAN.readMsgBuf(&len, buf);
    unsigned long canId = CAN.getCanId();
        
        
		Serial.print("0x");
		Serial.println(canId,HEX);

		for(int i=0;i<len;i++)
		{
		 Serial.print(buf[i],HEX);
		 Serial.print(" "); 
		}

    Serial.println();     
  }
}
