from pwn import *
import stockfish, re

engine = stockfish.Stockfish("/usr/bin/stockfish")
engine.set_depth(20)
engine.set_skill_level(20)

p = remote("20.195.43.216", 8091)

p.sendlineafter(b"(e.g., e2e4): ", b"g2g4")

position = ["g2g4"]

engine.set_position(position)
try:
    while True:
        stdout = p.recvuntil(b"(e.g., e2e4): ").decode("utf8")
        oponent = re.findall(r"Frendy plays: ([a-h][1-8][a-h][1-8])", stdout)[0]
        position.append(oponent)
        engine.set_position(position)
        best_move = engine.get_best_move()
        position.append(best_move)

        p.sendline(best_move.encode())
        print(stdout + best_move)
except:
    p.interactive()