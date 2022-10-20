import mamba

while True:
    text = input('mamba > ')
    result, error = mamba.run("<stdin>", text)

    if error:
        print(error.as_string())
    else:
        print(result)