from source.olfattometro import Olfactometer
if __name__=='__main__':
    print("This is the setup routine for Sniff0!\n")
    olf = Olfactometer(timer = None)
    olf.calibration()
    #olf.test_delay()