class Crate:
    def __init__(self, initial_multiplier, inhabitatnts):
        self.initial_multiplier = initial_multiplier
        self.inhabitatnts = inhabitatnts
    
    def get_min_percentage(self, target_multiplier):
        return (self.initial_multiplier / target_multiplier) - self.inhabitatnts
    
    def __repr__(self):
        return f"Crate({self.initial_multiplier}, {self.inhabitatnts})"

def sort_by_percent(crates, percent_to_be_profitable):
    for i in range(0, len(crates) - 1):
        for j in range(0, len(crates) - 1 - i):
            if crates[j].get_min_percentage(percent_to_be_profitable) > crates[j + 1].get_min_percentage(percent_to_be_profitable):
                temp = crates[j]
                crates[j] = crates[j + 1]
                crates[j + 1] = temp

"""
def test(crates):
    for i in range(0, len(crates) - 1):
        for j in range(0, len(crates) - 1 - i):
            if crates[j] > crates[j + 1]:
                temp = crates[j]
                crates[j] = crates[j + 1]
                crates[j + 1] = temp

a = [21, 1, 5, 4, 3, 7, 6, 8, 2, 9, 10, 13, 14, 12, 15, 16, 19, 20, 17, 18, 11]
test(a)
print(a)
"""

percent_to_be_profitable = 5
crates = [Crate(10, 1), Crate(80, 6), Crate(37, 3),
          Crate(90, 10), Crate(31, 2), Crate(50, 4),
          Crate(20, 2), Crate(73, 4), Crate(89, 8)]

sort_by_percent(crates, percent_to_be_profitable)

print("Min % of people needed for crate to be profitable (lowest to highest):")
print("Note: Formatting is Crate(multiplier, inhabitants)")
for crate in crates:
    print(f"{crate}: {crate.get_min_percentage(percent_to_be_profitable)}%")