from function import start

if __name__ == '__main__':
    with open('info.txt', 'r', encoding='utf-8') as file_read:
        for item in file_read:
            item = item.strip('\n')
            if item:
                name_file, result = item.split(' ')
                if result.strip("'"):
                    result = eval(result)
                else:
                    result = result.strip("'")
                print(start(name_file, result))
