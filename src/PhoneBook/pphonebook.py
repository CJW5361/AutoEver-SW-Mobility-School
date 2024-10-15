from pcontact import Contact

class PhoneBook:
    """PhoneBook 클래스는 연락처 배열 관리"""
    
    def __init__(self):
        self.contacts = []  
        self.max_contacts = 8  

    def add_contact(self):
        """연락처 추가 메서드"""
        first_name = input("이름: ").strip()
        last_name = input("성: ").strip()
        nickname = input("닉네임: ").strip()
        phone_number = input("전화번호: ").strip()
        secret = input("비밀: ").strip()

        if not all([first_name, last_name, nickname, phone_number, secret]):
            print("모두 채워야 합니다.")
            return

        contact = Contact(first_name, last_name, nickname, phone_number, secret)
        if len(self.contacts) < self.max_contacts:
            self.contacts.append(contact)  # 리스트에 연락처 추가
        else:
            self.contacts.pop(0)  # 가장 오래된 연락처 제거
            self.contacts.append(contact)  # 새로운 연락처 추가
        print("연락처가 저장되었습니다.")

    def search_contact(self):
        """연락처 검색 메서드"""
        count = len(self.contacts)
        if count == 0:
            print("저장된 연락처가 없습니다.")
            return

        print(f"|{'Index':>10}|{'First Name':>10}|{'Last Name':>10}|{'Nickname':>10}|")
        for i, contact in enumerate(self.contacts):
            print(f"|{i:>10}|{self.truncate(contact.get_first_name()):>10}|{self.truncate(contact.get_last_name()):>10}|{self.truncate(contact.get_nickname()):>10}|")

        try:
            index = int(input("조회할 연락처의 인덱스를 입력하세요: ").strip())
            contact = self.get_contact(index)
            if contact:
                print(f"이름: {contact.get_first_name()}")
                print(f"성: {contact.get_last_name()}")
                print(f"닉네임: {contact.get_nickname()}")
                print(f"전화번호: {contact.get_phone_number()}")
                print(f"비밀: {contact.get_secret()}")
            else:
                print("유효하지 않은 인덱스입니다.")
        except ValueError:
            print("숫자를 입력해야 합니다.")

    def get_contact(self, index):
        """인덱스로 연락처 가져오기"""
        if 0 <= index < len(self.contacts):
            return self.contacts[index]
        return None

    def truncate(self, text):
        """문자열을 10자로 잘라주는 메서드"""
        return text[:9] + '.' if len(text) > 10 else text