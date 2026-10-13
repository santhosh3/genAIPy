import json

def sum_numbers(*args):
    return sum(args)

print(sum_numbers(1,2,3,4,5))


def display_profile(**kwargs):
    print(json.dumps(kwargs))
    print([key for key in kwargs.keys()])
    print([val for val in kwargs.values()])
    for key,val in kwargs.items():
        print(f"{key}:{val}")


display_profile(name='santhosh',age=45)