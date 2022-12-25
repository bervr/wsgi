with open('P1010008.jpg', 'rb') as file:
    with open('2/P1010008.jpg', 'wb') as new_file:
        new_file.write(file.read())
