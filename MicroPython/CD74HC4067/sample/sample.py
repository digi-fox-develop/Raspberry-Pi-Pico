from machine import Pin
import time
import cd74hc4067 as mux

# マルチプレクサ単体のCh数
mux_ch_num = 16

# 鍵盤数
mux_ch_totalNum = 32

# マルチプレクサのピン設定
mux_s0 = 10
mux_s1 = 11
mux_s2 = 12
mux_s3 = 13
mux1_sig1 = 14
mux2_sig2 = 15  
mux_1 = mux.CD74HC4067_DUAL( mux_s0, mux_s1, mux_s2, mux_s3, mux1_sig1, mux2_sig2)

# マルチプレクサの戻り値を1（HIGH）で初期化
mux = [1 for x in range(mux_ch_totalNum)]

# ループ
while True:
	# マルチプレクサ読み取り
	for j in range(mux_ch_num):
		mux_1_res = mux_1.read(j)
		mux[j] = mux_1_res[0]
		mux[j+mux_ch_num] = mux_1_res[1]
	
	print(mux)
	time.sleep_ms(20)
	