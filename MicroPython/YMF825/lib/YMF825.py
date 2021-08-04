from micropython import const
from machine     import SPI
from utime       import sleep_ms,sleep_us
from struct      import unpack
import ubinascii

# command address
ADR_CLOCK_ENABLE                 = const(0x00)
ADR_RESET                        = const(0x01)
ADR_ANLG_BLK_PW_DWN_CTRL         = const(0x02)
ADR_SPEAKER_AMPLIFIER_GAIN       = const(0x03)
ADR_HARDWARE_ID                  = const(0x04)
ADR_INTERRUPT1                   = const(0x05)
ADR_INTERRUPT2                   = const(0x06)
ADR_CONTENTS_DATA_WRT_PORT       = const(0x07)
ADR_SQCR1                        = const(0x08)
ADR_SQCR2                        = const(0x09)
ADR_SQCR3                        = const(0x0A)
ADR_SYNTHESIZER1                 = const(0x0B)
ADR_SYNTHESIZER2                 = const(0x0C)
ADR_SYNTHESIZER3                 = const(0x0D)
ADR_SYNTHESIZER4                 = const(0x0E)
ADR_SYNTHESIZER5                 = const(0x0F)
ADR_SYNTHESIZER6                 = const(0x10)
ADR_SYNTHESIZER7                 = const(0x11)
ADR_SYNTHESIZER8                 = const(0x12)
ADR_SYNTHESIZER9                 = const(0x13)
ADR_SYNTHESIZER10                = const(0x14)
ADR_CTRL_REG_RD_PORT1            = const(0x15)
ADR_CTRL_REG_RD_PORT2            = const(0x16)
ADR_SQCR_TIME_UNIT1              = const(0x17)
ADR_SQCR_TIME_UNIT2              = const(0x18)
ADR_MASTER_VOLUME                = const(0x19)
ADR_SOFT_RESET                   = const(0x1A)
ADR_SQCR_D_R_V                   = const(0x1B)
ADR_LFO_RESET                    = const(0x1C)
ADR_RW_RAIL_SELECTION            = const(0x1D)
ADR_RESERVED1                    = const(0x1E)
ADR_RESERVED2                    = const(0x1F)
ADR_EQ_BAND0_CEC_WRT_PORT        = const(0x20)
ADR_EQ_BAND1_CEC_WRT_PORT        = const(0x21)
ADR_EQ_BAND2_CEC_WRT_PORT        = const(0x22)
ADR_EQLZ_CEC_RD_PORTS1           = const(0x23)
ADR_EQLZ_CEC_RD_PORTS2           = const(0x24)
ADR_EQLZ_CEC_RD_PORTS3           = const(0x25)
ADR_EQLZ_CEC_RD_PORTS4           = const(0x26)
ADR_EQLZ_CEC_RD_PORTS5           = const(0x27)
ADR_EQLZ_CEC_RD_PORTS6           = const(0x28)
ADR_EQLZ_CEC_RD_PORTS7           = const(0x29)
ADR_EQLZ_CEC_RD_PORTS8           = const(0x2A)
ADR_EQLZ_CEC_RD_PORTS9           = const(0x2B)
ADR_EQLZ_CEC_RD_PORTS10          = const(0x2C)
ADR_EQLZ_CEC_RD_PORTS11          = const(0x2D)
ADR_EQLZ_CEC_RD_PORTS12          = const(0x2E)
ADR_EQLZ_CEC_RD_PORTS13          = const(0x2F)
ADR_EQLZ_CEC_RD_PORTS14          = const(0x30)
ADR_EQLZ_CEC_RD_PORTS15          = const(0x31)
ADR_EQLZ_CEC_RD_PORTS16          = const(0x32)
ADR_EQLZ_CEC_RD_PORTS17          = const(0x33)
ADR_EQLZ_CEC_RD_PORTS18          = const(0x34)
ADR_EQLZ_CEC_RD_PORTS19          = const(0x35)
ADR_EQLZ_CEC_RD_PORTS20          = const(0x36)
ADR_EQLZ_CEC_RD_PORTS21          = const(0x37)
ADR_EQLZ_CEC_RD_PORTS22          = const(0x38)
ADR_EQLZ_CEC_RD_PORTS23          = const(0x39)
ADR_EQLZ_CEC_RD_PORTS24          = const(0x3A)
ADR_EQLZ_CEC_RD_PORTS25          = const(0x3B)
ADR_EQLZ_CEC_RD_PORTS26          = const(0x3C)
ADR_EQLZ_CEC_RD_PORTS27          = const(0x3D)
ADR_EQLZ_CEC_RD_PORTS28          = const(0x3E)
ADR_EQLZ_CEC_RD_PORTS29          = const(0x3F)
ADR_EQLZ_CEC_RD_PORTS30          = const(0x40)
ADR_EQLZ_CEC_RD_PORTS31          = const(0x41)
ADR_EQLZ_CEC_RD_PORTS32          = const(0x42)
ADR_EQLZ_CEC_RD_PORTS33          = const(0x43)
ADR_EQLZ_CEC_RD_PORTS34          = const(0x44)
ADR_EQLZ_CEC_RD_PORTS35          = const(0x45)
ADR_EQLZ_CEC_RD_PORTS36          = const(0x46)
ADR_EQLZ_CEC_RD_PORTS37          = const(0x47)
ADR_EQLZ_CEC_RD_PORTS38          = const(0x48)
ADR_EQLZ_CEC_RD_PORTS39          = const(0x49)
ADR_EQLZ_CEC_RD_PORTS40          = const(0x4A)
ADR_EQLZ_CEC_RD_PORTS41          = const(0x4B)
ADR_EQLZ_CEC_RD_PORTS42          = const(0x4C)
ADR_EQLZ_CEC_RD_PORTS43          = const(0x4D)
ADR_EQLZ_CEC_RD_PORTS44          = const(0x4E)
ADR_EQLZ_CEC_RD_PORTS45          = const(0x4F)
ADR_SOFTWARE_TEST_COMMUNICATION  = const(0x50)

class YMF825:
	def __init__(self, spi, ss, external_vcc= 0x01):
		self.spi = spi
		ss.init(ss.OUT)
		self.ss = ss
		# Set DRV_SEL to "0" when this device is used in single 5-V power supply configuration. 
		self.write( ADR_RW_RAIL_SELECTION, external_vcc)
		# Set the AP0 to "0". The VREF is powered.
		self.write( ADR_RW_RAIL_SELECTION, 0x00)
		# Wait until the clock becomes stable.
		self.write( ADR_ANLG_BLK_PW_DWN_CTRL, 0x0E )   #AP1,AP2,AP3
		# Set the CLKE to "1".
		self.write( ADR_CLOCK_ENABLE, 0x01 )           #CLKEN
		# Set the ALRST to "0".
		self.write( ADR_RESET, 0x00 )                  #AKRST
		# Set the SFTRST to "A3H".
		self.write( ADR_SOFT_RESET, 0xA3 )
		# Set the SFTRST to "00H".
		self.write( ADR_SOFT_RESET, 0x00 )
		# Wait for 30ms after the step 10.
		sleep_ms(30)
		# Set the AP1 and the AP3 to "0".
		self.write( ADR_ANLG_BLK_PW_DWN_CTRL, 0x04 )   #AP1,AP3
		# Wait for 10us.
		sleep_us(10)
		# Set the AP2 to "0".
		self.write( ADR_ANLG_BLK_PW_DWN_CTRL, 0x00 )
		sleep_us(10)
		self.write( ADR_MASTER_VOLUME, 0xF0 )          #MASTER VOL
		self.write( ADR_SQCR_D_R_V, 0x3F )             #interpolation
		self.write( ADR_SYNTHESIZER10, 0x00 )          #interpolation
		self.write( ADR_SPEAKER_AMPLIFIER_GAIN, 0x01 ) #Analog Gain
		sleep_us(10)
		self.write( ADR_SQCR1, 0xF6 )
		self.write( ADR_SQCR1, 0x00 )
		self.write( ADR_SQCR2, 0xF8 )
		self.write( ADR_SQCR3, 0x00 )
		sleep_us(10)
		self.write( ADR_SQCR_TIME_UNIT1, 0x40 )        #MS_S
		self.write( ADR_SQCR_TIME_UNIT2, 0x00 )
		super().__init__()
		self.ss(1) #common select off
		
	def write(self, cmd, data):
		data = bytearray([cmd,data])
		self.ss(1)
		self.ss(0)
		self.spi.write(data)
		self.ss(1)
		
	def write_burst(self, cmd, burstData):
		array = bytearray(len(burstData) + 1)
		array[0] = cmd
		for i in range(len(burstData)):
			array[i+1] = burstData[i]
		data = bytearray(array)
		self.ss(1)
		self.ss(0)
		self.spi.write(data)
		self.ss(1)
		
	def read(self, adr):
		data = (0x80 | adr)
		self.ss(1)
		self.ss(0)
		rcv = self.spi.read(2,data)
		self.ss(1)
		return unpack('B',rcv[1:])[0]
		
	def read_ch(self, ch):
		# Return = ch +  #12-#19
		startAdr = ch * 8
		rcv = []
		rcv.append(ch)
		for i in range(startAdr, startAdr + 8):
			self.write(ADR_CTRL_REG_RD_PORT1,i)
			rcv.append(self.read(ADR_CTRL_REG_RD_PORT2))
		return rcv

class SOUND_MDL(YMF825):
	def set_tone(self, toneData):
		data = [128 + (len(toneData) // 30)] + toneData + [0x80,0x03,0x81,0x80]
		self.write( ADR_SQCR1, 0xF6 )
		sleep_us(10)
		self.write( ADR_SQCR1, 0x00 )
		sleep_us(10)
		self.write_burst( ADR_CONTENTS_DATA_WRT_PORT, data )
		
	def set_ch(self, ch):
		self.write( ADR_SYNTHESIZER1, 0x00 | ch)  # ch
		self.write( ADR_SYNTHESIZER5, 0x30 ) # keyon = 0
		self.write( ADR_SYNTHESIZER6, 0x71 ) # chvol
		self.write( ADR_SYNTHESIZER7, 0x00 ) # XVB
		self.write( ADR_SYNTHESIZER8, 0x08 ) # FRAC
		self.write( ADR_SYNTHESIZER9, 0x00 ) # FRAC
		
	def keyon(self, chTone, fnumh, fnuml):
		self.write( ADR_SYNTHESIZER1, 0x00 | chTone[0])  # ch
		self.write( ADR_SYNTHESIZER2, 0x54 )  # vovol
		self.write( ADR_SYNTHESIZER3, fnumh ) # fnum
		self.write( ADR_SYNTHESIZER4, fnuml ) # fnum
		self.write( ADR_SYNTHESIZER5, 0x40 | chTone[1] )  # keyon = 1  & tone_num
		
	def keyoff(self, chTone):
		self.write( ADR_SYNTHESIZER1, 0x00 | chTone[0])  # ch
		self.write( ADR_SYNTHESIZER5, 0x00 | chTone[1] ) # keyon = 0 & tone_num
		
