package PhoneBook;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        PhoneBook phoneBook = new PhoneBook();
        Scanner scanner = new Scanner(System.in);
        String command;

        while (true) {
            System.out.print("명령어를 입력하세요 (ADD, SEARCH, EXIT): ");
            command = scanner.nextLine().toUpperCase();

            switch (command) {
                case "ADD":
                    addContact(phoneBook, scanner);
                    break;
                case "SEARCH":
                    searchContact(phoneBook, scanner);
                    break;
                case "EXIT":
                    System.out.println("프로그램을 종료합니다.");
                    scanner.close();
                    return;
                default:
                    System.out.println("유효하지 않은 명령어입니다.");
            }
        }
    }

    private static void addContact(PhoneBook phoneBook, Scanner scanner) {
        System.out.print("이름: ");
        String firstName = scanner.nextLine();
        System.out.print("성: ");
        String lastName = scanner.nextLine();
        System.out.print("닉네임: ");
        String nickname = scanner.nextLine();
        System.out.print("전화번호: ");
        String phoneNumber = scanner.nextLine();
        System.out.print("어두운 비밀: ");
        String darkestSecret = scanner.nextLine();

        if (firstName.isEmpty() || lastName.isEmpty() || nickname.isEmpty() ||
            phoneNumber.isEmpty() || darkestSecret.isEmpty()) {
            System.out.println("모든 필드를 채워야 합니다.");
            return;
        }

        Contact contact = new Contact(firstName, lastName, nickname, phoneNumber, darkestSecret);
        phoneBook.addContact(contact);
        System.out.println("연락처가 저장되었습니다.");
    }

    private static void searchContact(PhoneBook phoneBook, Scanner scanner) {
        int count = phoneBook.getContactCount();
        if (count == 0) {
            System.out.println("저장된 연락처가 없습니다.");
            return;
        }

        // 연락처 목록 출력
        System.out.printf("|%10s|%10s|%10s|%10s|\n", "Index", "First Name", "Last Name", "Nickname");
        for (int i = 0; i < count; i++) {
            Contact c = phoneBook.getContact(i);
            System.out.printf("|%10d|%10s|%10s|%10s|\n",
                    i,
                    truncate(c.getFirstName()),
                    truncate(c.getLastName()),
                    truncate(c.getNickname()));
        }

        // 연락처 상세 보기
        System.out.print("조회할 연락처의 인덱스를 입력하세요: ");
        String input = scanner.nextLine();
        try {
            int index = Integer.parseInt(input);
            Contact c = phoneBook.getContact(index);
            if (c != null) {
                System.out.println("이름: " + c.getFirstName());
                System.out.println("성: " + c.getLastName());
                System.out.println("닉네임: " + c.getNickname());
                System.out.println("전화번호: " + c.getPhoneNumber());
                System.out.println("어두운 비밀: " + c.getDarkestSecret());
            } else {
                System.out.println("유효하지 않은 인덱스입니다.");
            }
        } catch (NumberFormatException e) {
            System.out.println("숫자를 입력해야 합니다.");
        }
    }

    private static String truncate(String str) {
        if (str.length() > 10) {
            return str.substring(0, 9) + ".";
        }
        return String.format("%10s", str);
    }
}
