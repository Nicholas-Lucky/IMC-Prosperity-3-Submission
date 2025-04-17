class Suitcase:
    def __init__(self, initial_multiplier, contestants):
        self.initial_multiplier = initial_multiplier
        self.contestants = contestants
    
    def get_max_percentage(self, target_multiplier):
        return (self.initial_multiplier / target_multiplier) - self.contestants
    
    def __repr__(self):
        return f"Suitcase({self.initial_multiplier}, {self.contestants})"

def sort_by_percent(suitcases, max_percent_to_be_profitable):
    for i in range(0, len(suitcases) - 1):
        for j in range(0, len(suitcases) - 1 - i):
            if suitcases[j].get_max_percentage(max_percent_to_be_profitable) > suitcases[j + 1].get_max_percentage(max_percent_to_be_profitable):
                temp = suitcases[j]
                suitcases[j] = suitcases[j + 1]
                suitcases[j + 1] = temp

max_percent_to_be_profitable = 10
suitcases = [Suitcase(80, 6), Suitcase(50, 4), Suitcase(83, 7), Suitcase(31, 2), Suitcase(60, 4),
             Suitcase(89, 8), Suitcase(10, 1), Suitcase(37, 3), Suitcase(70, 4), Suitcase(90, 10),
             Suitcase(17, 1), Suitcase(40, 3), Suitcase(73, 4), Suitcase(100, 15), Suitcase(20, 2),
             Suitcase(41, 3), Suitcase(79, 5), Suitcase(23, 2), Suitcase(47, 3), Suitcase(30, 2)]

sort_by_percent(suitcases, max_percent_to_be_profitable)
percent_sum = 0.0

print(f"MAX % of people needed for suitcase to be profitable (final multiplier of at least {max_percent_to_be_profitable}x):")
print("Note: Order is lowest to highest, and formatting is Suitcase(multiplier, contestants)")
for suitcase in suitcases:
    max_percentage = suitcase.get_max_percentage(max_percent_to_be_profitable)
    print(f"{suitcase}: {max_percentage}%")

    if max_percentage >= 0:
        percent_sum += max_percentage

print(f"Sum of the max percentages (excluding negative percentages) ^^ = {percent_sum}%")
