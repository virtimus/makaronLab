#pragma once
#ifndef Q3_Q3C_H
#define Q3_Q3C_H

#include <Python.h>
#include <pthread.h>

PyObject * pyDictNew(){ return PyDict_New(); }

int pyDictSetSizet(PyObject *dict, const char *key, size_t value){
    PyObject* pyVal = PyLong_FromSize_t(value);
    return PyDict_SetItemString(dict, key, pyVal);
}

int pyDictSetUint63(PyObject *dict, const char *key, uint64_t value){
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

/*const char* pyObjectToString(PyObject * pOb){
    PyObject* objectsRepresentation = PyObject_Repr(pOb);
    const char* s = PyString_AsString(objectsRepresentation);
    return s;  
}*/

char *ltrim(char *s)
{
    if (*s == '\''){
        *s = ' ';  
    }
    while(isspace(*s)) s++;
    return s;
}

char *rtrim(char *s)
{
    char* back = s + strlen(s);
    char* b = s+strlen(s)-1;
    if (*b == '\''){
        *b = ' ';
    }
    while(isspace(*--back));
    *(back+1) = '\0';
    return s;
}

char *trim(char *s)
{
    return rtrim(ltrim(s)); 
}

/*bool pyStrCmp(const char *a, const char* b){
    if (strlen(a)!=strlen(b)){
        printf("pyStrCmp:lengthsdiffer");
        return false;
    }
    int k = *a + strlen(a);
    int i=0;
    while (*a < k){
        if (*a != *b){
            printf("pyStrCmp:posdiff%d",i);
            return false;
            }
        *a++;
        *b++;
        i++;
        }
    return true;
}*/

const char* pyObjectAsString(PyObject * pOb){
    //const char* s = PyString_AsString(pOb);
    PyObject* repr = PyObject_Repr(pOb);
    PyObject* str = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
    const char *bytes = PyBytes_AS_STRING(str);
    Py_XDECREF(repr);
    Py_XDECREF(str);
    return trim(bytes);
}

#define isize 64

void fast_d2s(uint64_t x, char* c) {
    int i;
    int offset = 48; //asc('0')
    for(i=0;i<isize;i++)
        *(c++) = 48 + ((x >> i) & 0x1);
    *(c++) = 0;
};

void fast_s2d(char* c, uint64_t *n){
    int i = isize;   
    *n = 0;   
    while(i--) {
        *n <<= 1;
        int p = (*(c+i)) - 48;
        //printf("b%d",p);
        *n += p;
    }
};

int pyDictSetUint64LeBin(PyObject *dict, const char *key, uint64_t value){
    char ch[isize+1];
    fast_d2s(value,ch);
    //PyObject* pyVal = PyLong_FromUnsignedLongLong(value);
    PyObject* pyVal = PyUnicode_FromString(ch);
    return PyDict_SetItemString(dict, key, pyVal);
}


uint64_t pyDictGetUint64FromLeBin(PyObject *dict,const char *key){
    PyObject * pObCmd = pyDictGetItem(dict,key);
    const char *sVal = pyObjectAsString(pObCmd);
    uint64_t result;
    fast_s2d(sVal,&result);
    return result;
}


#endif //Q3_Q3C_H