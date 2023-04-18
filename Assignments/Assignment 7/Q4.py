def Newton_Raphson(f, f_dash, ɛ, debug=False, x0=0):
    x = x0
    x0 = x+10*ɛ

    if debug: count = 0

    while abs(x-x0) > ɛ:
        x, x0 = x - (f(x)/f_dash(x)), x

        count += 1


    if debug: return {"x": x, "f(x)": f(x), "count": count}
    return x

def Secant(f, ɛ, debug=False, x0=0):
    x = x0
    x0 = x+10*ɛ  #Arbitrary number

    if debug: count = 0

    while abs(x-x0) > ɛ:
        x, x0 = x - (f(x)*(x-x0)/(f(x) - f(x0))), x

        if debug: count += 1

    if debug: return {"x": x, "f(x)": f(x), "count": count}
    return x


if __name__ == '__main__':
    import math

    ## Case 1
    f = lambda x: x + 3
    f_dash = lambda x: 1
    ɛ = 0.0001

    nr = Newton_Raphson(f, f_dash, ɛ, debug=True)
    sc = Secant(f, ɛ, debug=True)
    assert(abs(nr["x"] - (-3)) < ɛ)
    assert(abs(sc["x"] - (-3)) < ɛ)
    print()
    print("f(x) = x + 3")
    print("Newton-Raphson:")
    [print(x, ":", nr[x], end="\t") for x in nr]
    print()
    print("Secant:")
    [print(x, ":", sc[x], end="\t") for x in sc]
    print()

    ## Case 2
    f = lambda x: x**3 - 2*x + 2
    f_dash = lambda x: 3*x**2 - 2
    ɛ = 0.001

    nr = Newton_Raphson(f, f_dash, ɛ, debug=True, x0=-1) # starting at -1 as x=0 will lead to a minima
    sc = Secant(f, ɛ, debug=True, x0=-1)
    print()
    print("f(x) = x³ - 2x + 2")
    print("Newton-Raphson:")
    [print(x, ":", nr[x], end="\t") for x in nr]
    print()
    print("Secant:")
    [print(x, ":", sc[x], end="\t") for x in sc]
    print()

    ## Case 3
    f = lambda x: math.exp(x) - x**3
    f_dash = lambda x: math.exp(x) - 3*x**2
    ɛ = 0.00001

    nr = Newton_Raphson(f, f_dash, ɛ, debug=True)
    sc = Secant(f, ɛ, debug=True)
    print()
    print("f(x) = eˣ - x³")
    print("Newton-Raphson:")
    [print(x, ":", nr[x], end="\t") for x in nr]
    print()
    print("Secant:")
    [print(x, ":", sc[x], end="\t") for x in sc]
    print()


