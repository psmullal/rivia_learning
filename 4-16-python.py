class Monitor:
    """Class definition for tracking Monitor types"""
    def __init__(self, monitor_make: str, monitor_model: str) -> None:
        self.m_make = monitor_make
        self.m_model = monitor_model

    def set_properties(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    # def set_connection(self, connection_types: list) -> None:
    #     setattr(self, 'connection_types', connection_types)
    def get_rando(self, evenodd):
        choice = ['m_make', 'm_model']
        if evenodd % 2:
            self.rando = choice[0]
        else:
            self.rando = choice[1]
        return self.rando

    def __repr__(self):
        return(f"{self.m_make}: {self.m_model}\n{self.x_res}x{self.y_res}")

    def __str__(self) -> str:
        monitor_desc: str = '''
Monitor Manufacturer:   {}
Monitor Make:           {}
Resolution:             {} x {}
Connection Types:       {}
Owner:                  {}
        '''

        return(monitor_desc.format(self.m_make, self.m_model,
               self.x_res, self.y_res, ', '.join(self.connection_types),
               self.owner))


apple = Monitor('Apple', 'Thunderbolt')
# apple.set_resoltion(2560, 1440)
# apple.set_connection(['Lightning', 'USB-C'])

properties = {'x_res': 2560, 'y_res': 1440,
              'connection_types': ['Lightning', 'USB-C'],
              'owner': "Miles"}
apple.set_properties(**properties)

dell = Monitor('Dell', 'Curved')
d_properties = {'x_res': 888860, 'y_res': 1440000,
                'connection_types': ['Lightning', 'USB-C', 'HDMI'],
                'owner': "Pat"}
dell.set_properties(**d_properties)
# apple.computers_compatible(**manufacturers)

# print(apple.__repr__())
print(dell.get_rando(15))
print(apple)
print(dell)


'''
# LiveCode session https://livecode.amazon.jobs/session/9ce37638-acf9-4aed-bce9-53f5c4da5a3c


# class Vehicle:
#     """Vehicle class"""

#     def __init__(self, wheels, doors, electric=False):
#         self.wheels: int = wheels
#         self.doors: int = doors
#         self.electric: bool = electric
#         self.plate: string = self.generate_license_plate()

#     def __str__(self):
#         return f"Vehicle: [wheels = {self.wheels}, doors = {self.doors}, electrics = {self.electric}, \
#         plate = {self.plate}]"

#     @staticmethod
#     def generate_license_plate():
#         """generate license plate (ex: 1a2b3c4d)"""
#         plate = ""
#         for x in range(0, 8):
#             if x % 2 == 0:
#                 plate += str(random.randint(0, 9))
#             else:
#                 plate += random.choice(string.ascii_lowercase)
#         return plate


# class Coupe(Vehicle):
#     """Coupe extends vehicle"""

#     def __init__(self, convertible, doors=2):
#         super().__init__(wheels, doors, electric)
#         self.convertible: bool = convertible

#     def __str__(self):
#         return f"Coupe: [wheels = {self.wheels}, doors = {self.doors}, electrics = {self.electric}, \
#         convertible = {self.convertible}], plate = {self.plate}"

'''