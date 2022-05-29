
from ast import While
from myhdl import Signal, always, block, delay, instance, instances, intbv, toVerilog

from adc import adc

clk = Signal(intbv(0)[1:])
go  = Signal(intbv(0)[1:])
valid  = Signal(intbv(0)[1:])
cmp  = Signal(intbv(0)[1:])
value  = Signal(intbv(0)[8:])
sample  = Signal(intbv(0)[1:])
result  = Signal(intbv(0)[8:])
mask = Signal(intbv(0)[8:])
hold_value = Signal(intbv(0)[8:])
dut = adc(clk,go,valid,cmp,value,sample,result,mask)

@block
def bench():
    clk = Signal(intbv(0)[1:])
    go  = Signal(intbv(0)[1:])
    valid  = Signal(intbv(0)[1:])
    cmp  = Signal(intbv(0)[8:])
    value  = Signal(intbv(0)[8:])
    sample  = Signal(intbv(0)[1:])
    result  = Signal(intbv(0)[8:])
    state_now = Signal(intbv(0)[1:])
    mask = Signal(intbv(0)[8:])
    hold_value = Signal(intbv(0)[8:])

    dut = adc(clk,go,valid,cmp,value,sample,result,mask)



    @always(delay(10))
    def clk_gen():
        clk.next = not clk

    @always(delay(10))
    def comparator():      
        cmp.next = hold_value >= value


    @instance
    def monitor():
        while 1:
            yield delay(10)
            print("go=%s valid=%s result=%s sample=%s value=%s cmp=%s mask=%s" % (go,valid,int(result),sample,int(value),cmp,int(mask)))



    @always(sample.posedge)
    def hold():
        hold_value.next = Signal(intbv(70)[8:])
                
    @instance
    def stimulus():
        
        yield delay(10)
        clk.posedge
        go.next = 0

        yield delay(10)
        clk.posedge
        go.next = 1
            
    return instances()

   
def convert():
    toVerilog(dut,clk,go,valid,cmp,value,sample,result,mask)

def waveform():
    tb = bench()
    tb.config_sim(trace=True)
    tb.run_sim(500)

def simulation():
    sim = bench()
    sim.run_sim(500)

convert()
simulation()
waveform()

