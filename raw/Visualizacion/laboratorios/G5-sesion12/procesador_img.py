import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from sklearn.decomposition import PCA

# Tamaño máximo con que se muestra cada imagen (solo visualización;
# el procesamiento siempre se hace sobre la imagen original completa)
MAX_DISPLAY = (480, 520)


# --- NumPy (OpenCV) -> Tkinter Image ---
def np_to_tkimage(np_image, max_size=MAX_DISPLAY):
    if len(np_image.shape) == 2:  # Escala de grises
        img_pil = Image.fromarray(np_image)
    else:  # Color
        img_pil = Image.fromarray(cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB))

    # Reducir para que quepa en la ventana (mantiene proporción)
    img_pil.thumbnail(max_size, Image.LANCZOS)
    return ImageTk.PhotoImage(image=img_pil)


# --- Lógica de PCA ---
def aplicar_pca(imagen_np, k):
    """Aplica PCA y reconstruye una imagen en escala de grises."""
    media = np.mean(imagen_np, axis=0)

    # 1. Normalizar (centrar la media)
    img_norm = imagen_np.astype(float) - media

    # 2. Aplicar PCA
    pca = PCA(n_components=k)
    transformed = pca.fit_transform(img_norm)

    # 3. Reconstruir
    reconstructed = pca.inverse_transform(transformed)

    # 4. Devolver a la escala original
    reconstructed_img = reconstructed + media

    # 5. Rango [0, 255] y uint8
    return np.clip(reconstructed_img, 0, 255).astype(np.uint8)


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador de Imágenes")

        # --- Atributos de estado ---
        self.original_image_np = None   # Imagen NumPy (procesamiento)
        self.original_image_tk = None   # Referencia Tkinter (original)
        self.processed_image_tk = None  # Referencia Tkinter (procesada)

        # --- Frame de controles ---
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Actividad 1: botón de carga
        self.load_button = tk.Button(control_frame, text="Cargar Imagen",
                                     command=self.cargar_imagen)
        self.load_button.pack(side=tk.LEFT)

        # Actividad 2: filtros
        self.filter_options = ['Original', 'Suavizado (Blur)', 'Bordes (Laplace)']
        self.filter_var = tk.StringVar(self.root)
        self.filter_var.set(self.filter_options[0])

        filter_menu = tk.OptionMenu(control_frame, self.filter_var,
                                    *self.filter_options)
        filter_menu.pack(side=tk.LEFT, padx=5)

        apply_filter_btn = tk.Button(control_frame, text="Aplicar Filtro",
                                     command=self.aplicar_filtro)
        apply_filter_btn.pack(side=tk.LEFT)

        # Actividad 3: PCA
        self.pca_slider = tk.Scale(control_frame, from_=1, to=100,
                                   orient=tk.HORIZONTAL, label="Componentes PCA")
        self.pca_slider.pack(side=tk.LEFT, padx=10)

        apply_pca_btn = tk.Button(control_frame, text="Reconstruir PCA",
                                  command=self.reconstruir_pca)
        apply_pca_btn.pack(side=tk.LEFT)

        # --- Frame de visualización ---
        display_frame = tk.Frame(self.root)
        display_frame.pack(fill=tk.BOTH, expand=True)

        self.original_label = tk.Label(
            display_frame,
            text="Imagen Original\n(Cargue una imagen para comenzar)",
            relief="sunken", padx=10, pady=10)
        self.original_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                                 padx=10, pady=10)

        self.processed_label = tk.Label(display_frame, text="Imagen Procesada",
                                        relief="sunken", padx=10, pady=10)
        self.processed_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True,
                                  padx=10, pady=10)

    # --- Utilidad: mostrar en el panel procesado ---
    def _mostrar_procesada(self, np_img):
        tk_image = np_to_tkimage(np_img)
        self.processed_label.config(image=tk_image, text="")
        self.processed_image_tk = tk_image  # Guardar referencia

    # --- Actividad 1 ---
    def cargar_imagen(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                       ("Todos los archivos", "*.*")])
        if not file_path:
            return  # El usuario canceló

        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            messagebox.showerror("Error", "No se pudo leer la imagen seleccionada.")
            return
        self.original_image_np = img

        tk_image = np_to_tkimage(self.original_image_np)
        self.original_label.config(image=tk_image, text="")
        self.original_image_tk = tk_image  # Referencia (crucial)

        # Mostrar también en el panel procesado al inicio
        self._mostrar_procesada(self.original_image_np)

        # Ajustar rango del slider al máximo de componentes posibles
        max_comp = min(self.original_image_np.shape)
        self.pca_slider.config(to=max_comp)
        if self.pca_slider.get() > max_comp:
            self.pca_slider.set(max_comp)

    # --- Actividad 2 ---
    def aplicar_filtro(self):
        if self.original_image_np is None:
            return

        filtro = self.filter_var.get()

        if filtro == 'Original':
            processed_np = self.original_image_np

        elif filtro == 'Suavizado (Blur)':
            kernel_blur = np.ones((7, 7), np.float32) / 49.0
            processed_np = cv2.filter2D(self.original_image_np, -1, kernel_blur)

        elif filtro == 'Bordes (Laplace)':
            kernel_laplace = np.array([[0, 1, 0],
                                       [1, -4, 1],
                                       [0, 1, 0]], np.float32)
            # Se calcula en 16 bits con signo y se toma el valor absoluto:
            # con uint8 los valores negativos se saturan a 0 y se pierden bordes.
            lap = cv2.filter2D(self.original_image_np, cv2.CV_16S, kernel_laplace)
            processed_np = cv2.convertScaleAbs(lap)

        else:
            return

        self._mostrar_procesada(processed_np)

    # --- Actividad 3 ---
    def reconstruir_pca(self):
        if self.original_image_np is None:
            return

        k = int(self.pca_slider.get())
        k = min(k, min(self.original_image_np.shape))

        reconstructed_np = aplicar_pca(self.original_image_np, k)
        self._mostrar_procesada(reconstructed_np)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x700")
    app = ImageProcessorApp(root)
    root.mainloop()
