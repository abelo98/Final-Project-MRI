t = """.W
the buckling shear stress of simply-supported infinitely
long plates with transverse stiffeners .
  this report is an extension of previous theoretical
investigations of the elastic buckling in shear of flat
plates reinforced by transverse stiffeners . the plates are treated
as infinitely long and simply-supported along the long
sides . stiffeners are spaced at regular intervals, dividing the plate
into a number of panels of uniform size . the effect
ob bending and torsional stiffnesses of the stiffener upon the buckling
shear stress is calculated for the complete range
of stiffnesses, for panels with ratios of width to stiffener spacing of
graphical forms ."""

z = t.split(".I")
# print(z)

def a(x):
    while x < 10:
        x += 1
    return x

print(a(1))
