import math


def minimax(board, depth, maximizing, alpha, beta):
    # Terminal states
    if winner(board, 'O'):
        return 10 - depth

    if winner(board, 'X'):
        return depth - 10

    if ' ' not in board:
        return 0

    if maximizing:
        best = -math.inf

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'

                score = minimax(board, depth + 1, False, alpha, beta)

                board[i] = ' '

                best = max(best, score)
                alpha = max(alpha, best)

                # Alpha-Beta pruning
                if beta <= alpha:
                    break

        return best

    else:
        best = math.inf

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'

                score = minimax(board, depth + 1, True, alpha, beta)

                board[i] = ' '

                best = min(best, score)
                beta = min(beta, best)

                # Alpha-Beta pruning
                if beta <= alpha:
                    break

        return best


def winner(board, player):
    winning_positions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] == player:
            return True

    return False


def display_board(board):
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()


def best_move(board):
    best_score = -math.inf
    move = -1

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'

            score = minimax(
                board,
                0,
                False,
                -math.inf,
                math.inf
            )

            board[i] = ' '

            if score > best_score:
                best_score = score
                move = i

    return move


def main():
    board = [' '] * 9

    print("Tic-Tac-Toe using Minimax with Alpha-Beta Pruning")
    print("Positions are numbered from 0 to 8.")

    while True:
        display_board(board)

        # Human move
        try:
            position = int(input("Enter your move (0-8): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if position < 0 or position > 8:
            print("Enter a number between 0 and 8.")
            continue

        if board[position] != ' ':
            print("Position already occupied.")
            continue

        board[position] = 'X'

        if winner(board, 'X'):
            display_board(board)
            print("You win!")
            break

        if ' ' not in board:
            display_board(board)
            print("Draw!")
            break

        # AI move
        position = best_move(board)
        board[position] = 'O'

        print("AI selected position:", position)

        if winner(board, 'O'):
            display_board(board)
            print("AI wins!")
            break

        if ' ' not in board:
            display_board(board)
            print("Draw!")
            break


if __name__ == "__main__":
    main()