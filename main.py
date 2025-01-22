# Импортируем необходимые библиотеки
from PIL import Image  
import numpy as np    
import os            

def create_folders():
    """Создание необходимых папок для проекта."""
    # Получаем полный путь к директории скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Формируем пути к папкам
    input_folder = os.path.join(script_dir, 'input_images')
    output_folder = os.path.join(script_dir, 'output_results')
    
    # Создаем папки, если их нет
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    return input_folder, output_folder

class ASCIIArtGenerator:
    # Символы ASCII от темного к светлому
    ASCII_CHARS = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
    
    def __init__(self, width=100):
        # Задаем ширину выходного изображения
        self.width = width
        # Создаем папки и сохраняем пути
        self.input_folder, self.output_folder = create_folders()
    
    def get_next_file_number(self):
        """Получение следующего номера файла."""
        # Получаем список существующих файлов в выходной папке
        existing_files = [f for f in os.listdir(self.output_folder) if f.endswith('.txt')]
        # Возвращаем следующий номер после последнего
        return len(existing_files) + 1
    
    def load_image(self, image_name):
        """Загрузка изображения из папки input_images."""
        # Формируем полный путь к файлу
        image_path = os.path.join(self.input_folder, image_name)
        # Открываем изображение
        image = Image.open(image_path)
        return image

    def resize_image(self, image):
        """Изменение размера изображения с сохранением пропорций."""
        aspect_ratio = image.height/image.width
        height = int(self.width * aspect_ratio * 0.5)
        resized_image = image.resize((self.width, height))
        return resized_image

    def convert_to_grayscale(self, image):
        """Конвертация изображения в оттенки серого."""
        return image.convert('L')

    def map_pixels_to_ascii(self, image):
        """Преобразование пикселей в ASCII символы."""
        pixels = np.array(image)
        ascii_str = ''
        pixel_range = 255
        ascii_range = len(self.ASCII_CHARS) - 1
        
        for row in pixels:
            for pixel in row:
                ascii_index = int((pixel / pixel_range) * ascii_range)
                ascii_str += self.ASCII_CHARS[ascii_index]
            ascii_str += '\n'
            
        return ascii_str

    def generate_art(self, image_name):
        """Генерация ASCII арта из изображения."""
        # Получаем следующий номер файла
        file_number = self.get_next_file_number()
        
        # Загружаем и обрабатываем изображение
        image = self.load_image(image_name)
        image = self.resize_image(image)
        grayscale_image = self.convert_to_grayscale(image)
        ascii_art = self.map_pixels_to_ascii(grayscale_image)
        
        # Формируем имя выходного файла
        base_name = os.path.splitext(image_name)[0]
        output_name = f"{file_number:03d}_{base_name}.txt"
        output_path = os.path.join(self.output_folder, output_name)
        
        # Сохраняем только ASCII-арт
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(ascii_art)
        
        print(f"[{file_number}] ASCII арт создан: {output_name}")
        return ascii_art

    def process_all_images(self):
        """Обработка всех изображений в папке."""
        # Получаем список изображений
        image_files = [f for f in os.listdir(self.input_folder) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        if not image_files:
            print(f"В папке {self.input_folder} нет изображений")
            return
        
        print(f"\nНайдено изображений: {len(image_files)}")
        print("="*50)
        
        # Обрабатываем каждое изображение
        for image_file in image_files:
            self.generate_art(image_file)
            
        print("\n" + "="*50)
        print(f"Результаты сохранены в папке: {self.output_folder}")

# Точка входа программы
if __name__ == "__main__":
    generator = ASCIIArtGenerator(width=100)
    generator.process_all_images()