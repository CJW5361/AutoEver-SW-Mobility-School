package PGS;


public class P1 {
    public static int solution(String number){
        int answer=0;

        for (char digit : number.toCharArray()){
            answer+=Character.getNumericValue(digit);
        }
        return answer%9;
    }
    public static void main(String[] args) {
    
        
        // 테스트 케이스
        String number1 = "123";
        String number2 = "78720646226947352489";
        
        System.out.println("Test case 1: " + solution(number1));
        System.out.println("Test case 2: " + solution(number2));
    }
}
