#include "LoRaWan_APP.h"

// Device credentials, adjust these according to your actual configuration
uint8_t devEui[] = { 0xA4, 0x76, 0xB3, 0x86, 0x0E, 0xD5, 0xB2, 0x31 };
uint8_t appEui[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
uint8_t appKey[] = { 0x1B, 0x70, 0xBF, 0x9E, 0x49, 0x2A, 0x99, 0x8E, 0x73, 0xC5, 0xE4, 0xB7, 0x47, 0x2A, 0xB9, 0x93 };

uint8_t nwkSKey[16] = { /* Network session key */ };
uint8_t appSKey[16] = { /* Application session key */ };
uint32_t devAddr = 0x260111FF; // Example device address


// Operation parameters
uint8_t appPort = 2;
bool isTxConfirmed = false;
uint8_t confirmedNbTrials = 4;

// Network settings
uint16_t userChannelsMask[6] = {0xFF00, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000};
bool overTheAirActivation = true;
DeviceClass_t loraWanClass = CLASS_A;
bool loraWanAdr = true;
uint32_t appTxDutyCycle = 10000;  // Duty cycle in ms

void setup() {
    Serial.begin(115200);
    // Initialize LoRaWAN with the class and region.
    LoRaWAN.init(loraWanClass, LORAMAC_REGION_EU868);
    LoRaWAN.displayAck();
    LoRaWAN.join();
}

void prepareTxFrame() {
    // Prepare a dummy data payload to send
    uint16_t dummyTemperature = 250; // Example temperature 25.0 degrees Celsius
    uint16_t dummyHumidity = 485;    // Example humidity 48.5%
    
    appDataSize = 4; // Set the size of appData to be sent
    appData[0] = highByte(dummyTemperature);
    appData[1] = lowByte(dummyTemperature);
    appData[2] = highByte(dummyHumidity);
    appData[3] = lowByte(dummyHumidity);
}

void loop() {
    // Implementation of device state handling
    switch (deviceState) {
        case DEVICE_STATE_INIT:
            Serial.println("Device in initialization state.");
            break;
        case DEVICE_STATE_JOIN:
            Serial.println("Attempting to join network...");
            LoRaWAN.displayJoining();
            break;
        case DEVICE_STATE_SEND:
            Serial.println("Preparing to send data...");
            prepareTxFrame();
            LoRaWAN.send();
            Serial.println("Data sent.");
            deviceState = DEVICE_STATE_CYCLE;
            break;
        case DEVICE_STATE_CYCLE:
            Serial.println("Cycling for next send...");
            LoRaWAN.cycle(15000);
            deviceState = DEVICE_STATE_SLEEP;
            break;
        case DEVICE_STATE_SLEEP:
            Serial.println("Device sleeping...");
            LoRaWAN.sleep(CLASS_A);
            break;
        default:
            Serial.println("Unknown state, resetting...");
            deviceState = DEVICE_STATE_INIT;
            break;
    }
    delay(1000);
}
