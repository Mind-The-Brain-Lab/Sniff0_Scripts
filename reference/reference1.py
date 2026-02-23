import time
import random
import serial
from psychopy import core, visual, event

class FakeSerial:
    def write(self,message):
        print(message)

# PARAMETRI OLFATTOMETRO
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# Connessione all'olfattometro.py
olfactometer = FakeSerial()
time.sleep(2)  # Attendi inizializzazione

# Imposta canale aria pulita
olfactometer.write(b"setCAChannel 0\n")
time.sleep(1)

# Imposta il flusso di aria calibrato
olfactometer.write(b"setFlow 0:2.5;1:2.5;2:2.5;3:2.5;4:2.5\n")
time.sleep(1)

# Creazione finestra PsychoPy
win = visual.Window(fullscr=False, color=(0, 0, 0))
stim_text = visual.TextStim(win, text="", color=(1, 1, 1), height=0.1)

# Condizioni sperimentali
stimuli_families = ["Fruttato", "Floreale", "Speziato"]
channels = [1, 2, 3, 4]  # Canali disponibili

# Funzione per inviare comandi all'olfattometro.py
def send_command(command):
    olfactometer.write(command.encode() + b"\n")
    time.sleep(0.1)

# Loop sulle 3 RUN (una per ogni famiglia di odori)
for run_index, family in enumerate(stimuli_families):
    stim_text.text = f"RUN {run_index+1}: {family}"
    stim_text.draw()
    win.flip()
    core.wait(3)

    # 12 trial per ogni RUN
    for trial in range(12):
        stim_text.text = f"Trial {trial+1}"
        stim_text.draw()
        win.flip()
        core.wait(2)

        # 12s di rest
        stim_text.text = "Rest"
        stim_text.draw()
        win.flip()
        core.wait(12)

        # 1s di preparazione
        stim_text.text = "Preparazione"
        stim_text.draw()
        win.flip()
        core.wait(1)

        # Seleziona un canale casuale per la stimolazione
        channel = random.choice(channels)

        # Jittering della durata dello stimolo
        stim_duration = random.uniform(10, 14)  # Jitter tra 10s e 14s

        # Avvia stimolazione: disattiva aria pulita e attiva canale odorante
        send_command(f"CaOffOpenValveTimed {int(stim_duration * 1000)}")

        stim_text.text = f"Stimolo {family} (Canale {channel})"
        stim_text.draw()
        win.flip()
        core.wait(stim_duration)

        # 5s per la risposta
        stim_text.text = "Rispondi!"
        stim_text.draw()
        win.flip()
        core.wait(5)

# Chiusura della finestra PsychoPy
win.close()

# Chiudi connessione olfattometro.py
olfactometer.close()






'''Ecco uno script in **Python** per **PsychoPy** che controlla l'olfattometro.py **Sniff-0**, eseguendo il task olfattivo descritto. Lo script utilizza la libreria `serial` per la comunicazione con l'olfattometro.py e genera una sequenza di trial rispettando il **jittering** delle tempistiche e la randomizzazione dei canali.

### **Struttura dello script**
- **Connessione** con l'olfattometro.py tramite porta seriale.
- **Impostazione della calibrazione** del flusso d'aria.
- **Esecuzione di 3 RUN** (fruttato, floreale, speziato).
- **Ogni trial include:**
  - 12s di **rest**
  - 1s di **preparazione**
  - 12s di **stimolo ON** (con un canale randomizzato)
  - 5s di **risposta**
  - Jittering casuale sulle tempistiche di ogni stimolo.
### **Cosa fa lo script**
✅ **Connette** PsychoPy con l'olfattometro.py Sniff-0 via `serial`.  
✅ **Imposta il flusso d'aria** e il canale di aria pulita.  
✅ **Esegue 3 RUN** (fruttato, floreale, speziato).  
✅ **Ogni RUN ha 12 trial** con:
  - **Rest (12s)**
  - **Preparazione (1s)**
  - **Stimolo ON (10-14s, jitterato)**
  - **Risposta (5s)**
✅ **Jitterizza la durata dello stimolo** per aumentare la variabilità.  
✅ **Randomizza i canali disponibili (1-4)** per ogni trial.

### **Modifiche possibili**
🔹 Se vuoi usare un **trigger esterno**, puoi sostituire `CaOffOpenValveTimed` con `TCaOffOpenValveTimed`.  
🔹 Se vuoi **registrare risposte** dai partecipanti, puoi usare `event.waitKeys()`.  
🔹 Se il tuo olfattometro.py ha altri **parametri specifici**, puoi modificarli con `send_command()`.  

### **Requisiti**
- **Python** (consigliata la versione 3.7+)
- **PsychoPy** (`pip install psychopy`)
- **pyserial** (`pip install pyserial`)
- **Olfattometro Sniff-0** collegato tramite USB

### **Conclusione**
Questo script permette di controllare l'olfattometro.py direttamente da **PsychoPy**, sincronizzando gli stimoli olfattivi con la presentazione degli eventi nel task **fMRI**. 🎯'''