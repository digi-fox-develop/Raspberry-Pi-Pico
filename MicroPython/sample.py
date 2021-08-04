from machine import Pin, SPI
from time import sleep
from utime import sleep_ms

# lib
import YMF825
import YMF825_TONE

# SPI setting : Use 0 line.
mosi_0 = Pin(19)
miso_0 = Pin(16)
sck_0  = Pin(18)
spi_0  = SPI(0, baudrate=(10 * 1000 * 1000),
				polarity=0,
				phase=0,
				bits=8,
				firstbit=SPI.MSB,
				sck=sck_0,
				mosi=mosi_0,
				miso=miso_0)

# SS pin for 1st module
sdm1_ss = Pin(17)

# create 1st module object
sdm1 = YMF825.SOUND_MDL(spi_0, sdm1_ss)

# tone setting
use_tone=(
			YMF825_TONE.GRANDPIANO,
			YMF825_TONE.E_PIANO,
			YMF825_TONE.TENORSAX,
			YMF825_TONE.PICKBASS,
			YMF825_TONE.TNKLBELL,
			YMF825_TONE.NEWAGEPD,
			YMF825_TONE.BRIGHTPIANO,
			YMF825_TONE.VIBES,
			YMF825_TONE.CHURCHORGAN,
			YMF825_TONE.FLUTE,
			YMF825_TONE.ROCKORGAN,
			YMF825_TONE.NYLONGUITER,
			YMF825_TONE.SQUARELEAD,
			YMF825_TONE.SAWLEAD,
			YMF825_TONE.HARPSICHORD,
			YMF825_TONE.HARMONICA,
			)
tone_data = []
for num in use_tone:
	tone_data += YMF825_TONE.tone_data[num]

# write tone data
sdm1.set_tone(tone_data)

# write ch setting
for i in range(16):
	sdm1.set_ch(1)

# sound it
for SET_TONE in range(16):
	# ch , tone_data num
	ch1=[0, SET_TONE] 
	ch2=[1, SET_TONE] 
	ch3=[2, SET_TONE] 

	sdm1.keyon(ch1, 0x14,0x65)
	sleep_ms(500)
	sdm1.keyoff(ch1)
	print(sdm1.read_ch(0x00))

	sdm1.keyon(ch1, 0x1C,0x42)
	sleep_ms(500)
	sdm1.keyoff(ch1)
	print(sdm1.read_ch(0x00))

	sdm1.keyon(ch1, 0x24,0x17)
	sleep_ms(500)
	sdm1.keyoff(ch1)
	print(sdm1.read_ch(0x00))

	sleep(1)

	sdm1.keyon(ch1, 0x14,0x65)
	sleep_ms(700)
	sdm1.keyon(ch2, 0x1C,0x42)
	sleep_ms(700)
	sdm1.keyon(ch3, 0x24,0x17)
	sleep_ms(700)

	sdm1.keyoff(ch3)
	sleep_ms(700)
	sdm1.keyoff(ch2)
	sleep_ms(700)
	sdm1.keyoff(ch1)

	sleep(2)


