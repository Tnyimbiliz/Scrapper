# Initialize set to store seen multipliers
list = [0,1,2,2,4,5]

initial_multipliers = list
seen_multipliers = initial_multipliers[:1]

print(f"initial {initial_multipliers}")

while list:
    new_multipliers = list
    second_multiplier = new_multipliers[1]
    new_multipliers = new_multipliers[:1]

    print("--------------------")
    print(f"new {new_multipliers[0]}")   
    print(f"seen {seen_multipliers[0]}")
    print(f"second {second_multiplier}")
    print("--------------------")

    new_values = [value for value in new_multipliers if value not in seen_multipliers]

    if new_values:
        print(f"✅ {new_values[0]}")
        seen_multipliers = (seen_multipliers + new_values)[-1:]

    if second_multiplier == new_multipliers[0]:
        print("repeated value!!!!!!!!!!!!!")
        print(f"✅ {new_values[0]}")
        new_values = [second_multiplier]

    list.pop(0)
