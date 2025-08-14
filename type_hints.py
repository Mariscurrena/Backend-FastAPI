### Type Hints ###

my_string_variable = "My string variable"
print(my_string_variable)
print(f"Type is: {type(my_string_variable)}")

### Dynamic Typo
my_string_variable = 5
print(my_string_variable)
print(f"Type is: {type(my_string_variable)}\n\n")

### Typed variable that allows defined the variable type
### This is a weak typo, do not force the data type
### However, helps with the operation and logic that could use each variable
### -----------> FastAPI request use this syntax
my_typed_variable: str = "My typed variable"
print(my_typed_variable)
print(f"Type is: {type(my_typed_variable)}")

my_typed_variable = 5
print(my_typed_variable)
print(f"Type is: {type(my_typed_variable)}\n\n")

### FastAPI example using type hints.
def gretting(first_name: str, last_name: str):
    print(f'Hello, {first_name} {last_name}. Nice to meet you!')
gretting('Angel', 'Mariscurrena')
### This allows FastAPI to understand which value is expected and do not accept any other type