from fitpy import Person, Body, Running, Database


def main():
    name = input('Your Name: ')
    age = int(input('Your Age: '))
    height = float(input('Your height: '))
    weight = float(input('Your weight: '))
    hormonal_sex = str(input('Your hormonal sex: '))

    p = Person(name)
    b = Body(age, height, weight, hormonal_sex)

    d = p.asdict() | b.asdict()

    print('''Options:
        1 See overview
        2 Save data
        ''')

    option = input('Enter number: ')
    if option == '1':
        print(p.__str__() + b.__str__())

    elif option == '2':
        print('NotIplemented')



if __name__ == '__main__':
    main()
