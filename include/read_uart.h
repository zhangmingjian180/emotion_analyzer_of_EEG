#ifndef READ_UART_H
#define READ_UART_H

#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<unistd.h>
#include<termios.h>
#include<stdlib.h>

#define DATA_UNIT 60

int set_attr(int fd, speed_t speed, unsigned char vmin, unsigned char vtime);

int get_num_frame_data(int result[][8], unsigned int size, int fd);

#endif
