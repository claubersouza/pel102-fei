from contextlib import AsyncExitStack
from inspect import trace
from trace import Trace
from myhdl import Signal, Simulation,block, always, instance, instances,intbv,delay, toVHDL, toVerilog, traceSignals
import random
from amplificador import amplificador


clk = Signal(intbv(0)[1:])
ganho = Signal(intbv(0)[3:])
seno = Signal(intbv(0)[2:0])
saida = Signal(intbv(0)[2:0])

dut = amplificador(clk,seno,ganho,saida)

@block
def bench():
    clk = Signal(intbv(0)[1:])
    ganho = Signal(intbv(0)[3:])
    seno = Signal(intbv(0)[8:0])
    saida = Signal(intbv(0)[8:0])
    dut = amplificador(clk,seno,ganho,saida)

    @always(delay(10))
    def clk_gen():
        clk.next = not clk

    @instance
    def stimulus():
        yield delay(10)
        seno.next = 0
        ganho.next = 0
        saida.next = 0
        yield delay(10)

        #Cenario 1
        for x in range(4):
            yield delay(10)
            clk.posedge
            seno.next = random.randint(0,3)
            ganho.next = x
            yield delay(10)

            if x * seno.val == saida :
                validacao = "VALOR CORRETO"
            else:
                validacao = "VALOR INCORRETO"

            print("Valor SENO=%s GANHO=%s SAIDA=%s --> %s " % (seno,ganho,saida,validacao))
    return instances()

def convert():
    toVerilog(dut,clk,seno,ganho,saida)

def waveform():
    tb = bench()
    tb.config_sim(trace=True)
    tb.run_sim(100)

def simulation():
    sim = bench()
    sim.run_sim(100)

waveform()
simulation()
convert()



