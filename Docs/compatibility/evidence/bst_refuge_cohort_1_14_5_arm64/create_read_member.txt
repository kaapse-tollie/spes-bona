/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/binaries/victoria3.app/Contents/MacOS/victoria3:
(__TEXT,__text) section
__ZN16CCreatePopEffect10ReadMemberER7CReaderit:
101b5a0f0:	e8 03 01 aa	mov	x8, x1
101b5a0f4:	49 fc 84 52	mov	w9, #0x27e2
101b5a0f8:	5f 00 09 6b	cmp	w2, w9
101b5a0fc:	ad 01 00 54	b.le	0x101b5a130
101b5a100:	69 fc 84 52	mov	w9, #0x27e3
101b5a104:	5f 00 09 6b	cmp	w2, w9
101b5a108:	40 02 00 54	b.eq	0x101b5a150
101b5a10c:	a9 6c 8a 52	mov	w9, #0x5365
101b5a110:	5f 00 09 6b	cmp	w2, w9
101b5a114:	40 02 00 54	b.eq	0x101b5a15c
101b5a118:	49 ba 85 52	mov	w9, #0x2dd2
101b5a11c:	5f 00 09 6b	cmp	w2, w9
101b5a120:	c1 02 00 54	b.ne	0x101b5a178
101b5a124:	01 00 01 91	add	x1, x0, #0x40
101b5a128:	e0 03 08 aa	mov	x0, x8
101b5a12c:	43 59 ec 17	b	__ZN7CReader4ReadI8CPopTypeEEvRPKT_
101b5a130:	5f bc 00 71	cmp	w2, #0x2f
101b5a134:	a0 01 00 54	b.eq	0x101b5a168
101b5a138:	a9 fb 84 52	mov	w9, #0x27dd
101b5a13c:	5f 00 09 6b	cmp	w2, w9
101b5a140:	c1 01 00 54	b.ne	0x101b5a178
101b5a144:	01 20 01 91	add	x1, x0, #0x48
101b5a148:	e0 03 08 aa	mov	x0, x8
101b5a14c:	3e 0e a4 17	b	__ZN7CReader4ReadI12CCultureTypeEEvRPKT_
101b5a150:	01 40 01 91	add	x1, x0, #0x50
101b5a154:	e0 03 08 aa	mov	x0, x8
101b5a158:	72 f9 a0 17	b	__ZN7CReader4ReadI9CReligionEEvRPKT_
101b5a15c:	01 40 04 91	add	x1, x0, #0x110
101b5a160:	e0 03 08 aa	mov	x0, x8
101b5a164:	f7 dd 00 15	b	__ZN7CReader4ReadER11CFixedPoint
101b5a168:	00 60 01 91	add	x0, x0, #0x58
101b5a16c:	e1 03 08 aa	mov	x1, x8
101b5a170:	02 00 80 52	mov	w2, #0x0
101b5a174:	d5 8c d2 17	b	__ZN18CJominiScriptValueI11CFixedPointE4ReadER7CReadert
101b5a178:	e0 03 08 aa	mov	x0, x8
101b5a17c:	5c f4 fe 14	b	__ZN7CReader16ReportUnexpectedEv
