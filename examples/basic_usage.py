from modular_reduction import KLSBasisSystem, published_table


system = KLSBasisSystem("A2")
w = system.context.element_from_word("s1")

print("M_s1 in type A2 at q=11:")
print(system.mw(w, 11))
print("")

table = published_table("A2", 11)
print("Published rows:")
for row in table.rows:
    print(f"  {row.word}: {row.character}")
print("")
print("Paper reference:")
print(table.source.provenance.paper_reference)
