import string
import secrets

_MIN_PASSWORD_LENGTH = 8

_allowed_charsets = {
    'punctuation': string.punctuation,
    'lowercase': string.ascii_lowercase,
    'uppercase': string.ascii_uppercase,
    'numbers': string.digits
}


def _validate_password_length(password_length):
    """
    Function to validate the password length
    """

    if not type(password_length) is int:
        raise TypeError("Password length must be an integer")

    if password_length < _MIN_PASSWORD_LENGTH:

        error_msg = ("Password length cannot be less than "
                     "{0} "
                     "characters").format(_MIN_PASSWORD_LENGTH)

        raise ValueError(error_msg)


def _validate_charsets(include_charsets):
    """
    Function to validate the list of charsets that needs to be
    included the password
    """

    if len(include_charsets) == 0:
        raise ValueError("Character set cannot be empty")

    for charset_label in include_charsets:
        if charset_label not in _allowed_charsets:
            raise ValueError(f"{charset_label} is not a valid charset")


def _validate_no_of_passwords(no_of_passwords):
    """
    Function to validate the number of passwords parameter
    """

    if not type(no_of_passwords) is int:
        raise TypeError("No of passwords must be an integer")

    if no_of_passwords < 1:
        raise ValueError("No of passwords cannot be less than 1")


def generate_password(password_length,
                      include_charsets,
                      no_of_passwords=1):
    """
    Function to generate the random password string
    """

    _validate_password_length(password_length)

    _validate_charsets(include_charsets)

    _validate_no_of_passwords(no_of_passwords)

    password_list = []

    chars = "".join([
        _allowed_charsets[charset_label]
        for charset_label in include_charsets]
        )

    for i in range(no_of_passwords):

        while True:

            password = ''.join(
                secrets.choice(chars)
                for i in range(password_length))

            cond1 = ((any(c in string.punctuation for c in password))
                     if 'punctuation' in include_charsets
                     else True)

            cond2 = ((any(c.islower() for c in password))
                     if 'lowercase' in include_charsets
                     else True)

            cond3 = ((any(c.isupper() for c in password))
                     if 'uppercase' in include_charsets
                     else True)

            cond4 = ((any(c.isdigit() for c in password))
                     if 'numbers' in include_charsets
                     else True)

            if (cond1 and cond2 and cond3 and cond4):
                break

        password_list.append(password)

    return password_list
