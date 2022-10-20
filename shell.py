import mamba

while True:
    text = input('mamba > ')
    result, error = mamba.run(text)

    if error:
        print(error.as_string())
    else:
        print(result)