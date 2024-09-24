
/*
 * 문제 설명
어떤 문자열에 대해서 접미사는 특정 인덱스부터 시작하는 문자열을 의미합니다. 예를 들어, "banana"의 모든 접미사는 "banana", "anana", "nana", "ana", "na", "a"입니다.
문자열 my_string이 매개변수로 주어질 때, my_string의 모든 접미사를 사전순으로 정렬한 문자열 배열을 return 하는 solution 함수를 작성해 주세요.

제한사항
my_string은 알파벳 소문자로만 이루어져 있습니다.
1 ≤ my_string의 길이 ≤ 100
입출력 예
my_string	result
"banana"	["a", "ana", "anana", "banana", "na", "nana"]
"programmers"	["ammers", "ers", "grammers", "mers", "mmers", "ogrammers", "programmers", "rammers", "rogrammers", "rs", "s"]

 */
import java.util.Arrays;
public class P6 {
    public static String[] solution(String my_string) {
        int length = my_string.length();
        String[] sajun = new String[length];

        for (int i = 0; i < length; i++) {
            sajun[i] = my_string.substring(i);
        }
        Arrays.sort(sajun);
        return sajun;
    }
    public static void main(String[] args) {
    String[] result = solution("banana");
    for (String sajun : result) {   
        System.out.println(sajun);
    }
      
    }
    
}