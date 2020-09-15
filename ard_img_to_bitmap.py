import argparse
from PIL import Image

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-threshold', default = 122)
	parser.add_argument('-input_file', required = True)
	parser.add_argument('-output_file', default = './bitmaps.h')

	args = parser.parse_args()

	name = args.input_file.split('/')[-1].split('.')[0]

	im = Image.open(args.input_file).convert('L')
	w, h = im.size

	if h%8 != 0:
		print('Height not dividible by 8. By default, the Arduboy reads one byte at a time and draws eight pixels vertically.')
		return

	pix = im.load()
	
	output = 'const unsigned char PROGMEM ' + name +'[] = {\n'

	for y_off in range(0,h,8):
		for x in range(w):
			block = 0
			for y in range(y_off+7,y_off-1,-1):
				block += 2**(y-y_off)*(pix[x,y]>args.threshold)
			output+= str(hex(block)) + ','
		output +='\n'
	output+='};\n'

	output_file = open(args.output_file, 'a')
	output_file.write(output)
	output_file.close()

if __name__ == '__main__':
	main()