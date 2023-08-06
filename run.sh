#!/bin/sh

gcc -c main.c -o main.o -I include $(python3.9-config --cflags) -I /home/zhangjian/anaconda3/envs/DySAT_SEED/lib/python3.9/site-packages/numpy/core/include
gcc -o out main.o lib/RGB.o lib/read_uart.o $(python3.9-config --ldflags) -L lib -lpython3.9 -l:librockmong.so -l:libusb-1.0.so
sudo PATH=/home/zhangjian/anaconda3/envs/DySAT_SEED ./out
