from multiprocessing.connection import wait
from sre_parse import State
from myhdl import Signal, always_comb, always_seq, block, delay, always, enum, intbv, now, posedge


@block
def adc(clk,go,valid,cmp,value,sample,result,mask):
    t_state = enum('S_WAIT', 'S_SETUP','S_CONVERSION','S_DONE')
    state_next  = Signal(t_state.S_WAIT)


    @always(clk.posedge)
    def logic():
        if not go:
            state_next.next = t_state.S_WAIT
        if state_next == t_state.S_WAIT:
                state_next.next = t_state.S_SETUP
        elif state_next == t_state.S_SETUP:
                state_next.next = t_state.S_CONVERSION
                mask.next = Signal(intbv(128)[8:])
                result.next = Signal(intbv(0)[8:])
        elif state_next ==  t_state.S_CONVERSION:
                if cmp:
                    result.next = result | mask
                mask.next = mask>>1
                if mask == 0 :
                    state_next.next = t_state.S_DONE
        elif state_next == t_state.S_DONE:
            if result.next == value.next:
                valid.next = 1
            return

        valid.next = state_next == t_state.S_DONE
        value.next = result.next | mask.next
        sample.next  = state_next  == t_state.S_SETUP
    return logic

