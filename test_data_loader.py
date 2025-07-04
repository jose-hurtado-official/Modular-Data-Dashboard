from data_loader import load_data

# Test with a valid CSV URL
print(load_data("https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"))

# Test with a valid JSON URL
print(load_data("https://jsonplaceholder.typicode.com/users"))

# Test with a valid local CSV file
# print(load_data("your_local_file.csv"))  # Replace with a real file path

# Test with a valid local JSON file
# print(load_data("your_local_file.json"))  # Replace with a real file path

# Test with an invalid file path
print(load_data("nonexistent.csv"))

# Test with an unsupported file type
print(load_data("file.txt"))
