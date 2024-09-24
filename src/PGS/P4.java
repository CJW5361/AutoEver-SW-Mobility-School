package PGS;
/*
 * 길이가 같은 문자열 배열 my_strings와 이차원 정수 배열 parts가 매개변수로 주어집니다. parts[i]는 [s, e] 형태로, my_string[i]의 인덱스 s부터 인덱스 e까지의 부분 문자열을 의미합니다. 각 my_strings의 원소의 parts에 해당하는 부분 문자열을 순서대로 이어 붙인 문자열을 return 하는 solution 함수를 작성해 주세요.

제한사항
1 ≤ my_strings의 길이 = parts의 길이 ≤ 100
1 ≤ my_strings의 원소의 길이 ≤ 100
parts[i]를 [s, e]라 할 때, 다음을 만족합니다.
0 ≤ s ≤ e < my_strings[i]의 길이
입출력 예
my_strings	parts	result
["progressive", "hamburger", "hammer", "ahocorasick"]	[[0, 4], [1, 2], [3, 5], [7, 7]]	"programmers"
 */
public class P4 {
    public static String solution(String[] my_strings, int[][] parts) {
        String answer = "";
        for(int i=0;i<my_strings.length;i++){
            int s=parts[i][0];
            int e=parts[i][1];

            String str=my_strings[i];
            
            answer+=str.substring(s,e+1);
        } 

        return answer;
    }
    public static void main(String[] args) {
        String[] my_strings={"progressive", "hamburger", "hammer", "ahocorasick"};
        int[][] parts={{0, 4}, {1, 2}, {3, 5}, {7, 7}};
        System.out.println(solution(my_strings, parts));
    }
    
}
