import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動用辞書(降下キー、移動量) 
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_RIGHT: (+5, 0),
    pg.K_LEFT: (-5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect または爆弾Rectの画面内外判定用の関数
    引数 こうかとんRect または 爆弾Rect
    戻り値 横方向判定結果 縦方向判定結果 (True 画面内 False 画面外)
    """
    yoko, tate = True, True
    if obj_rct.left< 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    print("aioeo")
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # ここからこうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    # ここから爆弾の設定
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 横方向速度, 縦方向速度
    

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾がぶつかったら
            print("Game Over")
            dis_go(screen)  # dis_go関数を呼び出す
            return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動と表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾の移動と表示
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


def dis_go(screen: pg.Surface):
    """
    引数: スクリーン
    泣いているこうかとんの描画
    画面をブラックアウト
    「Game Over」の表示
    5秒後にプログラムを停止させる
    """
    back = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(back, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT)) 
    back.set_alpha(200)  # 背景を投下させる
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)    
    screen.blit(back, [0, 0])
    screen.blit(txt, [650, 450])
    screen.blit(kk2_img, [500, 400])
    screen.blit(kk2_img, [1000, 400])
    pg.display.update()
    time.sleep(5)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

