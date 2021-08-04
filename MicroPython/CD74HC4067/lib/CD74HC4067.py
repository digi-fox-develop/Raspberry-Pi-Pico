import machine

mux_channel = (
	# s0, s1, s2, s3     channel
	[0,  0,  0,  0], # 0
	[1,  0,  0,  0], # 1
	[0,  1,  0,  0], # 2
	[1,  1,  0,  0], # 3
	[0,  0,  1,  0], # 4
	[1,  0,  1,  0], # 5
	[0,  1,  1,  0], # 6
	[1,  1,  1,  0], # 7
	[0,  0,  0,  1], # 8
	[1,  0,  0,  1], # 9
	[0,  1,  0,  1], # 10
	[1,  1,  0,  1], # 11
	[0,  0,  1,  1], # 12
	[1,  0,  1,  1], # 13
	[0,  1,  1,  1], # 14
	[1,  1,  1,  1]  # 15
	)


class CD74HC4067:
	def __init__(self, s0, s1, s2, s3, sig):
		self.s0 = s0
		self.s1 = s1
		self.s2 = s2
		self.s3 = s3
		self.sig = sig
		self.Pin_Out = []
		self.Pin_Out.append(machine.Pin(self.s0, machine.Pin.OUT))
		self.Pin_Out.append(machine.Pin(self.s1, machine.Pin.OUT))
		self.Pin_Out.append(machine.Pin(self.s2, machine.Pin.OUT))
		self.Pin_Out.append(machine.Pin(self.s3, machine.Pin.OUT))
		self.Pin_sig=machine.Pin(self.sig, machine.Pin.IN)
		for k in range(4):
			self.Pin_Out[k].value(0)

	def read(self, channel):
		self.channel = channel
		self.muxChannel = mux_channel
		for i in range(4):
			self.Pin_Out[i].value(self.muxChannel[self.channel][i])
		return self.Pin_sig.value()

class CD74HC4067_DUAL:
	def __init__(self, s0, s1, s2, s3, sig1,sig2):
		self.s0 = s0
		self.s1 = s1
		self.s2 = s2
		self.s3 = s3
		self.sig1 = sig1
		self.sig2 = sig2
		self.Pin_Out = []
		self.Pin_Out.append(machine.Pin(self.s0, machine.Pin.OUT))
		self.Pin_Out.append(machine.Pin(self.s1, machine.Pin.OUT))
		self.Pin_Out.append(machine.Pin(self.s2, machine.Pin.OUT))
		self.Pin_Out.append(machine.Pin(self.s3, machine.Pin.OUT))
		self.Pin_sig1=machine.Pin(self.sig1, machine.Pin.IN)
		self.Pin_sig2=machine.Pin(self.sig2, machine.Pin.IN)
		for k in range(4):
			self.Pin_Out[k].value(0)

	def read(self, channel):
		self.channel = channel
		self.muxChannel = mux_channel
		for i in range(4):
			self.Pin_Out[i].value(self.muxChannel[self.channel][i])
		return [self.Pin_sig1.value(), self.Pin_sig2.value()]
