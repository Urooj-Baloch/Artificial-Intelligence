import chess
import chess.engine

def get_board_score(board, engine, limit=0.1):
    with engine.analysis(board, chess.engine.Limit(time=limit)) as analysis:
        info = analysis.wait()
        return info.get("score", chess.engine.PovScore(chess.engine.Mate(1), board.turn)).pov(board.turn).score(mate_score=10000)

def find_best_moves(board, width, depth, engine):
    current_sequences = [(board.copy(), [], 0)]
    
    for _ in range(depth):
        next_sequences = []
        for current_board, moves, score in current_sequences:
            for move in current_board.legal_moves:
                new_board = current_board.copy()
                new_board.push(move)
                new_moves = moves + [move]
                new_score = get_board_score(new_board, engine)
                next_sequences.append((new_board, new_moves, new_score))
        
        if not next_sequences:
            break
        
        if board.turn == chess.WHITE:
            next_sequences.sort(key=lambda x: -x[2])
        else:
            next_sequences.sort(key=lambda x: x[2])
        
        current_sequences = next_sequences[:width]
    
    if not current_sequences:
        return [], 0
    
    if board.turn == chess.WHITE:
        best = max(current_sequences, key=lambda x: x[2])
    else:
        best = min(current_sequences, key=lambda x: x[2])
    return best[1], best[2]

if __name__ == "__main__":
    engine_path = "path_to_stockfish"
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    
    board = chess.Board()
    
    beam_width = 3
    depth_limit = 2
    
    moves, score = find_best_moves(board, beam_width, depth_limit, engine)
    
    print("Best move sequence:", [move.uci() for move in moves])
    print("Evaluation score:", score)
    
    engine.quit()