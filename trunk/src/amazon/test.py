import pyaws.ecs as ecs


ecs.setLicenseKey('0ZW74MMABE2VX9H26182')

books = ecs.ItemSearch('python', SearchIndex='Books')

print books[1]
assert(isinstance(books[1], Bag))
ecs.Bag