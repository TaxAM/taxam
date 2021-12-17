# Number of samples
ns = 18
# Number of threads
nt = 5
qtt_min = int(ns / nt)
rest = ns % nt
# BEGGINING OF CUT IN THE LIST
bgg = 0
for i in range(nt):
    # CURRENT QUANTITY PER LINE
    crr_qtd = qtt_min + (1 if rest > 0 else 0)
    rest -= 1
    # END OF CUT IN THE LIST
    end = bgg + crr_qtd
    # CREATING THREAS LIST FOR EACH THREAD
    print(f'[{bgg}:{end}]')
    bgg = end