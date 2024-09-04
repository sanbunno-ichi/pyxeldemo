#https://note.com/pro_gramma/n/ned6a8d08d8c9
#正方形を並べて回転

#これを応用して、拡大＆回転させればいいのでは？あ
import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

WK_MAX = 20
id		= 0
cond	= 1

F_LIVE	= 0x01
F_ACT	= 0x02
F_WAIT	= 0x04

xp		= 2
yp		= 3
xspd	= 4
yspd	= 5
rp		= 6
wcnt	= 7

OFS_MAX	= 8
GWK = [[0 for i in range(OFS_MAX)] for j in range(WK_MAX)]

IMAGE_1 = [0, 0, 0, 15, 15, 0]  # image_bank, u, v, w, h, transparent_color

def update():
	for j in range(WK_MAX):
		if( GWK[j][cond] & F_LIVE ):
			GWK[j][rp] += 1
			#GWK[j][yp] = int(SCREEN_HEIGHT/2) + pyxel.sin(GWK[j][rp] * 100)
			if( GWK[j][rp] > 360 ):
				GWK[j][cond] = GWK[j][cond] & ~F_LIVE
				GWK[j][cond] = GWK[j][cond] | F_WAIT
				GWK[j][wcnt] = 20
				GWK[j][rp] = 0
				GWK[j][xp] = int(SCREEN_WIDTH/2)
				GWK[j][yp] = int(SCREEN_HEIGHT/2)
				
		elif( GWK[j][cond] & F_WAIT ):
			GWK[j][wcnt] -= 1
			if( GWK[j][wcnt] < 0 ):
				GWK[j][wcnt] = 0
				GWK[j][cond] = GWK[j][cond] & ~F_WAIT
				GWK[j][cond] = GWK[j][cond] | F_LIVE
#	if pyxel.btnp(pyxel.KEY_Q):
#		pyxel.quit()

def draw():
	pyxel.cls(6)       
	for j in range(WK_MAX):
		if( GWK[j][cond] & F_LIVE ):
			#_col = pyxel.rndi(1,15)

			_rotate = GWK[j][rp]
			_scale = GWK[j][rp] * 0.1
			pyxel.blt(GWK[j][xp], GWK[j][yp], *IMAGE_1, rotate=_rotate, scale=_scale)


pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT, title="rotating square")
image_bank = 0
# イメージバンクに正方形を書き込む
pyxel.images[image_bank].rectb(0, 0, 15, 15, 1)

#work clear
i = 0
for j in range(WK_MAX):
	GWK[j][id] = i
	GWK[j][cond] = F_WAIT
	GWK[j][xp] = int(SCREEN_WIDTH/2)
	GWK[j][yp] = int(SCREEN_HEIGHT/2)
	GWK[j][xspd] = 0
	GWK[j][yspd] = 0
	GWK[j][rp] = 0
	GWK[j][wcnt] = i * 20
	i += 1

pyxel.run(update, draw)
