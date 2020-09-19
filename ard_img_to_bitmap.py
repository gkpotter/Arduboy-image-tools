import argparse
from PIL import Image

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-t', '--threshold', default = 122)
	parser.add_argument('-i', '--input_file', required = True)
	parser.add_argument('-o', '--output_file', default = './bitmaps.h')

	parser.add_argument('-w', '--frame_width', type=int)

	args = parser.parse_args()

	name = args.input_file.split('/')[-1].split('.')[0]

	im = Image.open(args.input_file).convert('L')
	w, h = im.size

	if args.frame_width == None:
		args.frame_width = w
	elif w % args.frame_width != 0:
		print('Uneven number of frames.')
		return

	is_array = w//args.frame_width > 1

	if h % 8 != 0:
		print('Height not dividible by 8. By default, the Arduboy reads one byte at a time and draws eight pixels vertically.')
		return

	pix = im.load()
	
	output = 'const unsigned char PROGMEM ' + name + '[]' + ('[]' if is_array else '') + ' = {\n'

	for frame in range(w//args.frame_width):
		output += ('{' if is_array else '')
		
		for y_off in range(0, h, 8):
			for x in range(frame*args.frame_width, (frame+1)*args.frame_width):
				block = 0
				
				for y in range(y_off+7, y_off-1, -1):
					block += 2**(y-y_off) * (pix[x,y]>args.threshold)
				
				output += str(hex(block)) + ','
			output += ('},\n' if is_array and y_off == h - 8 else '\n')
	output += '};\n'

	output_file = open(args.output_file, 'a')
	output_file.write(output)
	output_file.close()

if __name__ == '__main__':
	main()