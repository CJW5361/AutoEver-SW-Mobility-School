class Contact:
  
    def __init__(self, first_name, last_name, nickname, phone_number,secret):
        self.first_name = first_name  
        self.last_name = last_name    
        self.nickname = nickname      
        self.phone_number = phone_number  
        self.secret = secret  

    # 각 필드의 getter 메서드
    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_nickname(self):
        return self.nickname

    def get_phone_number(self):
        return self.phone_number

    def get_secret(self):
        return self.secret