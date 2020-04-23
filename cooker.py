class Cooker:
    """
    Define basic cooking values
    Parameters:
     name: Name of the cooker
     brand: Brand name
     model: Model number/name
    """
    def __init__(self, name, brand, model):
        super().__init__()
        self.name = name
        self.brand = brand
        self.model = model

    def __repr__(self):
        cooker_str = '''--=[ Cooker: {} ]=--
Brand:        {}
Model:        {}
        '''
        if self.fuel_type:
            cooker_str += f'\rFuel:         {self.fuel_type}\n'
        if self.surf_area:
            cooker_str += f'\rCooking Area: {self.surf_area} sq.in.\n'
        try:
            if self.accessories:
                cooker_str += '\r\tAccessories:\n'
                cooker_str += '\r\t------------\n'
                for k in self.accessories.items():
                    # print(f"KEY: {k}")
                    cooker_str += f'\r\t{k[0]} ({k[1]})\n'
        except AttributeError:
            pass

        return cooker_str.format(self.name, self.brand, self.model)


class Smoker(Cooker):
    """
    Define Smoker as a Cooking Device
    Parameters:
     fuel_type: ['stick', 'pellet', 'coal', 'electric']
     surf_area: integer for square inches
     temp_min:  integer for lowest cooking temp
     temp_max:  integer for maximum cooking temp
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super(Cooker, self).__init__()

    def __repr__(self):
        return super().__repr__()


class Grill(Cooker):
    """
    Define Grill as a Cooking Device
    Parameters:
     fuel_type: ['propane', 'natural gas', 'charcoal', 'electric']
     surf_area: integer for square inches
     temp_min:  integer for lowest cooking temp
     temp_max:  integer for maximum cooking temp
     accessories: dict{'name': 'function',}
     """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super(Cooker, self).__init__()

    def __repr__(self):
        return super().__repr__()


rt_properties: dict = {'name': 'Smoker', 'brand': 'RecTec',
                       'model': 'rt-680', 'fuel_type': 'pellet',
                       'surf_area': 680, 'temp_min': 175, 'temp_max': 500}

cb_properties: dict = {'name': 'Gas Grill',
                       'brand': 'Char-Broil',
                       'model': 'cbcs-700', 'fuel_type': 'propane',
                       'surf_area': 700, 'temp_min': 125, 'temp_max': 700,
                       'accessories': {
                           'rotisserie': 'turns food slowly',
                           'scraper': 'grate matched tool for cleaning'}
                       }

rectec_680 = Smoker(**rt_properties)
charbroil = Grill(**cb_properties)

print(rectec_680)
print(charbroil)
