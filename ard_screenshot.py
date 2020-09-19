import serial
import time
import argparse
import numpy as np
from PIL import Image

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-p','--port', required=True)

	args = parser.parse_args()

	with serial.Serial(args.port) as ser:
		print('Listening for screenshots on port {} ...'.format(args.port))

		while True:
			buffer_data = ser.read(1024)

			chunks = [bin(x) for x in list(buffer_data)]
			pixel_array = np.zeros((64, 128), dtype=np.int8)

			x_off = 0
			y_off = 0

			for chunk in chunks:
				pixel_chunk = [255 if x == '1' else 0 for x in chunk[2:].zfill(8)]
				pixel_chunk.reverse()
				
				for y in range(y_off, y_off+8):
					pixel_array[y, x_off] = pixel_chunk[y-y_off]

				x_off+=1
				if x_off == 128:
					x_off = 0
					y_off += 8

			im = Image.fromarray(pixel_array, 'L')
			fn = './Screenshot_'+time.strftime("%Y-%m-%d_%H.%M.%S")+'.png'
			im.save(fn)
			print('Screenshot captured and saved to '+fn)

if __name__ == '__main__':
	main()