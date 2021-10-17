import os
import traceback
from tkinter import Entry, Tk, Label, filedialog as fd, Button, END, Frame, W, E
from tkinter.messagebox import showerror, showinfo, askokcancel
from git import Repo, rmtree, refresh
from git.exc import InvalidGitRepositoryError
import platform

if platform.system() == 'Windows':
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)


def get_addons_path():
    root_path = os.getenv('APPDATA') + "\\Blender Foundation\\Blender"
    if not os.path.exists(root_path):
        showinfo('Blender Not Found',
                 'Unable to automatically locate the addons folder.')
        return None

    dir_name = 'addons'
    for root, dirs, files in os.walk(root_path):
        if dir_name in dirs:
            return os.path.join(root, dir_name)


window = Tk()
window.title("Sollumz Automatic Updater")
# Gets the requested values of the height and widht.
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)

WINDOW_PADDING = 10
ITEM_PADDING = 5
ENTRY_WIDTH = int((windowWidth / 4) - 10)

# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))
frame = Frame(window)
frame.pack(anchor='w', padx=WINDOW_PADDING, pady=WINDOW_PADDING)

repo_url = 'https://github.com/Skylumz/Sollumz.git'
repo_label = Label(frame, text='Repo')
repo_label.pack(pady=ITEM_PADDING, anchor="w")

repo_entry = Entry(frame, width=ENTRY_WIDTH)
repo_entry.insert(0, repo_url)
repo_entry.pack(pady=ITEM_PADDING, anchor="w")

branch_label = Label(frame, text='Branch')
branch_label.pack(pady=ITEM_PADDING, anchor="w")

branch_entry = Entry(frame, width=ENTRY_WIDTH)
branch_entry.insert(0, 'refactor')
branch_entry.pack(pady=ITEM_PADDING, anchor="w")

select_label = Label(frame, text="Select Blender Addons Directory")
select_label.pack()

path_entry = Entry(frame, width=ENTRY_WIDTH)
path_entry.insert(0, get_addons_path() or 'unknown')
path_entry.pack(pady=ITEM_PADDING, anchor="w")


def select_dir():
    dir = fd.askdirectory(title="Select Directory",
                          initialdir=get_addons_path() or '/')
    path_entry.delete(0, END)
    path_entry.insert(0, dir)
    path_entry.pack()


# open button
open_button = Button(frame, text="Select Directory", command=select_dir)
open_button.pack(expand=True, pady=ITEM_PADDING, anchor="w")


def get_git_repo(path):
    try:
        repo = Repo(path)
        _ = repo.git_dir
        return repo
    except InvalidGitRepositoryError:
        return None


def update():
    try:
        dir = path_entry.get()
        if not os.path.exists(dir):
            showerror("Invalid Path", "Path does not exist!")
            return

        # If addon already exists
        addon_path = get_addons_path() + '\Sollumz'
        if os.path.exists(addon_path):
            repo = get_git_repo(addon_path)
            if repo:
                overwrite = askokcancel(
                    'Overwrite Directory', "Existing Sollumz installation found. In order to continue this install, the folder will be overwritten.")
                if not overwrite:
                    return
            rmtree(addon_path)
            # for root, dirs, files in os.walk(addon_path, topdown=False):
            #     for name in files:
            #         os.remove(os.path.join(root, name))
            #     for name in dirs:
            #         os.rmdir(os.path.join(root, name))
            # os.rmdir(addon_path)

        repo = Repo.clone_from(repo_url, dir + '\Sollumz')
        # Switch branch
        git = repo.git
        git.checkout(branch_entry.get())
        git.for_each_ref()
        showinfo('Success', 'Sollumz successfully updated.')
    except Exception as e:
        showerror("Error", traceback.format_exc())


update_button = Button(frame, text="Update", command=update)
update_button.pack(expand=True, pady=ITEM_PADDING, anchor="w")

window.mainloop()
