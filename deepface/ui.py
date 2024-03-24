import os
import sys
import webbrowser
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL
from typing import Any, Callable, Tuple, Optional
import cv2
from PIL import Image, ImageOps

import deepface.globals
import deepface.metadata
from deepface.face_analyser import get_one_face
from deepface.capturer import get_video_frame, get_video_frame_total
from deepface.face_reference import get_face_reference, set_face_reference, clear_face_reference
from deepface.predictor import predict_frame, clear_predictor
from deepface.processors.frame.core import get_frame_processors_modules
from deepface.utilities import is_image, is_video, resolve_relative_path
from PIL import Image, ImageTk

ROOT = None
ROOT_HEIGHT = 700
ROOT_WIDTH = 600

PREVIEW = None
PREVIEW_MAX_HEIGHT = 700
PREVIEW_MAX_WIDTH = 1200

RECENT_DIRECTORY_SOURCE = None
RECENT_DIRECTORY_TARGET = None
RECENT_DIRECTORY_OUTPUT = None

preview_label = None
preview_slider = None
source_label = None
target_label = None
status_label = None


# todo: remove by native support -> https://github.com/TomSchimansky/CustomTkinter/issues/934
class CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


def init(start: Callable[[], None], destroy: Callable[[], None]) -> ctk.CTk:
    global ROOT, PREVIEW

    ROOT = create_root(start, destroy)
    PREVIEW = create_preview(ROOT)

    return ROOT


def create_root(start: Callable[[], None], destroy: Callable[[], None]) -> ctk.CTk:
    global source_label, target_label, status_label

    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode('system')
    ctk.set_default_color_theme(resolve_relative_path('ui.json'))

    root = CTk()
    root.minsize(ROOT_WIDTH, ROOT_HEIGHT)
    root.title(f'{deepface.metadata.name} {deepface.metadata.version}')
    root.configure()
    root.protocol('WM_DELETE_WINDOW', lambda: destroy())

    header = ctk.CTkLabel(root, text='DeepFace', justify='center', cursor='hand2')
    header.place(relx=0.1, rely=0.06, relwidth=0.8)
    header.configure(text_color=ctk.ThemeManager.theme.get('DeepFaceTitle').get('text_color'))
    header.configure(font=("Arial", 20))
    header.bind('<Button>', lambda event: webbrowser.open('https://github.com/skytells-research/deepface'))


    button_image = ctk.CTkImage(Image.open("deepface/assets/logo.png"), size=(120, 120))
    logo = ctk.CTkLabel(root, text='', image=button_image, justify='center', cursor='hand2')
    logo.place(relx=0.1, rely=0.1, relwidth=0.8)
    logo.configure(text_color=ctk.ThemeManager.theme.get('DeepFaceCopyrights').get('text_color'))
    logo.bind('<Button>', lambda event: webbrowser.open('https://github.com/skytells-research/deepface'))

    
   



    source_label = ctk.CTkLabel(root, text=None, fg_color=ctk.ThemeManager.theme.get('DeepFaceDropArea').get('fg_color'))
    source_label.place(relx=0.1, rely=0.26, relwidth=0.3, relheight=0.25)
    source_label.configure(corner_radius=source_label.winfo_screenwidth() / 2)
    source_label.drop_target_register(DND_ALL)
    source_label.dnd_bind('<<Drop>>', lambda event: select_source_path(event.data))
    if deepface.globals.source_path:
        select_source_path(deepface.globals.source_path)

    target_label = ctk.CTkLabel(root, text=None, fg_color=ctk.ThemeManager.theme.get('DeepFaceDropArea').get('fg_color'))
    target_label.place(relx=0.6, rely=0.26, relwidth=0.3, relheight=0.25)
    target_label.configure(corner_radius=target_label.winfo_screenwidth() / 2)
    target_label.drop_target_register(DND_ALL)
    target_label.dnd_bind('<<Drop>>', lambda event: select_target_path(event.data))
    if deepface.globals.target_path:
        select_target_path(deepface.globals.target_path)

    source_button = ctk.CTkButton(root, text='Select a face', cursor='hand2', command=lambda: select_source_path())
    source_button.place(relx=0.1, rely=0.53, relwidth=0.3, relheight=0.04)

    target_button = ctk.CTkButton(root, text='Select a target', cursor='hand2', command=lambda: select_target_path())
    target_button.place(relx=0.6, rely=0.53, relwidth=0.3, relheight=0.04)

    keep_fps_value = ctk.BooleanVar(value=deepface.globals.keep_fps)
    keep_fps_checkbox = ctk.CTkSwitch(root, text='Keep target fps', variable=keep_fps_value, cursor='hand2', command=lambda: setattr(deepface.globals, 'keep_fps', not deepface.globals.keep_fps))
    keep_fps_checkbox.place(relx=0.1, rely=0.66)

    keep_frames_value = ctk.BooleanVar(value=deepface.globals.keep_frames)
    keep_frames_switch = ctk.CTkSwitch(root, text='Keep temporary frames', variable=keep_frames_value, cursor='hand2', command=lambda: setattr(deepface.globals, 'keep_frames', keep_frames_value.get()))
    keep_frames_switch.place(relx=0.1, rely=0.71)

    skip_audio_value = ctk.BooleanVar(value=deepface.globals.skip_audio)
    skip_audio_switch = ctk.CTkSwitch(root, text='Skip target audio', variable=skip_audio_value, cursor='hand2', command=lambda: setattr(deepface.globals, 'skip_audio', skip_audio_value.get()))
    skip_audio_switch.place(relx=0.6, rely=0.66)

    many_faces_value = ctk.BooleanVar(value=deepface.globals.many_faces)
    many_faces_switch = ctk.CTkSwitch(root, text='Many faces', variable=many_faces_value, cursor='hand2', command=lambda: setattr(deepface.globals, 'many_faces', many_faces_value.get()))
    many_faces_switch.place(relx=0.6, rely=0.71)

    start_button = ctk.CTkButton(root, text='Start', cursor='hand2', command=lambda: select_output_path(start))
    start_button.place(relx=0.15, rely=0.81, relwidth=0.2, relheight=0.05)

    stop_button = ctk.CTkButton(root, text='Destroy', cursor='hand2', command=lambda: destroy())
    stop_button.place(relx=0.4, rely=0.81, relwidth=0.2, relheight=0.05)

    preview_button = ctk.CTkButton(root, text='Preview', cursor='hand2', command=lambda: toggle_preview())
    preview_button.place(relx=0.65, rely=0.81, relwidth=0.2, relheight=0.05)

    status_label = ctk.CTkLabel(root, text=None, justify='center')
    status_label.place(relx=0.1, rely=0.9, relwidth=0.8)

    

    copyrights = ctk.CTkLabel(root, text='Skytells AI Research', justify='center', cursor='hand2')
    copyrights.place(relx=0.1, rely=0.95, relwidth=0.8)
    copyrights.configure(text_color=ctk.ThemeManager.theme.get('DeepFaceCopyrights').get('text_color'))
    copyrights.bind('<Button>', lambda event: webbrowser.open('https://github.com/skytells-research/deepface'))

    return root


def create_preview(parent: ctk.CTkToplevel) -> ctk.CTkToplevel:
    global preview_label, preview_slider

    preview = ctk.CTkToplevel(parent)
    preview.withdraw()
    preview.configure()
    preview.protocol('WM_DELETE_WINDOW', lambda: toggle_preview())
    preview.resizable(width=False, height=False)

    preview_label = ctk.CTkLabel(preview, text=None)
    preview_label.pack(fill='both', expand=True)

    preview_slider = ctk.CTkSlider(preview, from_=0, to=0, command=lambda frame_value: update_preview(frame_value))

    preview.bind('<Up>', lambda event: update_face_reference(1))
    preview.bind('<Down>', lambda event: update_face_reference(-1))
    return preview


def update_status(text: str) -> None:
    status_label.configure(text=text)
    ROOT.update()


def select_source_path(source_path: Optional[str] = None) -> None:
    global RECENT_DIRECTORY_SOURCE

    if PREVIEW:
        PREVIEW.withdraw()
    if source_path is None:
        source_path = ctk.filedialog.askopenfilename(title='select an source image', initialdir=RECENT_DIRECTORY_SOURCE)
    if is_image(source_path):
        deepface.globals.source_path = source_path
        RECENT_DIRECTORY_SOURCE = os.path.dirname(deepface.globals.source_path)
        image = render_image_preview(deepface.globals.source_path, (200, 200))
        source_label.configure(image=image)
    else:
        deepface.globals.source_path = None
        source_label.configure(image=None)


def select_target_path(target_path: Optional[str] = None) -> None:
    global RECENT_DIRECTORY_TARGET

    if PREVIEW:
        PREVIEW.withdraw()
    clear_face_reference()
    if target_path is None:
        target_path = ctk.filedialog.askopenfilename(title='select an target image or video', initialdir=RECENT_DIRECTORY_TARGET)
    if is_image(target_path):
        deepface.globals.target_path = target_path
        RECENT_DIRECTORY_TARGET = os.path.dirname(deepface.globals.target_path)
        image = render_image_preview(deepface.globals.target_path, (200, 200))
        target_label.configure(image=image)
    elif is_video(target_path):
        deepface.globals.target_path = target_path
        RECENT_DIRECTORY_TARGET = os.path.dirname(deepface.globals.target_path)
        video_frame = render_video_preview(target_path, (200, 200))
        target_label.configure(image=video_frame)
    else:
        deepface.globals.target_path = None
        target_label.configure(image=None)


def select_output_path(start: Callable[[], None]) -> None:
    global RECENT_DIRECTORY_OUTPUT

    if is_image(deepface.globals.target_path):
        output_path = ctk.filedialog.asksaveasfilename(title='save image output file', defaultextension='.png', initialfile='output.png', initialdir=RECENT_DIRECTORY_OUTPUT)
    elif is_video(deepface.globals.target_path):
        output_path = ctk.filedialog.asksaveasfilename(title='save video output file', defaultextension='.mp4', initialfile='output.mp4', initialdir=RECENT_DIRECTORY_OUTPUT)
    else:
        output_path = None
    if output_path:
        deepface.globals.output_path = output_path
        RECENT_DIRECTORY_OUTPUT = os.path.dirname(deepface.globals.output_path)
        start()


def render_image_preview(image_path: str, size: Tuple[int, int]) -> ctk.CTkImage:
    image = Image.open(image_path)
    if size:
        image = ImageOps.fit(image, size, Image.LANCZOS)
    return ctk.CTkImage(image, size=image.size)


def render_video_preview(video_path: str, size: Tuple[int, int], frame_number: int = 0) -> ctk.CTkImage:
    capture = cv2.VideoCapture(video_path)
    if frame_number:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    has_frame, frame = capture.read()
    if has_frame:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if size:
            image = ImageOps.fit(image, size, Image.LANCZOS)
        return ctk.CTkImage(image, size=image.size)
    capture.release()
    cv2.destroyAllWindows()


def toggle_preview() -> None:
    if PREVIEW.state() == 'normal':
        PREVIEW.unbind('<Right>')
        PREVIEW.unbind('<Left>')
        PREVIEW.withdraw()
        clear_predictor()
    elif deepface.globals.source_path and deepface.globals.target_path:
        init_preview()
        update_preview(deepface.globals.reference_frame_number)
        PREVIEW.deiconify()


def init_preview() -> None:
    PREVIEW.title('Preview [ ↕ Reference face ]')
    if is_image(deepface.globals.target_path):
        preview_slider.pack_forget()
    if is_video(deepface.globals.target_path):
        video_frame_total = get_video_frame_total(deepface.globals.target_path)
        if video_frame_total > 0:
            PREVIEW.title('Preview [ ↕ Reference face ] [ ↔ Frame number ]')
            PREVIEW.bind('<Right>', lambda event: update_frame(int(video_frame_total / 20)))
            PREVIEW.bind('<Left>', lambda event: update_frame(int(video_frame_total / -20)))
        preview_slider.configure(to=video_frame_total)
        preview_slider.pack(fill='x')
        preview_slider.set(deepface.globals.reference_frame_number)


def update_preview(frame_number: int = 0) -> None:
    if deepface.globals.source_path and deepface.globals.target_path:
        temp_frame = get_video_frame(deepface.globals.target_path, frame_number)
        if predict_frame(temp_frame):
            sys.exit()
        source_face = get_one_face(cv2.imread(deepface.globals.source_path))
        if not get_face_reference():
            reference_frame = get_video_frame(deepface.globals.target_path, deepface.globals.reference_frame_number)
            reference_face = get_one_face(reference_frame, deepface.globals.reference_face_position)
            set_face_reference(reference_face)
        else:
            reference_face = get_face_reference()
        for frame_processor in get_frame_processors_modules(deepface.globals.frame_processors):
            temp_frame = frame_processor.process_frame(
                source_face,
                reference_face,
                temp_frame
            )
        image = Image.fromarray(cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB))
        image = ImageOps.contain(image, (PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT), Image.LANCZOS)
        image = ctk.CTkImage(image, size=image.size)
        preview_label.configure(image=image)


def update_face_reference(steps: int) -> None:
    clear_face_reference()
    reference_frame_number = int(preview_slider.get())
    deepface.globals.reference_face_position += steps
    deepface.globals.reference_frame_number = reference_frame_number
    update_preview(reference_frame_number)


def update_frame(steps: int) -> None:
    frame_number = preview_slider.get() + steps
    preview_slider.set(frame_number)
    update_preview(preview_slider.get())
