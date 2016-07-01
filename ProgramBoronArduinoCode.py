'''
Created on Jun 30, 2016

@author: maxr
'''

def arduinoCode(data_width, data_array, format_comment):
    codeStr = """
    #include <Wire.h>
    
    #Define DATA_WIDTH %d
    
    byte data[DATA_WIDTH] = %s
    
    // format = %s
    
    byte numLinesTotal = 0;
    byte lineCounter = 0;
    byte packetNumBytes = 0;
    byte checkSum = 0;
    int array_ptr = 0;
    
    void setup() {
      Wire.begin(); // join i2c bus (address optional for master)
      Serial.begin(9600);
    }
    
    byte x = 0;
    void loop() {
    if(Serial.available() > 0)
    {
      x = Serial.read();
    }
    switch(x)
    {
      case '1':
        while(array_ptr < DATA_WIDTH)
        {
            Wire.beginTransmission(0x5A); // transmit to device #8
            
            checkSum = 0x30;
            Wire.write(0x30);
            
            checkSum = checkSum + data[array_ptr];
            Wire.write(data[array_ptr++]);
            
            checkSum = (checkSum + data[array_ptr]) - 0x08;
            Wire.write(data[array_ptr]-0x08);
            data[array_ptr++];
            
            checkSum = checkSum + data[array_ptr];
            packetNumBytes = data[array_ptr];
            Wire.write(data[array_ptr++]);
            
            for(int i=0;i<packetNumBytes;i++)
            {
              checkSum = checkSum + data[array_ptr];
              Wire.write(data[array_ptr++]);
            }
            
            checkSum = -checkSum;
            Wire.write(checkSum);
            
            Wire.endTransmission();    // stop transmitting
            /*
            Wire.requestFrom(0x5A, 3);    // request 6 bytes from slave device #8
            while (Wire.available()) { // slave may send less than requested
              char c = Wire.read(); // receive a byte as character
              Serial.println(c, HEX);         // print the character
             
            }
            */
        delay(100);
        Serial.println("line written");
        }
        array_ptr = 0;
        x = 0;
        break;
      
        
      case '2':
          Wire.beginTransmission(0x5A); // transmit to device #8
          Wire.write(0x30);
          Wire.write(0x00);
          Wire.write(0x00);
          Wire.write(0x01);
          Wire.write(0x03);
          checkSum = 0x30+0x00+0x00+0x01+0x03;
          Wire.write(-checkSum);
          Wire.endTransmission();    // stop transmitting
          Wire.requestFrom(0x5A, 3);    // request 6 bytes from slave device #8
          while (Wire.available()) { // slave may send less than requested
            char c = Wire.read(); // receive a byte as character
            
          }
            
        x = 0;
        break;
        
      default:
        x = 0;
        break;
    }
    delay(100);
    }
    """ % (data_width, data_array, format_comment)
    return codeStr
