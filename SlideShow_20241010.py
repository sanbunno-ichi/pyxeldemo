from PIL import Image
import numpy as np
import pyxel
import os
#----------------------------------------------------
#pyxapp化には注意が必要
#最初からimgフォルダと画像を用意してpyxapp内に取り込んでおかないと
#SlideShowは実行できない
#つまりはパレットファイル生成するのはローカルメモリ内だけなので
#外部ファイルとしては出力しない、かつ、アプリ外のフォルダ参照もできない
#html化するとさらにPILライブラリが無いといわれる・・・
#.pyファイルのみで遊ぶくらいしかできないというわけ・・・
#
#意外とこのへんめんどくさい
#----------------------------------------------------
#★前準備：
#あらかじめ「pyxel edit」を実行してエディタを起動＆保存して
#空のファイル：my_resource.pyxresを作成しておく
#（255色カラーパレットファイル作成用）
#★前準備２
#画像ファイルは、imgフォルダに格納してください
#★表示サイズや読み込みフォルダを変更したいときは下記のコードを変更してください
#※表示できないファイルはコンソールにエラー内容表示してとばします
#----------------------------------------------------
#Pillow対応画像形式（ただし必ず表示できるわけではない）
#参考：https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html
#[Full Support]
#	BLP, BMP, DDS, DIB, EPS, GIF, ICNS, ICO, IM, JPEG, JPEG2000, MSP, 
#	PCX, PFM, PNG, APNG, PPM, SGI, SPIDER, TGA, TIFF, WebP, XBM, 
#[Read-only]
#	CUR, DCX, FITS, FLI, FLC, FPX, FTEX, GBR, GD, IMT, IPTC/NAA, 
#	MCIDAS, MIC, MPO, PCD, PIXAR, PSD, QOI, SUN, WAL, WMF, EMF, XPM
#[Write-only]
#	PALM, PDF, XV Thumbnails
#[Identify-only]
#	BUFR, GRIB, HDF5, MPEG
#----------------------------------------------------
#表示画像サイズ
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
#画像フォルダ指定
_folder_path = './img'
#----------------------------------------------------
#画像表示
def disp_image(filename):
	try:
		im = Image.open(filename)
		#print(im.format, im.size, im.mode)
	except ValueError as e:
		disp_error(filename + ": Image.open ERROR[ValueError]")
		print(e)
		return
	except OSError as e:
		disp_error(filename + ": Image.open ERROR[OSError]")
		print(e)
		return
	except PIL.UnidentifiedImageError as e:
		disp_error(filename + ": Image.open ERROR[PIL.UnidentifiedImageError]")
		print(e)
		return
	except:
		disp_error(filename + ": Image.open ERROR[Other Error]")
		return
#----------------------------------------------------
#RGBAモードを変換したい
	if( im.mode == "RGBA" ):
		try:
			im = im.convert('RGB')
		except ValueError as e:
			disp_error(filename + ": convert RGB ERROR[ValueError]")
			print(e)
		except OSError as e:
			disp_error(filename + ": convert RGB ERROR[OSError]" )
			print(e)
		except:
			disp_error(filename + ": RGB convert ERROR")
			return

#----------------------------------------------------
#画像サイズ変更
	try:
		#im.resizeの引数に( SCREEN_WIDTH, SCREEN_HEIGHT )を渡すため二重かっこになるようだ
		resize_im = im.resize(( SCREEN_WIDTH, SCREEN_HEIGHT ))
	except ValueError as e:
		disp_error(filename + ": resize ERROR[ValueError]")
		print(e)
		return
	except OSError as e:
		disp_error(filename + ": resize ERROR[OSError]" )
		print(e)
		return
	except:
		disp_error(filename + ": resize ERROR[Other Error]")
		return

#----------------------------------------------------
#減色
	try:
		im_q = resize_im.quantize(colors=255, method=0, kmeans=100, dither=1)
	except ValueError as e:
		disp_error(filename + ": resize_im.quantize ERROR[ValueError]")
		peint(e)
		return
	except OSError as e:
		disp_error(filename + ": resize_im.quantize ERROR[OSError]")
		peint(e)
		return
	except:
		disp_error(filename + ": resize_im.quantize ERROR[Other Error]")
		return

#----------------------------------------------------
#画像からパレットを取得してRGBの順になるように3つずつのlistに格納する
	_palette = list(zip(*[iter(im_q.getpalette())]*3))
#----------------------------------------------------
#画像データ抽出して表示
	_pix = np.asarray(im_q)
	with open('./my_resource.pyxpal', mode='w') as f:
		for _col in range(len(_palette)):
			f.write( hex(_palette[_col][0]*0x10000 + _palette[_col][1]*0x100 + _palette[_col][2]).removeprefix('0x')+'\n' )
#255色カラーデータを読み込むためリソース読み込み
	pyxel.load("my_resource.pyxres")
	#print( "disp_image: ",filename )
#画面クリア
	pyxel.cls(0)
#描画
	_scrptr = pyxel.screen.data_ptr()
	for _yp in range(SCREEN_HEIGHT):
		_s = _yp * SCREEN_WIDTH
		_e = _s + SCREEN_WIDTH
		_scrptr[ _s : _e ] = _pix[_yp]
#キー入力待ち

#----------------------------------
def disp_error(_str):
	global _flag
	#エラー画像はとばす
	_flag = 2
	print(_str)
#----------------------------------------------------
#左クリックで次の画像へ、右クリックで終了
_flag = 0
_count = 0
_piclist =[]

def update():
	global _flag
	global _count
	global _piclist

	if( _flag == 1 ):
		if( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
			_flag = 0
			_count = _count + 1
			if( _count >= len( _piclist ) ):
				_count = 0
		elif( pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) ):
			pyxel.quit()
	#Error発生時はすぐに次へ
	elif( _flag == 2 ):
		_flag = 0
		_count = _count + 1
		if( _count >= len( _piclist ) ):
			_count = 0

#----------------------------------
def draw():
	global _flag
	global _count
	global _piclist

	if( _flag == 0 ):
		_flag = 1
		disp_image( _folder_path + '/' + _piclist[_count].rstrip() )
#----------------------------------------------------
pyxel.init( SCREEN_WIDTH, SCREEN_HEIGHT )

try:
	_piclist = os.listdir(_folder_path)
except FileNotFoundError:
	print("イメージフォルダ",_folder_path,"が無いので終了")
	pyxel.quit()
except:
	pyxel.quit()

#初期化
_flag = 0
_count = 0
#実行
pyxel.run(update, draw)
