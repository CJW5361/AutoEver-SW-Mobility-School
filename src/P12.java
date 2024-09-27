/*
 * 알파벳 대소문자로만 이루어진 문자열 my_string이 주어질 때, my_string에서 'A'의 개수, my_string에서 'B'의 개수,..., my_string에서 'Z'의 개수, my_string에서 'a'의 개수, my_string에서 'b'의 개수,..., my_string에서 'z'의 개수를 순서대로 담은 길이 52의 정수 배열을 return 하는 solution 함수를 작성해 주세요.

제한사항
1 ≤ my_string의 길이 ≤ 1,000
입출력 예
my_string	result
"Programmers"	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0]

 */
import java.util.Arrays;
public class P12 {
    public static int[] solution(String myString) {
        int[] result = new int[52];
        
        for (char c : myString.toCharArray()) {
            if (Character.isUpperCase(c)) {
                result[c - 'A']++;
            } else if (Character.isLowerCase(c)) {
                result[c - 'a' + 26]++;
            }
        }
        
        return result;
    }
    public static void main(String[] args) {
        System.out.println(Arrays.toString(solution("Programmers")));    
    }
}
