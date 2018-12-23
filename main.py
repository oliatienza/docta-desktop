import tkinter, os, numpy
from tkinter import filedialog, Grid, Label, Scrollbar
from PIL import ImageTk, Image

def get_density(img):
    matrix = numpy.asarray(img)
    height = matrix.shape[0]
    width = matrix.shape[1]

    white = 0
    total = height * width

    for i in range(height):
            for j in range(width):
                    if matrix[i][j]  == 255:
                            white = white + 1

    return white/total

def get_file_paths(type, extension):
    path = ''
    if type == 'ORIG':
        global orig_path
        path = orig_path

    elif type == 'BIN':
        global binary_path
        path = binary_path

    elif type == 'SKL':
        global skeleton_path
        path = skeleton_path

    else:
        return

    paths = []
    filenames = []
    for filename in os.listdir(path):
            if filename.endswith(extension):
                    fullpath = path + '/' + filename
                    paths.append(fullpath)
                    filenames.append(filename)

    return [paths, filenames]

def choose_directory(type):
    if type == 'ORIG':
        global orig_path, orig_path_entry
        orig_path = filedialog.askdirectory()
        orig_path_entry.delete(0, 'end')
        orig_path_entry.insert(0, orig_path)

    elif type == 'BIN':
        global binary_path, binary_path_entry
        binary_path = filedialog.askdirectory()
        binary_path_entry.delete(0, 'end')
        binary_path_entry.insert(0, binary_path)

    elif type == 'SKL':
        global skeleton_path, skeleton_path_entry
        skeleton_path = filedialog.askdirectory()
        skeleton_path_entry.delete(0, 'end')
        skeleton_path_entry.insert(0, skeleton_path)

    else:
        return

def process():
    orig_paths, orig_filenames = get_file_paths('ORIG', '.bmp')
    binary_paths, binary_filenames = get_file_paths('BIN', '.bmp')
    skeleton_paths, skeleton_filenames = get_file_paths('SKL', '.bmp')


    results = tkinter.Toplevel(root)
    results.title('Results')
    results.geometry('720x480')

    sb = Scrollbar(results, orient = tkinter.VERTICAL)
    sb.grid(row = 0, column = 1, sticky = 'ns')

    # results_top = tkinter.Frame(results)
    # results_top.grid(sticky = 'nsew')

    canvas = tkinter.Canvas(results)
    canvas.grid(row = 0, column = 0, sticky = 'nsew')
    Grid.rowconfigure(results, 0, weight=1)
    Grid.columnconfigure(results, 0, weight=1)
    results_frame = tkinter.Frame(canvas)
    canvas.create_window(0, 0, window = results_frame, anchor = 'nw')
    canvas.configure(scrollregion = canvas.bbox("all"))

    sb.config(command = canvas.yview)
    canvas.configure(yscrollcommand = sb.set)

    output_file = open('output.csv', 'w+')
    output_file.write('Filename,Vessel Density,Vessel Length Density\n')

    # for i in range(len(orig_paths) + 1):
    #     Grid.rowconfigure(results_frame, i, weight = 1)
    #     for j in range(6):
    #         Grid.columnconfigure(results_frame, j, weight = 1)

    header_filename = Label(results_frame, text = 'FILENAME')
    header_orig = Label(results_frame, text = 'ORIGINAL IMAGE')
    header_binary = Label(results_frame, text = 'BINARY IMAGE')
    header_skeleton = Label(results_frame, text = 'SKELETONIZED IMAGE')
    header_vd = Label(results_frame, text = 'VESSEL DENSITY')
    header_vdl = Label(results_frame, text = 'VESSEL LENGTH DENSITY')

    header_filename.grid(row = 0, column = 0, sticky = 'nsew')
    header_orig.grid(row = 0, column = 1, sticky = 'nsew')
    header_binary.grid(row = 0, column = 2, sticky = 'nsew')
    header_skeleton.grid(row = 0, column = 3, sticky = 'nsew')
    header_vd.grid(row = 0, column = 4, sticky = 'nsew')
    header_vdl.grid(row = 0, column = 5, sticky = 'nsew')

    for i in range(len(orig_paths)):
        # print(i)

        #filename
        file_label = Label(results_frame, text = orig_filenames[i])
        file_label.grid(row = i + 1, column = 0, sticky = 'nsew')

        #original image
        orig_img = Image.open(orig_paths[i]).resize((200, 200))
        orig = ImageTk.PhotoImage(orig_img)
        orig_label = Label(results_frame, image = orig)
        orig_label.image = orig
        orig_label.grid(row = i + 1, column = 1, sticky = 'nsew')

        #binary image
        binary_img = Image.open(binary_paths[i]).resize((200, 200))
        binary = ImageTk.PhotoImage(binary_img)
        binary_label = Label(results_frame, image = binary)
        binary_label.image = binary
        binary_label.grid(row = i + 1, column = 2, sticky = 'nsew')

        #skeleton image
        skeleton_img = Image.open(skeleton_paths[i]).resize((200, 200))
        skeleton = ImageTk.PhotoImage(skeleton_img)
        skeleton_label = Label(results_frame, image = skeleton)
        skeleton_label.image = skeleton
        skeleton_label.grid(row = i + 1, column = 3, sticky = 'nsew')

        # #vessel density
        vd = get_density(binary_img)
        vd_label = Label(results_frame, text = str(vd))
        vd_label.grid(row = i + 1, column = 4, sticky = 'nsew')

        # #vessel length density
        vdl = get_density(skeleton_img)
        vdl_label = Label(results_frame, text = str(vdl))
        vdl_label.grid(row = i + 1, column = 5, sticky = 'nsew')
        output_file.write(orig_filenames[i] + "," + str(vd) + "," + str(vdl) + '\n')
    output_file.close()

# MAIN
root = tkinter.Tk()
root.title('CS 198')
root.geometry('426x240')
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

frame = tkinter.Frame(root)
frame.grid(row = 0, column = 0, sticky = 'nsew')

for i in range(3):
    Grid.rowconfigure(frame, i, weight = 1)
    for j in range(2):
        Grid.columnconfigure(frame, j, weight = j + 1)

# vars
orig_path = 'C:/Users/Luis/Desktop/School/CS198/data/cropped'
binary_path = 'C:/Users/Luis/Desktop/School/CS198/data/binarized'
skeleton_path = 'C:/Users/Luis/Desktop/School/CS198/data/skeletonized'
# orig_path = ''
# binary_path = ''
# skeleton_path = ''

# buttons
orig_path_btn = tkinter.Button(frame, text = 'Choose (ORIG) directory', command = lambda: choose_directory('ORIG'))
binary_path_btn = tkinter.Button(frame, text = 'Choose (BIN) directory', command = lambda: choose_directory('BIN'))
skeleton_path_btn = tkinter.Button(frame, text = 'Choose (SKL) directory', command = lambda: choose_directory('SKL'))
process_btn = tkinter.Button(frame, text = 'Process images', command = process)

# texts
orig_path_entry = tkinter.Entry(frame)
binary_path_entry = tkinter.Entry(frame)
skeleton_path_entry = tkinter.Entry(frame)

# gridding
orig_path_btn.grid(row = 0, column = 0, sticky = 'nsew')
binary_path_btn.grid(row = 1, column = 0, sticky = 'nsew')
skeleton_path_btn.grid(row = 2, column = 0, sticky = 'nsew')

orig_path_entry.grid(row = 0, column = 1, sticky = 'nsew')
binary_path_entry.grid(row = 1, column = 1, sticky = 'nsew')
skeleton_path_entry.grid(row = 2, column = 1, sticky = 'nsew')

process_btn.grid(row = 3, column = 0, columnspan = 2)

root.mainloop()