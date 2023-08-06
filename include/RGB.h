#ifndef __RGB_H
#define __RGB_H

#include <stdio.h>
#include "usb_device.h"
#include "io.h"

int get_SerialNumber(int *SerialNumber);
int initRGB(int SerialNumber);
int light_RGB_one(int SerialNumber, uint8_t light);

#endif
