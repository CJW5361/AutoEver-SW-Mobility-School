
/*
 * 문자열 배열 intStrs와 정수 k, s, l가 주어집니다. intStrs의 원소는 숫자로 이루어져 있습니다.

배열 intStrs의 각 원소마다 s번 인덱스에서 시작하는 길이 l짜리 부분 문자열을 잘라내 정수로 변환합니다. 이때 변환한 정수값이 k보다 큰 값들을 담은 배열을 return 하는 solution 함수를 완성해 주세요.

제한사항
0 ≤ s < 100
1 ≤ l ≤ 8
10l - 1 ≤ k < 10l
1 ≤ intStrs의 길이 ≤ 10,000
s + l ≤ intStrs의 원소의 길이 ≤ 120
입출력 예
intStrs	                                       k	s	l	result
["0123456789","9876543210","9999999999999"]	50000	5	5	["98765"]
 */
import java.util.ArrayList;
import java.util.Arrays;

public class P3 {
    public static int[] solution(String[] intStrs, int k, int s, int l) {
        ArrayList<Integer> result = new ArrayList<>();
        
        for (String str : intStrs) {
            
            String subStr = str.substring(s, s + l);
            
          
            int num = Integer.parseInt(subStr);
            
          
            if (num > k) {
                result.add(num);
            }
        }
        
        //int[] 로 변환
        int[] answer = new int[result.size()];
        for (int i = 0; i < result.size(); i++) {
            answer[i] = result.get(i);
        }
        
        return answer;
    }

    public static ArrayList<Integer> solution2(String[] intStrs, int k, int s, int l) {
        ArrayList<Integer> result = new ArrayList<>();
        
        for (String str : intStrs) {
            
            String subStr = str.substring(s, s + l);
            
            
            int num = Integer.parseInt(subStr);
            
            if (num > k) {
                result.add(num);
            }
        }
        
        return result;
    }

    public static void main(String[] args) {
        String[] intStrs = {"0123456789","9876543210","9999999999999"};
        int k = 50000;
        int s = 5;
        int l = 5;
        int[] result = solution(intStrs, k, s, l);
        ArrayList<Integer> result2 =solution2(intStrs, k, s, l);
        System.out.println(Arrays.toString(result));
        System.out.println(result2);


    }
}
