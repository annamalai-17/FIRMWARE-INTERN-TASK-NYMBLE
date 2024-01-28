#include <avr/io.h>
#include <avr/eeprom.h>
#include <util/delay.h>

#define F_CPU 16000000UL
#define BAUD 2400
#define MYUBRR F_CPU/16/BAUD-1

#define EEPROM_SIZE 1020

void UART_Init(unsigned int ubrr) {
    // Set baud rate
    UBRR0H = (unsigned char)(ubrr >> 8);
    UBRR0L = (unsigned char)ubrr;
    
    // Enable transmitter and receiver
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);
    
    // Set frame format: 8 data bits, 1 stop bit, no parity
    UCSR0C = (3 << UCSZ00);
}

void UART_Transmit(char data) {
    // Wait for empty transmit buffer
    while (!(UCSR0A & (1 << UDRE0)))
        ;
    
    // Put data into buffer, sends the data
    UDR0 = data;
}

char UART_Receive(void) {
    // Wait for data to be received
    while (!(UCSR0A & (1 << RXC0)))
        ;
    
    // Get and return received data from buffer
    return UDR0;
}

void storeStringInEEPROM(char* str) {
    int address = 0;
    while (*str != '*') {
        eeprom_write_byte((uint8_t*)address, *str);
        address++;
        str++;
    }
    eeprom_write_byte((uint8_t*)address, '*');
}

void retrieveStringFromEEPROM(char* str) {
    int address = 0;
    char currentChar = eeprom_read_byte((uint8_t*)address);

    while (currentChar != '*') {
        *str = currentChar;
        address++;
        str++;
        currentChar = eeprom_read_byte((uint8_t*)address);
        //Serial.print(currentChar);
        
    }

    *str = '*';
}

int main(void) {
    char receivedData[EEPROM_SIZE];
    char storedData[EEPROM_SIZE];

    UART_Init(MYUBRR);
    int i=0;
    while (1) {
        if (UCSR0A & (1 << RXC0)) {
            char receivedChar = UART_Receive();
           // eeprom_write_byte((uint8_t*)0, receivedChar);

            //UART_Transmit(receivedChar);
            if(receivedChar!='*')
            {
              
              receivedData[i]=receivedChar;
              //Serial.print(receivedData[i]);
              //Serial.print(" ");
              i++;
              
            }
            else if(receivedChar=='*')
            {
              receivedData[i]='*';
              //Serial.println(receivedData);
              
              storeStringInEEPROM(receivedData);
              retrieveStringFromEEPROM(storedData);
              //Serial.println(storedData);
              
               i=0;
               char* strPtr = storedData;
                while (*strPtr != '*') 
                {
                    UART_Transmit(*strPtr);
                    
                    strPtr++;
                }
                receivedData[0]='\0';
                storedData[0]='\0';
            }
            
            //char request = UART_Receive();

            /*if (receivedChar == 'R') {
                retrieveStringFromEEPROM(storedData);

                char* strPtr = storedData;
                while (*strPtr != '\0') {
                    UART_Transmit(*strPtr);
                    strPtr++;
                }
            }*/
        }
    }

    return 0;
}
