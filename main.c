#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <stdio.h>
#include <Python.h>
#include <numpy/arrayobject.h>


#include "read_uart.h"
#include "RGB.h"


void display_int(int *data, unsigned int len){
    unsigned int j;
    for(j = 0;j < len;j++)
        printf("%d ", data[j]);
    printf("\n");
}


int main(){
    int data [400][8];
    int fd = 0;
    
    PyObject *pModule, *pFunc, *pArray, *pResult;
    npy_intp dims[2] = {400, 8};

    int flag, i;

    long int result;

    int SerialNumber;


    /*---- prepare uart ----*/
    char filename[] = "/dev/ttyACM0";

    fd = open(filename, O_RDONLY);
    if(fd == -1){
        perror("can't open the file.");
        return -1;
    }

    flag = set_attr(fd, B115200, DATA_UNIT, 1);
    if(flag == -1){
        perror("failed to set attribute.");
        return -1;
    }
    /*--- end prepare uart ---*/

    /*--- prepare python  ---*/
    Py_Initialize();

    flag = _import_array();
    if (flag < 0) {
        perror("faild to import array");
        return -1;
    }

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("import numpy");
    PyRun_SimpleString("sys.path.append('')");

    pModule = PyImport_ImportModule("py.emotion_detector");
    if (pModule == NULL) {
        perror("failed to import module.");
        return -1;
    }

    pFunc = PyObject_GetAttrString(pModule, "emotion_recognition");
    pArray = PyArray_SimpleNewFromData(2, dims, NPY_INT, data);
    /*--- end prepare python  ---*/

    /*--- prepare RGB ---*/
    flag = get_SerialNumber(&SerialNumber);
    if (flag < 0)
    {
        perror("failed to get_SerialNumber.");
        return -1;
    } 

    flag = initRGB(SerialNumber);
    if (flag < 0)
    {
        perror("failed to initRGB.");
        return -1;
    }
    /*--- end prepare RGB ---*/

    /*--- workplace ---*/
    flag = get_num_frame_data(data, 400, fd);
    if(flag == -1){
        perror("failed to get_num_frame_data.");
        return -1;
    }

    for(i = 0;i < 400;i++)
        display_int(data[i], 8);

    pResult = PyObject_CallFunctionObjArgs(pFunc, pArray, NULL);
    if (PyLong_Check(pResult))
        result = PyLong_AsLong(pResult);
    else {
        perror("failed to return long.");
        return -1;
    }
    printf("%ld\n", result);

    flag = light_RGB_one(SerialNumber, (uint8_t)result);
    if (flag < 0)
    {
        perror("failed to light_RGB_one.");
        return -1;
    }
    /*--- workplace ---*/

    /*--- finalize python ---*/
    Py_DECREF(pFunc);
    Py_DECREF(pModule);
    Py_DECREF(pArray);
    Py_DECREF(pResult);

    Py_Finalize();
    /*--- end finalize python ---*/

    /*--- finalize uart  ---*/
    flag = close(fd);
    if(flag == -1){
        perror("can't close the terminal.");
        return -1;
    }
    /*--- end finalize uart ---*/
    
    printf("OK\n");
    return 0;
}
