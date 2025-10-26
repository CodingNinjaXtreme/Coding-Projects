import sys
import pygame
from pygame import Rect
from pathlib import Path
import random
import math
import threading
import time

# --- Configuration ---
WINDOW_SIZE = 640
FPS = 60
ASSET_DIR = Path('..')  # images in working directory
AI_ENABLED = True
AI_COLOR = 'b'
AI_DEPTH = 2
AI_MOVE_DELAY = 0.6  # seconds

PIECE_FILES = {
    ('w', 'K'): 'white_king.png', ('w', 'Q'): 'white_queen.png',
    ('w', 'R'): 'white_rook.png', ('w', 'B'): 'white_bishop.png',
    ('w', 'N'): 'white_knight.png', ('w', 'P'): 'white_pawn.png',
    ('b', 'K'): 'black_king.png', ('b', 'Q'): 'black_queen.png',
    ('b', 'R'): 'black_rook.png', ('b', 'B'): 'black_bishop.png',
    ('b', 'N'): 'black_knight.png', ('b', 'P'): 'black_pawn.png',
}

PIECE_VALUES = {'K':900,'Q':90,'R':50,'B':30,'N':30,'P':10}

# --- Load Images ---
def load_images(square_size):
    imgs = {}
    for key, fname in PIECE_FILES.items():
        path = ASSET_DIR / fname
        if path.exists():
            img = pygame.image.load(str(path)).convert_alpha()
            img = pygame.transform.scale(img, (square_size, square_size))  # crisp scaling
            imgs[key] = img
    board_img = None
    board_path = ASSET_DIR / 'board.png'
    if board_path.exists():
        board_img = pygame.image.load(str(board_path)).convert()
        board_img = pygame.transform.scale(board_img, (square_size*8, square_size*8))
    return imgs, board_img

# --- Chess Board ---
class Board:
    def __init__(self):
        self.squares = [[None]*8 for _ in range(8)]
        self.setup_start()

    def setup_start(self):
        self.squares[0] = [('b','R'),('b','N'),('b','B'),('b','Q'),('b','K'),('b','B'),('b','N'),('b','R')]
        self.squares[1] = [('b','P')]*8
        for r in range(2,6): self.squares[r] = [None]*8
        self.squares[6] = [('w','P')]*8
        self.squares[7] = [('w','R'),('w','N'),('w','B'),('w','Q'),('w','K'),('w','B'),('w','N'),('w','R')]

    def in_bounds(self,r,c): return 0<=r<8 and 0<=c<8
    def piece_at(self,r,c): return self.squares[r][c] if self.in_bounds(r,c) else None

    def push_move(self,sr,sc,tr,tc):
        piece=self.squares[sr][sc]
        captured=self.squares[tr][tc]
        self.squares[tr][tc]=piece
        self.squares[sr][sc]=None
        promoted=False
        if piece and piece[1]=='P' and ((piece[0]=='w' and tr==0) or (piece[0]=='b' and tr==7)):
            self.squares[tr][tc]=(piece[0],'Q')
            promoted=True
        return captured,promoted,piece

    def undo_move(self,sr,sc,tr,tc,captured,promoted,piece):
        if promoted: self.squares[sr][sc]=piece; self.squares[tr][tc]=captured
        else: self.squares[sr][sc]=piece; self.squares[tr][tc]=captured

    def move_piece(self,sr,sc,tr,tc):
        piece=self.squares[sr][sc]
        self.squares[tr][tc]=piece
        self.squares[sr][sc]=None
        if piece and piece[1]=='P' and ((piece[0]=='w' and tr==0) or (piece[0]=='b' and tr==7)):
            self.squares[tr][tc]=(piece[0],'Q')

    def generate_moves(self,r,c):
        piece=self.piece_at(r,c)
        if not piece: return []
        color,kind=piece
        moves=[]
        enemy=lambda rr,cc:self.in_bounds(rr,cc) and self.piece_at(rr,cc) and self.piece_at(rr,cc)[0]!=color
        empty=lambda rr,cc:self.in_bounds(rr,cc) and self.piece_at(rr,cc) is None

        if kind=='P':
            dirr=-1 if color=='w' else 1
            if empty(r+dirr,c): moves.append((r+dirr,c))
            start_row=6 if color=='w' else 1
            if r==start_row and empty(r+dirr*2,c): moves.append((r+dirr*2,c))
            for dc in (-1,1):
                rr,cc=r+dirr,c+dc
                if enemy(rr,cc): moves.append((rr,cc))
        elif kind=='N':
            for dr,dc in ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)):
                rr,cc=r+dr,c+dc
                if self.in_bounds(rr,cc) and (self.piece_at(rr,cc) is None or self.piece_at(rr,cc)[0]!=color):
                    moves.append((rr,cc))
        elif kind in ('B','R','Q'):
            directions=[]
            if kind in ('B','Q'): directions+=[(-1,-1),(-1,1),(1,-1),(1,1)]
            if kind in ('R','Q'): directions+=[(-1,0),(1,0),(0,-1),(0,1)]
            for dr,dc in directions:
                rr,cc=r+dr,c+dc
                while self.in_bounds(rr,cc):
                    if self.piece_at(rr,cc) is None: moves.append((rr,cc))
                    else:
                        if self.piece_at(rr,cc)[0]!=color: moves.append((rr,cc))
                        break
                    rr+=dr; cc+=dc
        elif kind=='K':
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr==0 and dc==0: continue
                    rr,cc=r+dr,c+dc
                    if self.in_bounds(rr,cc) and (self.piece_at(rr,cc) is None or self.piece_at(rr,cc)[0]!=color):
                        moves.append((rr,cc))
        return moves

    def all_color_moves(self,color):
        res=[]
        for r in range(8):
            for c in range(8):
                p=self.piece_at(r,c)
                if p and p[0]==color:
                    for (tr,tc) in self.generate_moves(r,c): res.append((r,c,tr,tc))
        return res

# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.square=WINDOW_SIZE//8
        self.screen=pygame.display.set_mode((self.square*8,self.square*8))
        pygame.display.set_caption('Chess')
        self.clock=pygame.time.Clock()
        self.images,self.board_img=load_images(self.square)
        self.board=Board()
        self.selected=None
        self.legal_moves=[]
        self.turn='w'
        self.font=pygame.font.SysFont(None,24)
        self.ai_thinking=False
        self.ai_thread=None
        self.lock=threading.RLock()

    def coord_to_pixels(self,r,c): return c*self.square,r*self.square
    def pixels_to_coord(self,x,y): return min(7,max(0,y//self.square)),min(7,max(0,x//self.square))

    def draw(self, moving_piece=None, piece_pos=None):
        if self.board_img: self.screen.blit(self.board_img,(0,0))
        else:
            colors=[(240,217,181),(181,136,99)]
            for r in range(8):
                for c in range(8):
                    pygame.draw.rect(self.screen,colors[(r+c)%2],Rect(c*self.square,r*self.square,self.square,self.square))
        if self.selected:
            r,c=self.selected
            pygame.draw.rect(self.screen,(50,200,50),Rect(c*self.square+2,r*self.square+2,self.square-4,self.square-4),3)
        for mr,mc in self.legal_moves:
            center=(mc*self.square+self.square//2,mr*self.square+self.square//2)
            pygame.draw.circle(self.screen,(50,50,200),center,max(6,self.square//10))
        for r in range(8):
            for c in range(8):
                p=self.board.piece_at(r,c)
                if p and (moving_piece!=p or piece_pos!=self.coord_to_pixels(r,c)):
                    img=self.images.get(p)
                    px,py=self.coord_to_pixels(r,c)
                    if img: self.screen.blit(img,(px,py))
                    else: pygame.draw.circle(self.screen,(255,255,255) if p[0]=='w' else (0,0,0),(px+self.square//2,py+self.square//2),self.square//3)
        if moving_piece and piece_pos:
            self.screen.blit(self.images[moving_piece], piece_pos)
        txt=f"Turn: {'White' if self.turn=='w' else 'Black'}"
        self.screen.blit(self.font.render(txt,True,(255,255,255)),(6,6))
        if AI_ENABLED and self.turn==AI_COLOR:
            ai_txt="AI thinking..." if self.ai_thinking else "AI waiting..."
            self.screen.blit(self.font.render(ai_txt,True,(255,200,100)),(6,26))

    def handle_click(self,pos):
        if AI_ENABLED and self.turn==AI_COLOR: return
        r,c=self.pixels_to_coord(*pos)
        piece=self.board.piece_at(r,c)
        if self.selected:
            if (r,c) in self.legal_moves:
                sr,sc=self.selected
                with self.lock:
                    self.animate_move(sr,sc,r,c,self.board.piece_at(sr,sc))
                    self.board.push_move(sr,sc,r,c)
                    self.turn='b' if self.turn=='w' else 'w'
            self.selected=None
            self.legal_moves=[]
            if piece and piece[0]==self.turn:
                self.selected=(r,c)
                self.legal_moves=[m for m in self.board.generate_moves(r,c) if not self._capture_own(m)]
        else:
            if piece and piece[0]==self.turn:
                self.selected=(r,c)
                self.legal_moves=[m for m in self.board.generate_moves(r,c) if not self._capture_own(m)]

    def _capture_own(self,target):
        tr,tc=target
        p=self.board.piece_at(tr,tc)
        return p is not None and p[0]==self.turn

    # --- AI / Evaluation ---
    def evaluate(self):
        total=0
        for r in range(8):
            for c in range(8):
                p=self.board.piece_at(r,c)
                if p:
                    val=PIECE_VALUES.get(p[1],0)
                    total+=val if p[0]==AI_COLOR else -val
        return total

    def minimax(self,depth,maximizing,alpha,beta):
        if depth==0: return self.evaluate()
        player=AI_COLOR if maximizing else ('w' if AI_COLOR=='b' else 'b')
        moves=self.board.all_color_moves(player)
        if not moves: return self.evaluate()
        if maximizing:
            max_eval=-math.inf
            for sr,sc,tr,tc in moves:
                captured,promoted,piece=self.board.push_move(sr,sc,tr,tc)
                val=self.minimax(depth-1,False,alpha,beta)
                self.board.undo_move(sr,sc,tr,tc,captured,promoted,piece)
                max_eval=max(max_eval,val)
                alpha=max(alpha,val)
                if beta<=alpha: break
            return max_eval
        else:
            min_eval=math.inf
            for sr,sc,tr,tc in moves:
                captured,promoted,piece=self.board.push_move(sr,sc,tr,tc)
                val=self.minimax(depth-1,True,alpha,beta)
                self.board.undo_move(sr,sc,tr,tc,captured,promoted,piece)
                min_eval=min(min_eval,val)
                beta=min(beta,val)
                if beta<=alpha: break
            return min_eval

    def _compute_ai_move(self):
        best_val=-math.inf
        best_moves=[]
        moves=self.board.all_color_moves(AI_COLOR)
        if not moves: return None
        random.shuffle(moves)
        for sr,sc,tr,tc in moves:
            captured,promoted,piece=self.board.push_move(sr,sc,tr,tc)
            val=self.minimax(AI_DEPTH-1,False,-math.inf,math.inf)
            self.board.undo_move(sr,sc,tr,tc,captured,promoted,piece)
            if val>best_val: best_val=val; best_moves=[(sr,sc,tr,tc)]
            elif val==best_val: best_moves.append((sr,sc,tr,tc))
        if not best_moves: return None
        return random.choice(best_moves)

    # --- Move Animation ---
    def animate_move(self,sr,sc,tr,tc,piece,steps=6):
        start_x,start_y=self.coord_to_pixels(sr,sc)
        end_x,end_y=self.coord_to_pixels(tr,tc)
        for step in range(1,steps+1):
            interp_x=start_x+(end_x-start_x)*step/steps
            interp_y=start_y+(end_y-start_y)*step/steps
            self.draw(moving_piece=piece,piece_pos=(interp_x,interp_y))
            pygame.display.flip()
            self.clock.tick(FPS)

    def _delayed_ai_move(self):
        try:
            time.sleep(AI_MOVE_DELAY)
            with self.lock:
                move=self._compute_ai_move()
                if move:
                    sr,sc,tr,tc=move
                    piece=self.board.piece_at(sr,sc)
                    self.animate_move(sr,sc,tr,tc,piece)
                    self.board.push_move(sr,sc,tr,tc)
                    self.turn='b' if self.turn=='w' else 'w'
        finally:
            self.ai_thinking=False
            self.ai_thread=None

    def schedule_ai_move(self):
        if self.ai_thread: return
        self.ai_thinking=True
        self.ai_thread=threading.Thread(target=self._delayed_ai_move,daemon=True)
        self.ai_thread.start()

    # --- Main Loop ---
    def run(self):
        running=True
        while running:
            self.clock.tick(FPS)
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT: running=False
                elif ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1: self.handle_click(ev.pos)
                elif ev.type==pygame.KEYDOWN and ev.key==pygame.K_r:
                    with self.lock: self.board=Board()
                    self.turn='w'; self.selected=None; self.legal_moves=[]
            if AI_ENABLED and self.turn==AI_COLOR and not self.ai_thinking: self.schedule_ai_move()
            self.draw(); pygame.display.flip()
        pygame.quit(); sys.exit()

if __name__=='__main__':
    Game().run()
