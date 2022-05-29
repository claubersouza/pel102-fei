
from ast import While
from myhdl import Signal, always, block, delay, instance, instances, intbv, toVerilog

from amplificador_full import amplificador_full

clk = Signal(intbv(0)[1:])
go  = Signal(intbv(0)[1:])
valid  = Signal(intbv(0)[1:])
cmp  = Signal(intbv(0)[1:])
value  = Signal(intbv(0)[8:])
sample  = Signal(intbv(0)[1:])
result  = Signal(intbv(0)[8:])
mask = Signal(intbv(0)[8:])
hold_value = Signal(intbv(0)[8:])
output = Signal(intbv(0)[8:])
gain = Signal(intbv(0)[4:])
dut = amplificador_full(clk,go,valid,cmp,value,sample,result,mask,gain,output)

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
    output = Signal(intbv(0)[8:])
    gain = Signal(intbv(0)[4:])
    dut = amplificador_full(clk,go,valid,cmp,value,sample,result,mask,gain,output)



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
            print("go=%s valid=%s result=%s sample=%s value=%s cmp=%s mask=%s gain=%s output=%s" % (go,valid,int(result),sample,int(value),cmp,int(mask),int(gain),int(output)))



    @always(sample.posedge)
    def hold():
        hold_value.next = Signal(intbv(5)[8:])
                
    @instance
    def stimulus():
        yield delay(10)
        clk.posedge
        go.next = 0

        yield delay(10)
        clk.posedge
        go.next = 1
        gain.next = 2
            
    return instances()

   
def convert():
    toVerilog(dut,clk,go,valid,cmp,value,sample,result,mask,gain,output)

def waveform():
    tb = bench()
    tb.config_sim(trace=True)
    tb.run_sim(500)

def simulation():
    sim = bench()
    sim.run_sim(500)

#convert()
simulation()
#waveform()

