def age_postfix(age: int) -> str:
    postfix = ""
    last_digit = age%10
    if last_digit == 1:
        postfix = "год"
    elif last_digit < 5 and last_digit > 1:
        postfix = "года"
    else:
        postfix = "лет"
    return postfix