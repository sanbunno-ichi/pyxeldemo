import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

water = [0 for tbl in range(2)]
water[0] = [0 for tbl in range(SCREEN_WIDTH)]
water[1] = [0 for tbl in range(SCREEN_WIDTH)]

gameCtr = 0;
tt = 0;
nt = 0;

def water_init():
	for loop1 in range(2):
		for loop2 in range(SCREEN_WIDTH):
			water[loop1][loop2] = [0 for tbl in range(SCREEN_HEIGHT)]

	for loop1 in range(2):
		for loop2 in range(SCREEN_WIDTH):
			for loop3 in range(SCREEN_HEIGHT):
				water[loop1][loop2][loop3] = 0

#===============================================================================
#描画（demo:taku_disp()）
#===============================================================================
def draw():
	global water
	global gameCtr
	global tt
	global nt

	x = 0;
	y = 0;
	py = 0;
	depth = 0;
	len = 0;
	dy = 0;


	#画面クリア
	pyxel.cls(0)

	#マウス位置を取得
	msxp = pyxel.mouse_x
	msyp = pyxel.mouse_y

	tt = gameCtr & 1
	nt = tt ^ 1			#水面テーブルのインデックスは交互に使う
	
	x = int(int( msxp ) % SCREEN_WIDTH)
	y = int((SCREEN_HEIGHT - int( msyp ))%SCREEN_HEIGHT)

	#水滴を落とす位置（マウスポインタの位置）
	water[tt][ x ][ y ] = 512
	
	#水面の計算
	for y in range(1, SCREEN_HEIGHT-1):
		for x in range(1, SCREEN_WIDTH-1):
			depth  = water[tt][x-1][y  ]		#今回の水面の四方を足す
			depth += water[tt][x+1][y  ]
			depth += water[tt][x  ][y-1]
			depth += water[tt][x  ][y+1]
			depth  = int( depth / 2 )			#÷２

			depth -= water[nt][x][y]			#前回の水面の中央を引く
			depth -= int( depth / 32 )			#÷１６（割る数が大きいほど持続）
			water[nt][x][y] = depth				#次回の水面に結果を代入

	#水面を描画する
	for x in range( 0, SCREEN_WIDTH - 1 ):
		py = SCREEN_HEIGHT - 1						#下から描画する
		dy = 7										#１ドットは１／８単位
		for y in range( 1, SCREEN_HEIGHT - 1 ):		#縦方向に処理していく
			dy -= 8
			depth = water[nt][x][y]
			if( depth > dy ):						#最大－最小法で陰線消去する
				len = depth - dy					#というよりも最大のみを使用する
				dy = depth | 7

				_col = int( ( SCREEN_HEIGHT / 2 ) - 1 ) - y + ( SCREEN_HEIGHT / 2 )
				_col = int( ( _col * 238 ) / SCREEN_HEIGHT ) + 16

				while( True ):
					pyxel.pset( x, py, _col )
					py -= 1
					if( len <= 8 ):
						break
					else:
						len -= 8
	gameCtr += 1
	
#===============================================================================
#更新（main loop）
#===============================================================================
def update():
	pass
#-----------------------------------------------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)

#マウスカーソル表示
pyxel.mouse(visible = True)

#パレットロード（デフォルト16色＋グレー239色）
pyxel.load("water.pyxres")

#初期化
water_init()

pyxel.run(update, draw)
