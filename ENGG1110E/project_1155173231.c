/**
 * ENGG1110 Problem Solving by Programming
 *
 * Course Project
 *
 * I declare that the project here submitted is original
 * except for source material explicitly acknowledged,
 * and that the same or closely related material has not been
 * previously submitted for another course.
 * I also acknowledge that I am aware of University policy and
 * regulations on honesty in academic work, and of the disciplinary
 * guidelines and procedures applicable to breaches of such
 * policy and regulations, as contained in the website.
 *
 * University Guideline on Academic Honesty:
 *   https://www.cuhk.edu.hk/policy/academichonesty/
 *
 * Student Name  :Wong Wai Chun
 * Student ID    :1155173231
 * Class/Section :E
 * Date          :13/11/2021
 */

#include <stdio.h>
/* NO other header files are allowed */

/* NO global variables are allowed */

/* Macros used to represent the state of each square */
#define EMPTY 0
#define CIRCLE 1
#define CROSS 2



/* Initialize the game board by setting all squares to EMPTY */
void initGameBoard(int gameBoard[6][7]) {

    // TODO : Complete this part
     for(int i=0;i<6;i++){
        for(int j=0;j<7;j++){
            gameBoard[i][j]=EMPTY;
        }
     }
}



/* Display the game board on the screen.
   You are required to exactly follow the output format stated in the project specification.
   IMPORTANT: Using other output format will result in mark deduction. */
void printGameBoard(int gameBoard[6][7]) {

    // TODO : Complete this part
    for(int i=0;i<6;i++){
            printf("|");
        for(int j=0;j<7;j++){
            if(gameBoard[i][j]==CIRCLE)
                printf("O|");
            else if(gameBoard[i][j]==CROSS)
                printf("X|");
            else
                printf(" |");
        }
        printf("\n");
    }

}



/* Ask the human player to place the mark.
   You can assume that the user input must be an integer. */
void placeMarkByHumanPlayer(int gameBoard[6][7], int mark) {

    // TODO : Complete this part
    int input;
    scanf("%d",&input);
    while(1){
        if((input>=1)&&(input<=7)&&((gameBoard[0][input-1])==EMPTY)){
            break;
        }
        if((input<1)||(input>7)){
            printf("Input out of range. Please input again: \n");
            scanf("%d",&input);
        }
        else if((gameBoard[0][input-1])!=EMPTY){
            printf("Column is full. Please input again: \n");
            scanf("%d",&input);
        }

    }

     for(int i=5;i>=0;i--){
            if(gameBoard[i][input-1]==EMPTY){
                gameBoard[i][input-1]=mark;
                break;
            }
     }

}






/* Return 1 if there is a winner in the game, otherwise return 0.
   Note: the winner is the current player indicated in main(). */
int hasWinner(int gameBoard[6][7]){

    // TODO : Complete this part
    for(int i=0;i<6;i++){
        for(int j=0;j<7;j++){
            if(j<=3&&gameBoard[i][j]!=EMPTY&&gameBoard[i][j]==gameBoard[i][j+1]&&gameBoard[i][j]==gameBoard[i][j+2]&&gameBoard[i][j]==gameBoard[i][j+3]){  //horizontal

                return 1;
            }
            if(i<=2&&gameBoard[i][j]!=EMPTY&&gameBoard[i][j]==gameBoard[i+1][j]&&gameBoard[i][j]==gameBoard[i+2][j]&&gameBoard[i][j]==gameBoard[i+3][j]){ //vertical
                return 1;
            }
            if(i<=2){
                if(j>=3&&gameBoard[i][j]!=EMPTY&&gameBoard[i][j]==gameBoard[i+1][j-1]&&gameBoard[i][j]==gameBoard[i+2][j-2]&&gameBoard[i][j]==gameBoard[i+3][j-3]){// left diagonal
                    return 1;
                }
                if(j<=3&&gameBoard[i][j]!=EMPTY&&gameBoard[i][j]==gameBoard[i+1][j+1]&&gameBoard[i][j]==gameBoard[i+2][j+2]&&gameBoard[i][j]==gameBoard[i+3][j+3]){// right diagonal
                    return 1;
                }
            }
        }
     }
     return 0;
}



/* Return 1 if the game board is full, otherwise return 0. */
int isFull(int gameBoard[6][7]) {

    // TODO : Complete this part
    for(int i=0;i<6;i++){
        for(int j=0;j<7;j++){
            if(gameBoard[i][j]==EMPTY){
                return 0;
            }
        }
     }
     return 1;
}



/* Determine the next move of the computer player.
   You are required to exactly follow the strategy mentioned in the project specification.
   Using other strategies will result in mark deduction. */

// TODO : Write the placeMarkByComputerPlayer(...) function here
void placeMarkByComputerPlayer(int gameBoard[6][7], int mark){

    int v=0;
    for(int i=5;i>=0;i--){
        for(int j=0;j<7;j++){
            if(gameBoard[i][j]==EMPTY){
                gameBoard[i][j]=mark;
                if(hasWinner(gameBoard)&&((gameBoard[i+1][j]!=EMPTY)||i==5)){             //check winning move with bottom have mark
                    v=1;
                    break;
                }
                gameBoard[i][j]=CIRCLE;
                if(hasWinner(gameBoard)&&((gameBoard[i+1][j]!=EMPTY)||i==5)){            //check player winning move with bottom have mark
                    gameBoard[i][j]=mark;            //****
                    v=1;
                    break;
                }
                gameBoard[i][j]=EMPTY;
            }
        }
        if(v){break;}
    }
    if(!v){
        for(int i=5;i>=0;i--){
            for(int j=6;j>=0;j--){
            if(gameBoard[i][j]==EMPTY){
                gameBoard[i][j]=mark;
                v=1;                                    //no winning moves for both players
                break;
                }
            }
         if(v){break;}
        }
    }
}





/* The main function */
int main()
{
    /* Local variables */
    int gameBoard[6][7];    // Each element stores 0 (EMPTY), 1 (CIRCLE), or 2 (CROSS)
    int currentPlayer;      // 1: Player 1             2: Player 2
    int gameContinue;       // 1: The game continues   0: The game ends
    int numOfHumanPlayers;  // 1 or 2

    /* Initialize the local variables */
    initGameBoard(gameBoard);
    currentPlayer = 1;
    gameContinue = 1;
    printf("Enter the number of human players [1-2]:\n");
    scanf("%d", &numOfHumanPlayers);    // You can assume that the user input must be valid

    /* Uncomment the following statements to test whether the printGameBoard() and the placeMarkByHumanPlayer() functions
       are implemented correctly.
       You can add more if you wish.
       After testing, you can delete them or move them elsewhere. */



    /* Game start
       If there are two human players, they are Player 1 and Player 2
       If there is only one human player, he/she is Player 1 and another player is the computer player
       For both cases, Player 1 moves first and places the CIRCLE mark; while Player 2 (or the computer player) places the CROSS mark
       Hint: use a while loop */

    // TODO : Complete this part
    printGameBoard(gameBoard);

    while(gameContinue){

        printf("Player 1's turn:\n");
        placeMarkByHumanPlayer(gameBoard, CIRCLE);
        printGameBoard(gameBoard);
        if(isFull(gameBoard)||hasWinner(gameBoard)){
            if(hasWinner(gameBoard)){
                printf("Congratulations! Player 1 wins!");
            }
            else{
                printf("Draw game.");
            }
            gameContinue=0;
            break;
        }
        if(numOfHumanPlayers==2){
            printf("Player 2's turn:\n");
            placeMarkByHumanPlayer(gameBoard, CROSS);
            printGameBoard(gameBoard);

            if(isFull(gameBoard)||hasWinner(gameBoard)){
                if(hasWinner(gameBoard)&&numOfHumanPlayers==2){
                printf("Congratulations! Player 2 wins!");
                }
                else{
                printf("Draw game.");
                }
                gameContinue=0;
            }
        }
        else {
            printf("Computer's turn:\n");
            placeMarkByComputerPlayer(gameBoard, CROSS);
            printGameBoard(gameBoard);

            if(isFull(gameBoard)||hasWinner(gameBoard)){
                if(hasWinner(gameBoard)){
                    printf("Computer wins!");
                }
                else{
                    printf("Draw game.");
                }
            gameContinue=0;
            }
        }
     }

    return 0;
}
