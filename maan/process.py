from select_events import reconstruct_and_store

YEAR = 2010
STATION = 501

if __name__ == '__main__':

    assert(STATION==501, 'reconstruct_and_store werkt alleen met 501...')

    aantal = 0

    for month in range(1,13):
        print "maand: ", month

        filename = "s501_"+str(YEAR)+"_"+str(month)+".h5"
        aantal += reconstruct_and_store(filename)

    print "Klaar."
    print "Totaal %d events gereconstrueerd.", aantal
