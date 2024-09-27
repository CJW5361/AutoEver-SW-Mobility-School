using System;
using System.Data;
using System.Threading;

class Program
{
    static void Main(string[] args)
    {
        // for (int i = 1; i <= 8; i++)
        // {
        //     for (int j = 1; j <= 8 - i; j++)
        //     {
        //         Console.Write(" ");
        //     }

        //     for (int k = 1; k <= 2*i-1; k++)
        //     {   
        //         Console.Write("*");
        //     }
        //     Console.WriteLine();
        // }

    // for (int i = 1, j = 1; i <= 9; j++)
    // {
    //     Console.WriteLine($"{i} * {j} = {i * j}");
    //     if (j == 9)
    //     {
    //         i++;
    //         j = 0;
    //     }
    // }

        // for (int i = 1; i <= 81; i++)
        // {
        //     int dan = (i - 1) / 9 + 1;
        //     int num = (i - 1) % 9 + 1;
        //     Console.WriteLine($"{dan} * {num} = {dan * num}");
        // }
        

        //철수 영희 만수 덕배 4명이서 369게임을 하는데 1000번째 박수치는사람은 누굴까
        //1 2 3 4 5 6 7 8 9 3번
        //10 11 12 13 14 15 16 17 18 19 3번
        //20 21 22 23 24 25 26 27 28 29 3번
        //30 31 32 33 34 35 36 37 38 39 13번
        //40 41 42 43 44 45 46 47 48 49 3번
        //50 51 52 53 54 55 56 57 58 59 3번
        //60 61 62 63 64 65 66 67 68 69 13번
        //70 71 72 73 74 75 76 77 78 79 3번
        //80 81 82 83 84 85 86 87 88 89 3번
        //90 91 92 93 94 95 96 97 98 99 13번
        // int COUNT=1;
        // int total_clap=0;
        
        // while(true){
        //     //박수개수
        //     int clap=0;
        //     int num=COUNT;
        //     while(true){
        //         int num_1=num%10;
        //         if(num_1==3||num_1==6||num_1==9){
        //             clap++;
        //         }
        //         num=num/10;
        //         if(num==0)break;
        //     }
        //     total_clap+=clap;
        
        //     int player = (COUNT-1)%4;

            
        //     Console.WriteLine(player+"번 선수("+clap+"  총 박수: "+total_clap+")");
            
        //     COUNT++;
        //     if (total_clap>=1000){break;}
        // }
        
         String[,] Tetris = {
                {"#", "#", "#" },
                {" ", " ", "#" },
                {" ", " ", " " }
                };
    for (int i = Tetris.GetLength(0) - 1; i >= 0; i--)
    {
        for (int j = Tetris.GetLength(1) - 1; j >= 0; j--)
        {
            Console.Write(Tetris[i, j]);
        }
        Console.WriteLine();
    }

    }   
}