/*
 * 문제 설명
문자열 my_string과 정수 s, e가 매개변수로 주어질 때, my_string에서 인덱스 s부터 인덱스 e까지를 뒤집은 문자열을 return 하는 solution 함수를 작성해 주세요.

제한사항
my_string은 숫자와 알파벳으로만 이루어져 있습니다.
1 ≤ my_string의 길이 ≤ 1,000
0 ≤ s ≤ e < my_string의 길이
입출력 예
my_string	s	e	result
"Progra21Sremm3"	6	12	"ProgrammerS123"
"Stanley1yelnatS"	4	10	"Stanley1yelnatS"

 */
//reverse() 메소드를 제공하는 StringBuilder/StringBuffer 클래스를 이용한다. 
//출처: https://yangbox.tistory.com/59 [양's World:티스토리]

public class P9 {
    public static String solution(String my_string, int s, int e) {
        String answer = "";
        String reverse= my_string.substring(s,e+1);
        StringBuffer sb=new StringBuffer(reverse);
        reverse=sb.reverse().toString();
        answer=my_string.substring(0,s)+reverse+my_string.substring(e+1);
        
        
        
        return answer;
    }

    public static String solution2(String my_string, int s, int e) {

        char[] spell = my_string.toCharArray();

        for (int i = s; i < e; i++) {
            char tmp = spell[i];
            spell[i] = spell[e];
            spell[e] = tmp;
            e--;
        }

        String answer = "";
        for (char c : spell) {
            answer += c;
        }
        return answer;
    }


    public static void main(String[] args) {
        System.out.println(solution("Progra21Sremm3", 6, 12)); // "ProgrammerS123"
        System.out.println(solution("Stanley1yelnatS", 4, 10)); // "Stanley1yelnatS"

        System.out.println(solution2("Progra21Sremm3", 6, 12)); // "ProgrammerS123"
        System.out.println(solution2("Stanley1yelnatS", 4, 10)); // "Stanley1yelnatS"
    }
}
