#include "RGB.h"

int get_SerialNumber(int *SerialNumber){
    int ret = 0, i;
    int SerialNumbers[16];
    
    ret = UsbDevice_Scan(SerialNumbers);
    if (ret < 0)
    {
        printf("Scan error: %d\n", ret);
        return -1;
    }
    else if (ret == 0)
    {
        printf("No device\n");
        return -1;
    }
    else
    {
        for (i = 0; i < ret; i++)
        {
            printf("Dev%d SN: %d\n", i, SerialNumbers[i]);
        }
        *SerialNumber = SerialNumbers[0];
        return 0;
    }
}

int initRGB(int SerialNumber){
    int flag;
    IO_InitStruct_Tx_t init_T[] = {{0, 1, 0}, {1, 1, 0}, {2, 1, 0}};
    IO_InitStruct_Rx_t init_R[] = {{0}, {0}, {0}};
    flag = IO_InitMultiPin(SerialNumber, init_T, init_R, 3);
    if (flag < 0)
    {
        perror("failed to IO_InitMultiPin.");
        return -1;
    }
    return 0;
}

int light_RGB_one(int SerialNumber, uint8_t light){
    int flag;
    IO_WriteStruct_Tx_t write_T[] = {{0, 0}, {1, 0}, {2, 0}};
    IO_WriteStruct_Rx_t write_R[] = {{0}, {0}, {0}};

    write_T[light].PinState = 1;
    flag = IO_WriteMultiPin(SerialNumber, write_T, write_R, 3);
    if (flag < 0)
    {
        perror("failed to IO_WriteMultiPin.");
        return -1;
    }
    return 0;
}

