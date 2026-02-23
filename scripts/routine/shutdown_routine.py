from source.olfattometro import Olfactometer
if __name__=='__main__':
    print("This is the shutdown routine for Sniff0!\n")
    olf = Olfactometer(timer = None)
    olf.flush(flush_duration=100) #seconds