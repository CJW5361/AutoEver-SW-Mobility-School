class Person {
    private String name;
    private int age;

    // 생성자
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // getter 메서드
    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    // setter 메서드
    public void setName(String name) {
        this.name = name;
    }

    public void setAge(int age) {
        this.age = age;
    }
}

public class Main {
    public static void main(String[] args) {
        Person person = new Person("홍길동", 25);
        System.out.println("이름: " + person.getName());
        System.out.println("나이: " + person.getAge());
    }
}
