def alpha_beta(cards, left, right, is_max_turn, alpha, beta):
    if left > right:
        return 0

    if is_max_turn:
        pick_left = cards[left] + alpha_beta(cards, left + 1, right, False, alpha, beta)
        pick_right = cards[right] + alpha_beta(cards, left, right - 1, False, alpha, beta)
        best = max(pick_left, pick_right)
        alpha = max(alpha, best)
        if beta <= alpha:
            return best
        return best
    else:
        pick_left = alpha_beta(cards, left + 1, right, True, alpha, beta)
        pick_right = alpha_beta(cards, left, right - 1, True, alpha, beta)
        best = min(pick_left, pick_right)
        beta = min(beta, best)
        if beta <= alpha:
            return best
        return best

def play_game(cards):
    print("Initial Cards:", cards)
    left = 0
    right = len(cards) - 1
    max_score = 0
    min_score = 0

    is_max_turn = True

    while left <= right:
        if is_max_turn:
           
            pick_left = cards[left] + alpha_beta(cards, left + 1, right, False, float('-inf'), float('inf'))
            pick_right = cards[right] + alpha_beta(cards, left, right - 1, False, float('-inf'), float('inf'))
            if pick_left >= pick_right:
                choice = cards[left]
                left += 1
            else:
                choice = cards[right]
                right -= 1
            max_score += choice
            print(f"Max picks {choice}, Remaining Cards: {cards[left:right+1]}")
        else:
          
            if cards[left] <= cards[right]:
                choice = cards[left]
                left += 1
            else:
                choice = cards[right]
                right -= 1
            min_score += choice
            print(f"Min picks {choice}, Remaining Cards: {cards[left:right+1]}")
        is_max_turn = not is_max_turn

    print(f"Final Scores - Max: {max_score}, Min: {min_score}")
    if max_score > min_score:
        print("Winner: Max")
    elif min_score > max_score:
        print("Winner: Min")
    else:
        print("It's a Draw!")

cards = [4, 10, 6, 2, 9, 5]
play_game(cards)
