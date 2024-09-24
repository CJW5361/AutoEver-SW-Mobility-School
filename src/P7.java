

public class P7 {
    public static String solution(String my_string, int n) {
       
        String answer=my_string.substring(0,n);
        return answer;
    }
    public static void main(String[] args) {

        System.out.println(solution("ProgrammerS123", 11)); // 출력: "ProgrammerS"
        System.out.println(solution("He110W0r1d", 5));      // 출력: "He110"
    
    }
      
}
    
