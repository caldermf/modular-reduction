from modular_reduction import type_a_reduction


result = type_a_reduction("A3", (2, 1, 1), 29)

print("Reduction of the Type A partition (2,1,1) in A3 at q=29:")
print(result.character)
print("")
print("Summands:")
for term in result.terms:
    print(f"  {term.word}: {term.character}")
