import pam


def verify_user(username: str, password: str) -> bool:
    p = pam.pam()
    return p.authenticate(username, password)


if __name__ == "__main__":
    user = input("Username: ")
    passwd = input("Password: ")

    if verify_user(user, passwd):
        print("Authentication successful")
    else:
        print("Authentication failed")
