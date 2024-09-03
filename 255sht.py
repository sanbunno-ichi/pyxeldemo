import pyxel

_ass = 0
GWK = [0 for _ass in range(0x100)]	#変数管理
cid			=	0x00		#ID番号
ccond		=	0x01		#状態フラグ
#状態フラグ内訳
F_LIVE			=	0x01		#[bit0]生(1)死(0)
F_ACTIVE		=	0x02		#[bit1]アクティブ
F_HIT			=	0x04		#[bit2]ヒット！(1)無し(0)
F_CRASH			=	0x08		#[bit3]爆発中(1)無し(0)

cxpos		=	0x02		#X座標
cypos		=	0x03		#Y座標
cxspd		=	0x04		#X移動スピード
cyspd		=	0x05		#Y移動スピード
cwait		=	0x06		#待ちカウンタ

#12機×待ちカウンタ×座標
PPOS_MAX = 12*10
PPOS = [0 for _ass in range(PPOS_MAX*2)]
ppos_counter = 0

#	0 1 2 3 4 5 6 7   8 9 a b c d e f
#0	□□□□□□□□　□□□□□□□□
#1	□□□□□□■□　□■□□□□□□
#2	□□□□□□■□　□■□□□□□□
#3	□□□□□□■■　■■□□□□□□
#4	□□■□□□■■　■■□□□■□□
#5	□□■□□■■■　■■■□□■□□
#6	□□■□□■■■　■■■□□■□□
#7	□□■□□■■■　■■■□□■□□
#
#8	□□■□■■■■　■■■■□■□□
#9	□□■□■■■■　■■■■□■□□
#a	□□■■■■■■　■■■■■■□□
#b	□□■■■■■■　■■■■■■□□
#c	□■■■■■■■　■■■■■■■□
#d	■■■□■■■■　■■■■□■■■
#e	■■□□■■□□　□□■■□□■■
#f	□□□□■■□□　□□■■□□□□

plyer_tbl = [0 for tbl in range(0xf6)]
plyer_tbl = [
	0x61, 0x4, 0x91, 0x4, 0x62, 0x3, 0x92, 0x3,		#0x00
	0x63, 0x3, 0x73, 0xf, 0x83, 0xf, 0x93, 0x3,		#
	0x24, 0x4, 0x64, 0xf, 0x74, 0x1, 0x84, 0x2,		#0x10
	0x94, 0xf, 0xd4, 0x4, 0x25, 0x3, 0x55, 0xa,		#
	0x65, 0xd, 0x75, 0x1, 0x85, 0x2, 0x95, 0xd,		#0x20
	0xa5, 0xa, 0xd5, 0x3, 0x26, 0x3, 0x56, 0xa,		#
	0x66, 0xd, 0x76, 0xd, 0x86, 0xd, 0x96, 0xd,		#0x30
	0xa6, 0xa, 0xd6, 0x3, 0x27, 0xf, 0x57, 0xa,		#
	0x67, 0xc, 0x77, 0xd, 0x87, 0xd, 0x97, 0xc,		#0x40
	0xa7, 0xa, 0xd7, 0xf, 0x28, 0xf, 0x48, 0xb,		#
	0x58, 0xa, 0x68, 0xf, 0x78, 0xc, 0x88, 0xc,		#0x50
	0x98, 0xf, 0xa8, 0xa, 0xb8, 0xb, 0xd8, 0xf,		#
	0x29, 0xf, 0x49, 0xb, 0x59, 0xa, 0x69, 0xf,		#0x60
	0x79, 0xa, 0x89, 0xa, 0x99, 0xf, 0xa9, 0xa,		#
	0xb9, 0xb, 0xd9, 0xf, 0x2a, 0xf, 0x3a, 0xe,		#0x70
	0x4a, 0xb, 0x5a, 0xa, 0x6a, 0xf, 0x7a, 0x9,		#

	0x8a, 0xe, 0x9a, 0xf, 0xaa, 0xa, 0xba, 0xb,		#0x80
	0xca, 0xe, 0xda, 0xf, 0x2b, 0xe, 0x3b, 0xe,		#
	0x4b, 0xb, 0x5b, 0xa, 0x6b, 0xf, 0x7b, 0x9,		#0x90
	0x8b, 0xe, 0x9b, 0xf, 0xab, 0xa, 0xbb, 0xb,		#
	0xcb, 0xe, 0xdb, 0xe, 0x1c, 0xe, 0x2c, 0xe,		#0xa0
	0x3c, 0xe, 0x4c, 0xb, 0x5c, 0xa, 0x6c, 0xf,		#
	0x7c, 0x9, 0x8c, 0xe, 0x9c, 0xf, 0xac, 0xa,		#0xb0
	0xbc, 0xb, 0xcc, 0xe, 0xdc, 0xe, 0xec, 0xe,		#
	0x0d, 0xe, 0x1d, 0xe, 0x2d, 0xe, 0x4d, 0x8,		#0xc0
	0x5d, 0x8, 0x6d, 0x7, 0x7d, 0x9, 0x8d, 0xe,		#
	0x9d, 0x7, 0xad, 0x8, 0xbd, 0x8, 0xdd, 0xe,		#0xd0
	0xed, 0xe, 0xfd, 0xe, 0x0e, 0xe, 0x1e, 0xe,		#
	0x4e, 0x5, 0x5e, 0x5, 0xae, 0x5, 0xbe, 0x5,		#0xe0
	0xee, 0xe, 0xfe, 0xe, 0x4f, 0x6, 0x5f, 0x6,		#
	0xaf, 0x6, 0xbf, 0x6, 0xff, 0xff				#0xf0
	]

def dot_pattern( dx, dy, tp):
	adr = plyer_tbl

	_cnt = 0
	while (adr[_cnt*2+0] != 0xff):
		_xp = pyxel.floor( adr[_cnt*2+0]/0x10 )
		_yp = pyxel.floor( adr[_cnt*2+0]&0x0f )
		_col = adr[_cnt*2+1] + (tp+1) * 0x10
		pyxel.pset( dx + _xp, dy + _yp, _col )
		_cnt+=1

def update():
	global ppos_counter

	_wk = 0
	if( GWK[_wk+ccond] & F_LIVE ):
		if getInputLEFT():
			GWK[_wk+cxpos] -= GWK[_wk+cxspd]
		if getInputRIGHT():
			GWK[_wk+cxpos] += GWK[_wk+cxspd]
		if getInputUP():
			GWK[_wk+cypos] -= GWK[_wk+cyspd]
		if getInputDOWN():
			GWK[_wk+cypos] += GWK[_wk+cyspd]
		
		#座標を記憶
		PPOS[ppos_counter*2+0] = GWK[_wk+cxpos]
		PPOS[ppos_counter*2+1] = GWK[_wk+cypos]
		ppos_counter+=1
		if(ppos_counter >= PPOS_MAX):
			ppos_counter-=PPOS_MAX

	for _cnt in range(1,12):
		_wk = _cnt * 0x10
		if( GWK[_wk+ccond] & F_LIVE ):
			_pcnt = ppos_counter - (GWK[_wk+cid]*7)
			if(_pcnt < 0):
				_pcnt+=PPOS_MAX
			GWK[_wk+cxpos] = PPOS[_pcnt*2+0]
			GWK[_wk+cypos] = PPOS[_pcnt*2+1]
		else:
			GWK[_wk+cwait]-=1
			if(GWK[_wk+cwait]<0):
				GWK[_wk+ccond] |= F_LIVE

def draw():
	pyxel.cls(0)

	for _cnt in range(10, 0, -1):
		_wk = _cnt * 0x10
		if(GWK[_wk+ccond] & F_LIVE):
			dot_pattern(GWK[_wk+cxpos], GWK[_wk+cypos], GWK[_wk+cid]+1)
	#本体を最後に描画
	_wk = 0
	dot_pattern(GWK[_wk+cxpos], GWK[_wk+cypos], GWK[_wk+cid]+1)


#-----------------------------------------------------------------
#入力（キーボード＆ジョイパッド）
#-----------------------------------------------------------------
#上
def getInputUP():
	if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
		return 1
	else:
		return 0
#下
def getInputDOWN():
	if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
		return 1
	else:
		return 0
#左
def getInputLEFT():
	if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
		return 1
	else:
		return 0
#右
def getInputRIGHT():
	if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
		return 1
	else:
		return 0
#==============================================================================================================
pyxel.init(120, 160, fps=60)
pyxel.load("255sht.pyxres")
#work clear
for _cnt in range( 0, 0x100 ):
	GWK[_cnt] = 0
#init
for _cnt in range( 0, 12 ):
	_wk = _cnt * 0x10
	GWK[_wk + cid] = _cnt
	GWK[_wk + ccond] = 0
	GWK[_wk + cxpos] = 60
	GWK[_wk + cypos] = 80
	GWK[_wk + cxspd] = 2
	GWK[_wk + cyspd] = 2
	GWK[_wk + cwait] = _cnt * 10
#最初の一機のみ最初に出す
GWK[ccond] = F_LIVE
pyxel.run(update, draw)
