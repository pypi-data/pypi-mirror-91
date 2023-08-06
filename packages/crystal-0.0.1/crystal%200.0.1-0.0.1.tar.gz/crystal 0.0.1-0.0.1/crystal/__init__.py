def mismatch(a1, a2):
    d = ((a1-a2) / a2)*100
    return d

print('Cubic mismatch is', abs(mismatch(0.38,0.36)))

