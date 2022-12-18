import random
import tkinter as tk
from tkinter import messagebox


CELL_SIZE = 40  # size of a cell
C = 15  # number of colums in the canvas
R = 20  # number of rows in the canvas
BOARD_HEIGHT = R * CELL_SIZE
BOARD_WIDTH = C * CELL_SIZE

# shape of blocks. row_id for y, col_id for x
BLOCK_SHAPES = {
    'O': [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    'Z': [(-1, -1), (0, -1), (0, 0), (1, 0)],
    'S': [(-1, 0), (0, 0), (0, -1), (1, -1)],
    'T': [(-1, 0), (0, 0), (0, -1), (1, 0)],
    'I': [(0, 1), (0, 0), (0, -1), (0, -2)],
    'L': [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    'J': [(-1, 0), (0, 0), (0, -1), (0, -2)]
}
# color of blocks
BLOCK_COLORS = {
    'O': 'blue',
    'Z': 'Cyan',
    'S': 'red',
    'T': 'yellow',
    'I': 'green',
    'L': 'purple',
    'J': 'orange',
}

FPS = 500  # in ms


def draw_block_one(canvas, c, r, color='#000000'):
    """ Draw empty blocks as the background

    :param canvas: the canvas to draw a block
    :param c: colom of the block
    :param r: row of the block
    :param color: color of the block
    """
    x0 = c * CELL_SIZE
    y0 = r * CELL_SIZE
    x1 = c * CELL_SIZE + CELL_SIZE
    y1 = r * CELL_SIZE + CELL_SIZE
    # draw and fill a box at given row and colum, and the white border width 2
    canvas.create_rectangle(
        x0, y0, x1, y1, fill=color, outline='black', width=1)


def draw_board(canvas, block_list):
    """ Draw an empty board """
    for ri in range(R):
        for ci in range(C):
            cell_type = block_list[ri][ci]
            if cell_type:
                draw_block_one(canvas, ci, ri, BLOCK_COLORS[cell_type])
            else:
                draw_block_one(canvas, ci, ri)


def draw_cells(canvas, c, r, cell_list, color='#000000'):
    """ Draw the cell with given shape and color

    canvas: canvas
    r: row
    c: colom
    cell_list: the shape
    color: the color of that shape
    """

    for cell in cell_list:
        cell_c, cell_r = cell
        ci = cell_c + c
        ri = cell_r + r
        # draw the cell only if it's in whthin the board
        if 0 <= c < C and 0 <= r < R:
            # draw the cell
            draw_block_one(canvas, ci, ri, color)


def draw_block_move(canvas, block, direction=[0, 0]):
    """ draw the block after moving

    canvas:
    block:
    direction
    """
    # get the block
    shape_type = block['kind']
    c, r = block['cr']
    cell_list = block['cell_list']
    # clear original clock before moving
    draw_cells(canvas, c, r, cell_list)
    # move in the given direction
    dc, dr = direction
    new_c, new_r = c + dc, r + dr
    block['cr'] = [new_c, new_r]
    # draw the block at new position
    draw_cells(canvas, new_c, new_r, cell_list, BLOCK_COLORS[shape_type])


def generate_new_block():
    """ randonly generate a new block """
    kind = random.choice(list(BLOCK_SHAPES.keys()))
    # origin at the up left corner, x increases when going right
    # y increases when going down
    cr = [C // 2, 0]
    new_block = {
        'kind': kind,
        'cell_list': BLOCK_SHAPES[kind],
        'cr': cr  # original position before moving
    }

    return new_block


# anchor the block when it landed, then generate a new block
def check_move(block, direction=[0, 0]):
    """ check if the block is able to move in the given direction

    block:
    direction:
    boolean:
    """
    cc, cr = block['cr']
    cell_list = block['cell_list']
    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc + direction[0]
        r = cell_r + cr + direction[1]
        # check if the block is in the board
        # don't check the top line of the board
        if c < 0 or c >= C or r >= R:
            return False

        # r >= 0
        if r >= 0 and block_list[r][c]:
            return False

    return True


# make a record
def save_block_to_list(block):  # for the block won't move
    shape_type = block['kind']
    cc, cr = block['cr']
    cell_list = block['cell_list']
    # save the type
    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc
        r = cell_r + cr
        # save
        block_list[r][c] = shape_type


def horizontal_move_block(event):
    """ move the block horizontally """
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block, direction):
        # move and draw
        draw_block_move(canvas, current_block, direction)


def rotate_block(event):
    """ changing the shape of a block """
    global current_block
    if current_block is None:
        return
    # rotate all the cells in the block
    cell_list = current_block['cell_list']
    rotate_list = []
    for cell in cell_list:
        cell_c, cell_r = cell
        rotate_cell = [cell_r, cell_c]
        rotate_list.append(rotate_cell)
    # new block after rotating
    block_after_rotate = {
        'kind': current_block['kind'],
        'cell_list': rotate_list,
        'cr': current_block['cr']
    }

    if check_move(block_after_rotate):  # check if it's able to rotate
        cc, cr = current_block['cr']
        # clear the original block
        draw_cells(canvas, cc, cr, current_block['cell_list'])
        # draw the block after rotating
        draw_cells(
            canvas, cc, cr, rotate_list, BLOCK_COLORS[current_block['kind']])
        current_block = block_after_rotate


def land(event):
    """ for the blocks landed """
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    cc, cr = current_block['cr']
    min_height = R
    for cell in cell_list:
        cell_c, cell_r = cell
        c, r = cell_c + cc, cell_r + cr
        if block_list[r][c]:
            return
        h = 0
        #
        for ri in range(r + 1, R):
            if block_list[ri][c]:
                break
            else:
                h += 1
        if h < min_height:
            min_height = h

    down = [0, min_height]
    if check_move(current_block, down):
        draw_block_move(canvas, current_block, down)


def check_row_complete(row):
    """ check if it's ok to clear a row """
    for cell in row:
        if cell == '':
            return False

    return True


def check_and_clear():
    has_complete_row = False
    for ri in range(len(block_list)):
        if check_row_complete(block_list[ri]):
            has_complete_row = True
            # ok to clear current row
            if ri > 0:
                for cur_ri in range(ri, 0, -1):
                    block_list[cur_ri] = block_list[cur_ri - 1][:]
                block_list[0] = ['' for j in range(C)]
            else:
                block_list[ri] = ['' for j in range(C)]
            global score
            score += 10

    if has_complete_row:
        draw_board(canvas, block_list)
        win.title(f'score: {score}')


# refresh the window
def game_loop():
    win.update()
    # down = [0, 1]
    # draw_block_move(canvas, a_block, down)
    global current_block
    if current_block is None:
        new_block = generate_new_block()
        # draw the new block
        draw_block_move(canvas, new_block)
        current_block = new_block
        # the position is already taken
        if not check_move(current_block, [0, 0]):
            # pop-up window
            messagebox.showinfo('Game over!!!', f'Your score: {score}')
            win.destroy()
            return
    else:
        if check_move(current_block, [0, 1]):
            draw_block_move(canvas, current_block, [0, 1])
        else:
            # can't move
            save_block_to_list(current_block)
            current_block = None
            check_and_clear()

    win.after(FPS, game_loop)


def main():
    pass


# tk
win = tk.Tk()
#
canvas = tk.Canvas(win, width=BOARD_WIDTH, height=BOARD_HEIGHT)
#
canvas.pack()

#
# draw_cells(canvas, 3, 3, BLOCK_SHAPES['O'], BLOCK_COLORS['O'])
#
# draw_cells(canvas, 3, 8, BLOCK_SHAPES['S'], BLOCK_COLORS['S'])
# draw_cells(canvas, 3, 13, BLOCK_SHAPES['T'], BLOCK_COLORS['T'])
# draw_cells(canvas, 8, 3, BLOCK_SHAPES['I'], BLOCK_COLORS['I'])
# draw_cells(canvas, 8, 8, BLOCK_SHAPES['L'], BLOCK_COLORS['L'])
# draw_cells(canvas, 8, 13, BLOCK_SHAPES['J'], BLOCK_COLORS['J'])
# draw_cells(canvas, 5, 18, BLOCK_SHAPES['Z'], BLOCK_COLORS['Z'])
#
# a_block = {
#     'kind': 'O',
#     'cell_list': BLOCK_SHAPES['O'],
#     'cr': [3, 3]
# }
#
current_block = None

#
block_list = []
#
for i in range(R):
    i_row = ['' for j in range(C)]
    block_list.append(i_row)
draw_board(canvas, block_list)

#
canvas.focus_set()
canvas.bind('<KeyPress-Left>', horizontal_move_block)
canvas.bind('<KeyPress-Right>', horizontal_move_block)#
canvas.bind('<KeyPress-Up>', rotate_block)
canvas.bind('<KeyPress-Down>', land)

#
score = 0
win.title(f'Score: {score}')
win.update()
win.after(FPS, game_loop)
win.mainloop()


if __name__ == '__main__':
    main()
