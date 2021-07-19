'''
Code to test pymc functions
'''
# Import class from pymc
from pymc import CreateTissue

# Create tissue object
# Note: This creates a 200*200*200 tissue structure 
#       and saves it as a binary file.
tissue = CreateTissue(0.1, 0.15, 0.75, 200)

print(' ')
print(tissue)
print(' ')

# print('Default tissue binsize is: ' + str(tissue.binsize))
# tissue.view()
# print(' ')
# tissue.set_thickness(1.50)
# print('Update tissue binsize is: ' + str(tissue.binsize))
# print(' ')
# tissue.view()

tissue.run_monte_carlo(10.0)

