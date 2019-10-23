
#define CAN_500KBPS 16
#include <mcp_can.h>
#include <SPI.h>

const int SPI_CS_PIN = 9;
unsigned char msg_to_send[8]={0,0,0,0,0,0,0,0};
  
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
        if(canId==272) // 0x110 contains 4 wheelspeeds across 8 bytes. 
        {
          for(int i=0;i<3;i++)
          {
             Serial.print(buf[i],HEX);
            Serial.print(" "); 
          }
		  for(int i =0;i<len;i++) //also send the content of last seen 0x280.
		  {
            Serial.print(msg_to_send[i],HEX);
            Serial.print(" ");			  
			  
		  }
        
         Serial.println();
        }
		else if(canId==640) //0x280, contains RPMS in bits 2 and 3. Update variable that gets sent when 0x110 received.
		{
		  for(int i=0;i<len;i++)
          {
			msg_to_send[i]=buf[i];
          }
			
			
		}
  }
 // else{
 //  Serial.println(" "); 
 // }
}
