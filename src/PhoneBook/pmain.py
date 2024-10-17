from pphonebook import PhoneBook

def main():
    phone_book = PhoneBook()  # 빈 전화번호부 객체 생성

    while True:
        command = input("명령어를 입력하세요 (ADD, SEARCH, EXIT): ").strip().upper()

        if command == "ADD":
            phone_book.add_contact()
        elif command == "SEARCH":
            phone_book.search_contact()
        elif command == "EXIT":
            print("프로그램을 종료합니다.")
            break
        else:
            print("유효하지 않은 명령어입니다.")

if __name__ == "__main__":
    main()