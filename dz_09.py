import re

START_COMMAND = ["hello"]
STOP_COMMAND = ["good bye", "close", "exit"]
ACTION_COMMAND = ["add", "change"]
SHOW_COMMAND = ["phone", "show all"]

PHONE_BOOK = {}

def input_error(func):
    def inner(*args, **kwargs):
        print('''Вас приветствует, PHONE_BOOK! Вы можете выполнить несколько действий:
              --  add Имя Телефон - Добавить новый контакт в PHONE_BOOK
              --  change Имя Телефон - Заменить номер телефона у контакта Имя в PHONE_BOOK
              --  phone Телефон - Узнать Имя указанного телефона в PHONE_BOOK
              --  show all - Вывод всех контактов в PHONE_BOOK
              --  good bye, close, exit - Выход''')
        while True:
            try:
                result = func()
            except SystemExit:
                break
            except IndexError:
                print("Вы ввели неправильное имя или телефон попробуйте еще...")
            except Exception as e:
                print("Error:", e)
    return inner

@input_error
def main():
    text = input("Введите команду и параметры: ")
    result = text.split(" ")
    command = result[0].lower()
    if len(command) == 0:
        print("Вы ничего не ввели, попробуйте ввести команду...")
        
    elif command in START_COMMAND:
        print("Введите одну из команд: add, change, phone, show all, exit")    

    elif command in STOP_COMMAND or " ".join(result[:2]).lower() in STOP_COMMAND:
        print("Good bye!")
        raise SystemExit
    
    elif command in ACTION_COMMAND:
        name = result[1]
        phone = result[2]
        valid_name = valid(name, "name")
        valid_phone = valid(phone, "phone")
        if valid_name and valid_phone:
            asw = action_func(name, phone, command)
            if asw:
                if command == "add":
                    text = f"В PHONE_BOOK добавлен новый контакт с именем: {name} и телефоном: {phone}"
                else: 
                    text = f"В PHONE_BOOK заменен телефон: {phone} для контакт с именем: {name}"
            else:
                if command == "add":
                    text = f"Не удалось сохранить контакт с именем: {name} и телефоном: {phone} в PHONE_BOOK"
                else:
                    text = f"Не удалось найти контакт с именем: {name} в PHONE_BOOK"
            print(text)
        else:
            raise IndexError
        
    elif command in SHOW_COMMAND or " ".join(result[:2]).lower() in SHOW_COMMAND:
        if command == "phone":
            phone = result[1]
            valid_phone = valid(phone, "phone")
            if valid_phone:
                rez_find_phone = find_phone(phone)
                if rez_find_phone == "":
                    print(f"Телефон: {phone}, не найден в PHONE_BOOK")
                else:
                    print(f"Найден телефон: {phone}, он принадлежит контакту: {rez_find_phone}")
            else:
                raise IndexError
        else:
            if len(PHONE_BOOK) == 0:
                print("Вы еще ничего не записали, PHONE_BOOK - пустой")
            count = 0
            for key, value in PHONE_BOOK.items():
                count += 1
                print(('{:<1} {:<10} {:<1}'.format("№", "Имя", "Номер")))
                print(('{:<1} {:<10} {:<1}'.format(count, key, value))) 
            
    else:
        print("У Вас получится, попробуйте ввести команду...")    

def find_phone(phone):
    result = ""
    for key, value in PHONE_BOOK.items():
        if phone == value:
            result = key
            break
    return result
        
def valid(param, type):
    result = False
    try:
        if type == "phone":
            if len(re.search("\+?\d+", param).group()) == len(param):
                result = True
        if type == "name":
            if len(re.search("[А-Яа-яA-za-z]{1,50}", param).group()) == len(param):
                result = True
        return result
    except:
        return result
           
def action_func(name, phone, command):
    if command == "change":
        if PHONE_BOOK.get(name) == None:
            return False
        else:
            PHONE_BOOK[name] = phone
            return True
    else:
        PHONE_BOOK[name] = phone
        return True

main()