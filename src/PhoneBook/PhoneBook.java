package PhoneBook;

public class PhoneBook {
    private Contact[] contacts;
    private int contactCount;

    public PhoneBook() {
        this.contacts = new Contact[8];
        this.contactCount = 0;
    }

    public void addContact(Contact contact) {
        if (contactCount < 8) {
            contacts[contactCount] = contact;
            contactCount++;
        } else {
            // 가장 오래된 연락처를 덮어씀
            for (int i = 1; i < 8; i++) {
                contacts[i - 1] = contacts[i];
            }
            contacts[7] = contact;
        }
    }

    public Contact getContact(int index) {
        if (index >= 0 && index < contactCount) {
            return contacts[index];
        }
        return null;
    }

    public int getContactCount() {
        return contactCount;
    }
}
