#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 17:05:46 2022

@author: framas
"""

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
import random

NPROD = 3
N = 5


def producer(sem_empty,sem_nonempty,storage,pid):
    v = 0 
    for i in range(N):
        print (f"producer {current_process().name} produciendo")
        sleep(random.random()/3)
        v += random.randint(0,5) #se producen los números de forma creciente, a partir del anterior sumándole un número random entre 0 y 5
        sem_empty[pid].acquire() 
        storage[pid] = v
        sem_nonempty[pid].release() 
        print (f"producer {current_process().name} almacenado {v}")
    sem_empty[pid].acquire()
    storage[pid] = -1 #cuando ha terminado de producir añadimos un -1 al almacén 
    sem_nonempty[pid].release() 
    

def minimo(lista): #función auxiliar para calcular el mínimo de una lista y su posición en ella
    minimo=max(lista)+1
    pos=0
    for i in range(len(lista)):
        if lista[i]<minimo and lista[i]!=-1:
            minimo=lista[i]
            pos=i
    return minimo, pos
    
def consumer(sem_empty,sem_nonempty,storage):  
    prod_consumidos = [] 
    list_aux=[-1]*NPROD 
    for i in range(NPROD):  
        sem_nonempty[i].acquire() 
    while list_aux != list(storage): #se mete en el bucle mientras que haya elementos para consumir 
        v, pos = minimo(storage)
        prod_consumidos.append(v)
        print (f"consumer {current_process().name} consumiendo {v}")
        sem_empty[pos].release() 
        sem_nonempty[pos].acquire() 
    print ('Lista de productos consumidos:', prod_consumidos) 



def main():
    storage = Array('i',NPROD)
    sem_empty=[]
    sem_nonempty = []
    for i in range(NPROD):
        non_empty = Semaphore(0)
        empty = BoundedSemaphore(1)
        sem_empty.append(empty)
        sem_nonempty.append(non_empty)
    l_prod = [ Process(target = producer, 
                       name=f'prod_{i}', 
                       args=(sem_empty, sem_nonempty, storage, i))
                    for i in range (NPROD)]
    cons = Process(target = consumer, name="cons", args = (sem_empty,sem_nonempty,storage))
    
    
    for p in l_prod:
         p.start()
    cons.start()
    for p in l_prod:
        p.join()
    cons.join()


if __name__ == "__main__":
 main()    
           
         
    
    


