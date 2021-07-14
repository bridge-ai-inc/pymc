from pymc import CreateTissue

tissue = CreateTissue(0.1, 0.15, 0.75, 200)

print('tissue id is: ' + tissue.id)
print(tissue)
tissue.view()
# tissue.save('my_test_tissue')
# tissue.run_monte_carlo(10.0)