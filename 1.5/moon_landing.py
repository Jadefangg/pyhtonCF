#Practic for classes and objects in OOP in Python.
#OOP PRACTICE
class MoonLanding(object):
    def __init__(self,day,month,year):
     self.day=day
     self.month=month
     self.year=year

moon_landing= MoonLanding(20,7,1969)

print("The first moon landing happened on:")
print(f"Day: {moon_landing.day}")
print(f"Month: {moon_landing.month}")
print(f"Year: {moon_landing.year}")