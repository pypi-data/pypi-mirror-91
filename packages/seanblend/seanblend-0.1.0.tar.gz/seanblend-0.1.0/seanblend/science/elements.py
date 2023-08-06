class Element:
    def data(self):
        print(f"Name: {self.name}\nChemical Symbol: {self.chemical_symbol}\nAtomic Mass: {self.atomic_mass}\nAtomic Number: {self.atomic_number}\ntype: {self.type}")


class Hydrogen(Element):
    name = "Hydrogen"
    chemical_symbol = "H"
    atomic_mass = 1.0079
    atomic_number = 1
    type = "Reactive Metals"

class Helium(Element):
    name = "Helium"
    chemical_symbol = "He"
    atomic_mass = 4.0026
    atomic_number = 2
    type = "Mainly Non-metals"

class Lithium(Element):
    name = "Lithium"
    chemical_symbol = "Li"
    atomic_mass = 6.941
    atomic_number = 3
    type = "Reactive Metals"

class Beryllium(Element):
    name = "Beryllium"
    chemical_symbol = "Be"
    atomic_mass = 9.0122
    atomic_number = 4
    type = "Reactive Metals"