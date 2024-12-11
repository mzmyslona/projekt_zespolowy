class Identity:
    def __init__(self, user):
        self.user = user


    def __str__(self):
        return f"User(username='{self.user}', email='{self.email}')"

class Authorization:
    
