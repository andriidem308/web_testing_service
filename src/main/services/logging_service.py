passwords_file = 'passwords.txt'


def log_user(user, password):
    with open('passwords.txt', 'a') as filename:
        if user.user.is_teacher:
            filename.write(
                '*** Teacher ***\n'
                f'first_name: {user.user.first_name}\n'
                f'last_name: {user.user.last_name}\n'
                f'full_name: {user.user.first_name} {user.user.last_name}\n'
                f'username: {user.user.username}\n'
                f'email: {user.user.email}\n'
                f'password: {password}\n\n'
            )
        elif user.user.is_student:
            filename.write(
                '*** Student ***\n'
                f'first_name: {user.user.first_name}\n'
                f'last_name: {user.user.last_name}\n'
                f'full_name: {user.user.first_name} {user.user.last_name}\n'
                f'username: {user.user.username}\n'
                f'email: {user.user.email}\n'
                f'password: {password}\n\n'
                f'group: {user.group}\n\n'
                f'teacher: {user.group.teacher}\n\n'
            )
