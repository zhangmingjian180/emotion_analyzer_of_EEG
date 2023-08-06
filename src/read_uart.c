#include "read_uart.h"


int set_attr(int fd, speed_t speed, unsigned char vmin, unsigned char vtime){
    struct termios options, termios_chk;
    int flag;

    flag = tcgetattr(fd, &options);
    if(flag == -1){
        perror("can't get arribute of termninal.");
        return -1;
    }

    cfsetispeed(&options, speed); //B115200 为宏定义
    
    // raw model.
    options.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
    options.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
    options.c_cflag &= ~(CSIZE | PARENB);
    options.c_cflag |= CS8;

    options.c_cflag |= (CLOCAL | CREAD);

    options.c_cflag &= ~CSTOPB;
    
    options.c_cc[VMIN] = vmin;
    options.c_cc[VTIME] = vtime;
     
    flag = tcsetattr(fd, TCSAFLUSH, &options);
    if(flag == -1){
        perror("can't set arribute of termninal.");
        return -1;
    }
    
    tcflush(fd, TCIFLUSH);
    
    // check whether the changes all is set.
    flag = tcgetattr(fd, &termios_chk);
    if(flag == 0){
        if(options.c_cflag != termios_chk.c_cflag){
            perror("Failed to set the parameters of termios\n");
            return -1;
        }
    }else{
        perror("can't get arribute of termninal.");
        return -1;
    }
    return 0;
}


int read_data(int fd, unsigned char *data, unsigned int num){
    unsigned char buffer[DATA_UNIT];
    unsigned int i, n, len = 0;

    while(len != num){
        n = read(fd, buffer, sizeof(buffer));
        if(n != sizeof(buffer)){
            if(n == -1)
                perror("failed to read.");
            else
                perror("timeout.");
            return -1;
        }

        for(i = len;i < (len + n);i++)
            data[i] = buffer[i-len];
        len += n;
    }
    return 0;
}


/*
void display_data(unsigned char *data, unsigned int len){
    int j;
    for(j = 0;j < len;j++)
        printf("%02X ", data[j]);
    printf("\n");
}
*/

void get_data_from_frame(unsigned char *data, int *real_data){
    unsigned char cache[32];
    int *t = (int *)cache;

    int i;
    for(i = 0;i < 32;i++)
        cache[i] = data[39 - i];

    for(i = 0;i < 8;i++)
        real_data[i] = t[7 - i];

    return;
}


int get_num_frame_data(int result[][8], unsigned int size, int fd){
    unsigned char data[60];
    int flag, i;
    for(i = 0;i < size;i++){
        flag = read_data(fd, data, sizeof(data));
        if(flag == -1){
            perror("failed to read.");
            return -1;
        }
        get_data_from_frame(data, result[i]);
    }
    return 0;
}


