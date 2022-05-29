from myhdl import always_comb, always_seq, block, delay, always, now, posedge


@block
def amplificador(clk,seno,ganho,saida):
    @always(clk.posedge)
    def logic():
        saida.next = seno * ganho

    return logic


