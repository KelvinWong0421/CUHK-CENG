def is_happy_year(x):
    y=1

    while y==1:
        x = str(int(x)+1)
        z = [int(i) for i in str(x)]
        if z[0] != z[1] and z[0] != z[2] and z[0]!=z[3] and z[1]!=z[2] and z[1]!=z[3] and z[2]!=z[3]:
            return str(x)
            y = 0

x = input("Enter a year (YYYY): ")

print("The next happy year: "+is_happy_year(x))