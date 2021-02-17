#pragma once
#ifndef WQ_WQC_H
#define WQ_WQC_H

#include <Python.h>
#include <pthread.h>

PyObject * pyDictNew(){ return PyDict_New(); }

int pyDictSetSizet(PyObject *dict, const char *key, size_t value){
    PyObject* pyVal = PyLong_FromSize_t(value);
    return PyDict_SetItemString(dict, key, pyVal);
}

int pyDictSetUint64(PyObject *dict, const char *key, uint64_t value){
    PyObject* pyVal = PyLong_FromUnsignedLongLong(value);
    return PyDict_SetItemString(dict, key, pyVal);
}

int pyDictSetString(PyObject *dict, const char *key, const char *value){
    PyObject* pyVal = PyUnicode_FromString(value);
    return PyDict_SetItemString(dict, key, pyVal);
}

int pyDictSetObject(PyObject *dict, const char *key, PyObject *pyVal){
    return PyDict_SetItemString(dict, key, pyVal);
}

PyObject * pyDictGetItem(PyObject *dict,const char *key){
    return PyDict_GetItemString(dict, key);
}



#endif //WQ_WQC_H