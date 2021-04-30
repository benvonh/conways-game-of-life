import tkinter as tk


HEIGHT = 1280
WIDTH = 720
root = tk.Tk()
canvas = tk.Canvas()
sim_text = tk.StringVar()
IS_RUNNING = False
CELLS = [[False for x in range(WIDTH//10)] for y in range(HEIGHT//10)]
CELLS_COUNT = [[0 for x in range(WIDTH//10)] for y in range(HEIGHT//10)]


# Initialize root window
def init_root():
    root.title("Conway's Game of Life")
    root.geometry(f"{HEIGHT}x{WIDTH}")
    root.bind("x", lambda event: init_control())
    make_grid()
    canvas.pack(fill=tk.BOTH, expand=1)
    canvas.bind("<B1-Motion>", handle_button1)
    canvas.bind("<B3-Motion>", handle_button2)


# Initialize control window
def init_control():
    control = tk.Toplevel()
    control.geometry("300x100")
    control.title("Controls")
    btn_reset = tk.Button(control, text="Reset Grid", command=make_grid, anchor="e")
    btn_sim = tk.Button(control, textvariable=sim_text, command=change_sim, anchor="e")
    btn_reset.pack(expand=1)
    btn_sim.pack(expand=1)
    sim_text.set("Play")


def fill_rect(x, y, colour):
    canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill=colour)


def make_grid():
    global CELLS
    CELLS.clear()
    CELLS = [[False for x in range(WIDTH // 10)] for y in range(HEIGHT // 10)]
    canvas.delete("all")
    for row in range(1, HEIGHT//10 - 1):
        for col in range(1, WIDTH//10 - 1):
            fill_rect(row, col, "white")


def update_grid():
    canvas.delete("all")
    for row in range(1, HEIGHT//10 - 1):
        for col in range(1, WIDTH//10 - 1):
            if CELLS[row][col]:
                fill_rect(row, col, "green")
            else:
                fill_rect(row, col, "white")


def handle_button1(event=None):
    if not IS_RUNNING:
        row = event.x // 10
        col = event.y // 10
        fill_rect(row, col, "green")
        CELLS[row][col] = True


def handle_button2(event=None):
    if not IS_RUNNING:
        row = event.x // 10
        col = event.y // 10
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                fill_rect(row + offset_x, col + offset_y, "white")
                CELLS[row + offset_x][col + offset_y] = False


def change_sim():
    global IS_RUNNING
    IS_RUNNING = not IS_RUNNING
    if IS_RUNNING:
        sim_text.set("Pause")
    else:
        sim_text.set("Play")


def sim():
    if IS_RUNNING:
        verify_neighbours()
        cell_event()
        update_grid()
    root.after(1, sim)


def verify_neighbours():
    for x in range(1, HEIGHT//10 - 1):
        for y in range(1, WIDTH//10 - 1):
            neighbour_count = 0
            for offset_x in range(-1, 2):
                for offset_y in range(-1, 2):
                    test = CELLS[x+offset_x][y+offset_y]
                    if test and not (offset_x == 0 and offset_y == 0):
                        neighbour_count += 1
            CELLS_COUNT[x][y] = neighbour_count


def cell_event():
    for x in range(1, HEIGHT//10 - 1):
        for y in range(1, WIDTH//10 - 1):
            neighbours = CELLS_COUNT[x][y]
            if CELLS[x][y]:
                if neighbours < 2 or neighbours > 3:
                    CELLS[x][y] = False
            elif neighbours == 3:
                CELLS[x][y] = True


if __name__ == '__main__':
    init_root()
    init_control()
    sim()
    root.mainloop()
