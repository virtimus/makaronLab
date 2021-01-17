#include <Python.h>
#include <pthread.h>
#include "m6502.h"


void* sum(void *argp){
    unsigned long *stepsFrom = (unsigned long *) argp;
    unsigned long *stepsTo = (unsigned long *) (argp + sizeof(unsigned long));
    unsigned long s, i;

    s = 0;
    for(i=*stepsFrom; i<*stepsTo; i++)
        s += (i+1);

    return (void *)s;
}


static int number = 0;

int incDecNumber(int n){
    number += n;
    return number;
}


static PyObject* method_sum(PyObject* self, PyObject* args) {
    unsigned long countOfNumbers;
    if(!PyArg_ParseTuple(args, "k", &countOfNumbers)){
        printf("# FAIL\n");
        return NULL;
    }

    int n = (int)countOfNumbers;
    int result = incDecNumber(n);

    return PyLong_FromLong((unsigned long)result);
}

static PyMethodDef WqcMethods[] = {
    {"sum", method_sum, METH_VARARGS, "Calculate sum of n numbers."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef wqcmodule = {
    PyModuleDef_HEAD_INIT,
    "sum",
    "Calculate sum of n numbers.",
    -1,
    WqcMethods
};

PyMODINIT_FUNC PyInit_wqc() {
    return PyModule_Create(&wqcmodule);
}
