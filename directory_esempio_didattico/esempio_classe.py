#esempio studido:
#alberto, giovanni
alberto_altezza  =1.75
alberto_peso = 80
alberto_eta = 22

giovanni_altezza  =1.75
giovanni_peso = 80
giovanni_eta = 22

#esempio migliore
class Persona:
    def __init__(self, altezza,peso,eta,nome_completo):
        self.altezza = altezza #attributi ...
        self.peso = peso
        self.eta = eta
        self.nome_completo = nome_completo

    def presentati(self, quante_volte): #metodo
        for i in range(quante_volte):
            print('ciao! mi chiamo '+ self.nome_completo)

giovanni = Persona(altezza = 1.8, eta  =57,peso = 57, nome_completo='Giovanni Muciaccia')
print(giovanni.altezza)

giovanni.presentati(10)
