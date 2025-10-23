import argparse
import cv2
import glob
import os
import math
import numpy as np
import axengine as axe

def pre_process(img, tile_size=108, tile_pad=10):
    """Pre-process, such as pre-pad and mod pad, so that the images can be divisible
    """
    # mod pad for divisible borders
    pad_h, pad_w = 0, 0
    h, w = img.shape[0:2]

    if h % tile_size != 0:
        pad_h = (tile_size - h % tile_size)
    if w % tile_size != 0:
        pad_w = (tile_size - w % tile_size)
    img = np.pad(img, ((0, pad_h), (0, pad_w), (0, 0)), 'constant')   #mode='reflect')

    # boundary pad
    img = np.pad(img, ((tile_pad, tile_pad), (tile_pad, tile_pad), (0, 0)), 'constant')

    # to CHW-Batch format
    img = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)

    return img

def tile_process(img, origin_shape, model, scale=2, tile_size=108, tile_pad=10, imgname=None):
    """It will first crop input images to tiles, and then process each tile.
    Finally, all the processed tiles are merged into one images.
    """

    # determine model paths
    if not os.path.exists(model):
        raise ValueError(f'Model {model} does not exist.')

    session = axe.InferenceSession(model)
    input_name = session.get_inputs()[0].name
    output_names = [x.name for x in session.get_outputs()]

    # tile
    batch, channel, height, width = img.shape
    output_height = int(round(height * scale))
    output_width = int(round(width * scale))
    output_shape = (batch, channel, output_height, output_width)
    origin_h, origin_w = origin_shape[0:2]

    # start with black image
    output = np.zeros(output_shape)
    tiles_x = math.floor(width / tile_size)
    tiles_y = math.floor(height / tile_size)
    print(f'Tile {tiles_x} x {tiles_y} for image {imgname}')

    # loop over all tiles
    for y in range(tiles_y):
        for x in range(tiles_x):
            # extract tile from input image
            ofs_x = x * tile_size
            ofs_y = y * tile_size
            # input tile area on total image
            input_start_x = ofs_x
            input_end_x = min(ofs_x + tile_size, width)
            input_start_y = ofs_y
            input_end_y = min(ofs_y + tile_size, height)

            # input tile dimensions
            input_tile = img[:, :, input_start_y:(input_end_y+2*tile_pad),
                             input_start_x:(input_end_x+2*tile_pad)]

            # upscale tile
            try:
                output_tile = session.run(output_names, {input_name: input_tile})
            except RuntimeError as error:
                print('Error', error)
            #print(f'\tTile {tile_idx}/{tiles_x * tiles_y}')

            # output tile area on total image
            output_start_x = int(round(input_start_x * scale))
            output_end_x = int(round(input_end_x * scale))
            output_start_y = int(round(input_start_y * scale))
            output_end_y = int(round(input_end_y * scale))

            start_tile = int(round(tile_pad * scale))
            end_tile = int(round(tile_size * scale)) + start_tile

            output[:, :, output_start_y:output_end_y,
                   output_start_x:output_end_x] = output_tile[0][:, :, start_tile:end_tile, start_tile:end_tile]

    # remove extra padding parts
    output = output[:, :, :int(round(origin_h * scale)), :int(round(origin_w * scale))].squeeze(0)
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0)).astype(np.float32)

    return output

def main():
    """Inference demo for Real-ESRGAN.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default='inputs', help='Input image or folder')
    parser.add_argument('-o', '--output', type=str, default='results', help='Output folder')
    parser.add_argument('-s', '--outscale', type=float, default=2, help='The final upsampling scale of the image, [Option:2, 4]')
    parser.add_argument(
        '--model_path', type=str, default=None, help='Model path. you need to specify it [Options: ]')
    parser.add_argument('--suffix', type=str, default='out', help='Suffix of the restored image')
    parser.add_argument('-t', '--tile', type=int, default=108, help='Tile size, 0 for no tile during testing')
    parser.add_argument('--tile_pad', type=int, default=10, help='Tile padding, (tile + tile_pad must == 128.)')
    parser.add_argument(
        '--ext',
        type=str,
        default='auto',
        help='Image extension. Options: auto | jpg | png, auto means using the same extension as inputs')

    args = parser.parse_args()

    # shape check
    assert (args.tile + 2*args.tile_pad) == 128, 'the model input size: 128.'

    # input
    if os.path.isfile(args.input):
        paths = [args.input]
    else:
        paths = sorted(glob.glob(os.path.join(args.input, '*')))

    # output
    os.makedirs(args.output, exist_ok=True)

    for idx, path in enumerate(paths):
        imgname, extension = os.path.splitext(os.path.basename(path))
        print('Testing', idx, imgname)
        if extension not in ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.webp']:
            continue

        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print('Error loading image')
            continue
        img = img.astype(np.float32)
        if np.max(img) > 256:  # 16-bit image
            max_range = 65535
            print('\tInput is a 16-bit image')
        else:
            max_range = 255
        img = img / max_range
        if len(img.shape) == 2:  # gray image
            img_mode = 'L'
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:  # RGBA image with alpha channel
            img_mode = 'RGBA'
            alpha = img[:, :, 3]
            img = img[:, :, 0:3]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_mode = 'RGB'
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # pre-process
        origin_shape = img.shape
        img = pre_process(img, args.tile)

        # tile process
        try:
            output_img = tile_process(img, origin_shape, args.model_path, args.outscale, args.tile, args.tile_pad, imgname)
        except RuntimeError as error:
            print('Error', error)
            print('If you encounter out of memory, try to set --tile with a smaller number.')

        if img_mode == 'L':
            output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
        if img_mode == 'RGBA':
            h, w = alpha.shape[0:2]
            output_alpha = cv2.resize(
                alpha,
                (int(round(w * args.outscale)),
                int(round(h * args.outscale))),
                interpolation=cv2.INTER_LINEAR
            )
            output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2BGRA)
            output_img[:, :, 3] = output_alpha

        if max_range == 65535:  # 16-bit image
            output = np.clip((output_img * 65535.0), 0, 65535).astype(np.uint16)
        else:
            output = np.clip((output_img * 255.0), 0, 255).astype(np.uint8)

        if args.ext == 'auto':
            extension = extension[1:]
        else:
            extension = args.ext

        if args.suffix == '':
            save_path = os.path.join(args.output, f'{imgname}.{extension}')
        else:
            save_path = os.path.join(args.output, f'{imgname}_{args.suffix}.{extension}')
        cv2.imwrite(save_path, output)

if __name__ == '__main__':
    main()
