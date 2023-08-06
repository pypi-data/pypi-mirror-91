def test_case(args, random) -> str:
    # Reading args passed to the stress testing command
    n_limit = int(args[0])
    num_limit = int(args[1])

    # Generating the size of the array randomly
    n = random.randint(1, n_limit)

    # Populating the array with random numbers as strings
    nums = ' '.join([str(random.randint(1, num_limit)) for _ in range(n)])

    # Returning test case content with the correct format
    return f'{n}\n{nums}'
