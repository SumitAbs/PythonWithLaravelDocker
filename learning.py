# List Array in Python
skills = ["Laravel", "PHP", "Cloud", "Python"]

print("My Learning Path:")
for item in skills:
    print(f"- I am learning {item}")

    # a simple logic check
    if "Python" in skills:
        print("\nNext goal: Master Python for Cloud!")