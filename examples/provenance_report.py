from modular_reduction import basis_data, provenance


report = provenance("B3")
print("B3 provenance:")
print(report.json())
print("")

dataset = basis_data("B3", only_near_involutions=True, q_value=29)
print("First near-involution basis datum:")
print(dataset.data[0].as_dict())
