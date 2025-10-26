"""
文件處理模組
負責圖像文件的讀取、保存和格式轉換
"""

import numpy as np
import cv2
from PIL import Image
import io
from typing import Optional, Union
import streamlit as st


class FileHandler:
    """文件處理器類別，負責圖像文件操作"""
    
    def __init__(self):
        """初始化文件處理器"""
        self.supported_formats = ['.png', '.jpg', '.jpeg']
    
    def load_image_from_upload(self, uploaded_file) -> Optional[np.ndarray]:
        """
        從Streamlit上傳組件載入圖像
        
        Args:
            uploaded_file: Streamlit UploadedFile對象
            
        Returns:
            NumPy圖像數組，如果載入失敗則返回None
        """
        if uploaded_file is None:
            return None
        
        try:
            # 讀取文件字節數據
            file_bytes = uploaded_file.read()
            
            # 使用PIL載入圖像
            pil_image = Image.open(io.BytesIO(file_bytes))
            
            # 轉換為RGB格式（如果需要）
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # 轉換為NumPy數組
            np_image = self.convert_pil_to_numpy(pil_image)
            
            # 轉換為OpenCV格式（BGR）
            cv_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
            
            return cv_image
            
        except Exception as e:
            st.error(f"載入圖像失敗: {str(e)}")
            return None
    
    def save_result_image(self, img: np.ndarray, filename: str = "result.png") -> bytes:
        """
        保存結果圖像並返回字節數據
        
        Args:
            img: 要保存的圖像數組
            filename: 文件名
            
        Returns:
            PNG格式的字節數據
        """
        try:
            # 轉換為PIL圖像
            pil_image = self.convert_numpy_to_pil(img)
            
            # 創建字節緩衝區
            img_buffer = io.BytesIO()
            
            # 保存為PNG格式
            pil_image.save(img_buffer, format='PNG')
            
            # 獲取字節數據
            img_bytes = img_buffer.getvalue()
            
            return img_bytes
            
        except Exception as e:
            st.error(f"保存圖像失敗: {str(e)}")
            return b""
    
    def validate_image_format(self, uploaded_file) -> bool:
        """
        驗證圖像格式是否支援
        
        Args:
            uploaded_file: Streamlit UploadedFile對象
            
        Returns:
            True如果格式支援，否則False
        """
        if uploaded_file is None:
            return False
        
        file_extension = '.' + uploaded_file.name.split('.')[-1].lower()
        return file_extension in self.supported_formats
    
    def get_file_info(self, uploaded_file) -> dict:
        """
        獲取上傳文件的資訊
        
        Args:
            uploaded_file: Streamlit UploadedFile對象
            
        Returns:
            包含文件資訊的字典
        """
        if uploaded_file is None:
            return {}
        
        info = {
            'name': uploaded_file.name,
            'size': uploaded_file.size,
            'type': uploaded_file.type,
            'extension': '.' + uploaded_file.name.split('.')[-1].lower()
        }
        return info
    
    def convert_pil_to_numpy(self, pil_image: Image.Image) -> np.ndarray:
        """
        將PIL圖像轉換為NumPy數組
        
        Args:
            pil_image: PIL圖像對象
            
        Returns:
            NumPy圖像數組
        """
        return np.array(pil_image)
    
    def convert_numpy_to_pil(self, np_image: np.ndarray) -> Image.Image:
        """
        將NumPy數組轉換為PIL圖像
        
        Args:
            np_image: NumPy圖像數組
            
        Returns:
            PIL圖像對象
        """
        # 如果是灰度圖像，確保格式正確
        if len(np_image.shape) == 2:
            return Image.fromarray(np_image, mode='L')
        # 如果是BGR格式，轉換為RGB
        elif len(np_image.shape) == 3 and np_image.shape[2] == 3:
            rgb_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb_image, mode='RGB')
        else:
            return Image.fromarray(np_image)