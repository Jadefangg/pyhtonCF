class Date(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def get_date(self):
        output = str(self.day) + "/" + str(self.month) + "/" + str(self.year)
        return output

    def set_date(self):
        self.day = int(input("Enter the day of the month: "))
        self.month = int(input("Enter the month: "))
        self.year = int(input("Enter the year: "))


# We'll start our main code from here.
# First, we'll create an instance of Date
# as an object called 'first_moon_landing'.
first_moon_landing = Date(20, 7, 1969)

# Next, we'll print out the date
# with our new getter function.
print(first_moon_landing.get_date())

# Now, let's try changing the date
# with our setter function.
first_moon_landing.set_date()

# Printing out the modified date -
print(first_moon_landing.get_date())