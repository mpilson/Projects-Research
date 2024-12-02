import zstandard as zstd
import chess.pgn

def decompress_zst_file(zst_file_path):
    year, month = zst_file_path[26:30], zst_file_path[31:33]
    output_file_path = f'lichess_{year}_{month}_data.pgn'
    with open(zst_file_path, 'rb') as compressed:
        decomp = zstd.ZstdDecompressor()
        with open(output_file_path, 'wb') as destination:
            decomp.copy_stream(compressed, destination)
    return output_file_path

zst_2013_01_file_path_zst = 'lichess_db_standard_rated_2013-01.pgn.zst'
zst_2014_07_file_path_zst = 'lichess_db_standard_rated_2014-07.pgn.zst'

#decompress_zst_file(zst_2013_01_file_path_zst)
zst_2014_07_file_path_pgn = decompress_zst_file(zst_2014_07_file_path_zst)

def filter_games(pgn_file_path, min_elo = 2000, min_length = 20):
    games = []
    count = 0
    with open(pgn_file_path, 'r') as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            
            white_elo = game.headers.get("WhiteElo", "0")
            black_elo = game.headers.get("BlackElo", "0")
            termination = game.headers.get("Termination","")
            length = len(list(game.mainline_moves()))
            
            # Handle cases where criteria is not defined or game corrupted
            try:
                if (int(white_elo) >= min_elo and int(black_elo) >= min_elo
                    and 'time' not in termination and length >= min_length):
                    games.append(game)
            except ValueError:
                continue
            
            count += 1
            if count % 1000 == 0:
                print(f"Processed {count} games...")
            
    return games


valid_games_2014_07 = filter_games(zst_2014_07_file_path_pgn)

# Optionally, save the filtered games back to a new PGN file
with open('valid_games_2014_07.pgn', 'w') as output_pgn:
    for game in valid_games_2014_07:
        print(game, file=output_pgn, end="\n\n")