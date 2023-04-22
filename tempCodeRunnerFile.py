
            password=password[:-1]
    if data=='B':
        if password!="":
            if password==current_password:
                print('Correct Password')
                guessed=True
                ser.write(bytes('part1', 'utf-8'))
            else:
                print('Incorrect Password')
                incorrect_count+=1
                password=""
                if incorrect_count==5:
                    print('Too many incorrect attempts')