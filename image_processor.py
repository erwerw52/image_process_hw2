"""
圖像處理核心模組
提供邏輯AND運算和聯合運算功能
"""

import numpy as np
import cv2
from typing import Tuple, Optional


class ImageProcessor:
    """圖像處理器類別，負責執行邏輯運算"""
    
    def __init__(self):
        """初始化圖像處理器"""
        self.max_dimension = 2048  # 最大尺寸限制
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def logical_and(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        執行邏輯AND運算
        
        Args:
            img1: 第一個輸入圖像
            img2: 第二個輸入圖像
            
        Returns:
            運算結果圖像
        """
        # 自動調整圖像尺寸以匹配
        img1, img2 = self.resize_to_match(img1, img2)
        
        # 優化記憶體使用
        img1 = self.optimize_memory_usage(img1)
        img2 = self.optimize_memory_usage(img2)
        
        # 轉換為二進制圖像
        binary1 = self.convert_to_binary(img1)
        binary2 = self.convert_to_binary(img2)
        
        # 執行邏輯AND運算
        result = cv2.bitwise_and(binary1, binary2)
        
        return result
    
    def union_operation(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        執行聯合運算（邏輯OR）
        
        Args:
            img1: 第一個輸入圖像
            img2: 第二個輸入圖像
            
        Returns:
            運算結果圖像
        """
        # 自動調整圖像尺寸以匹配
        img1, img2 = self.resize_to_match(img1, img2)
        
        # 優化記憶體使用
        img1 = self.optimize_memory_usage(img1)
        img2 = self.optimize_memory_usage(img2)
        
        # 轉換為二進制圖像
        binary1 = self.convert_to_binary(img1)
        binary2 = self.convert_to_binary(img2)
        
        # 執行邏輯OR運算
        result = cv2.bitwise_or(binary1, binary2)
        
        return result
    
    def validate_dimensions(self, img1: np.ndarray, img2: np.ndarray) -> bool:
        """
        驗證圖像尺寸是否相同
        
        Args:
            img1: 第一個圖像
            img2: 第二個圖像
            
        Returns:
            True如果尺寸相同，否則False
        """
        return img1.shape == img2.shape
    
    def convert_to_binary(self, img: np.ndarray) -> np.ndarray:
        """
        將圖像轉換為二進制格式
        
        Args:
            img: 輸入圖像
            
        Returns:
            二進制圖像（像素值為0或255）
        """
        # 如果是彩色圖像，先轉為灰度
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()
        
        # 使用閾值轉換為二進制圖像
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return binary
    
    def get_image_info(self, img: np.ndarray) -> dict:
        """
        獲取圖像資訊
        
        Args:
            img: 輸入圖像
            
        Returns:
            包含尺寸和其他資訊的字典
        """
        info = {
            'shape': img.shape,
            'height': img.shape[0],
            'width': img.shape[1],
            'channels': len(img.shape) if len(img.shape) == 2 else img.shape[2],
            'dtype': str(img.dtype),
            'size': img.size
        }
        return info
    
    def resize_if_needed(self, img: np.ndarray) -> np.ndarray:
        """
        如果圖像過大則調整尺寸
        
        Args:
            img: 輸入圖像
            
        Returns:
            調整後的圖像
        """
        height, width = img.shape[:2]
        
        if height > self.max_dimension or width > self.max_dimension:
            # 計算縮放比例
            scale = min(self.max_dimension / height, self.max_dimension / width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # 調整尺寸
            resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            return resized
        
        return img
    
    def optimize_memory_usage(self, img: np.ndarray) -> np.ndarray:
        """
        優化記憶體使用
        
        Args:
            img: 輸入圖像
            
        Returns:
            優化後的圖像
        """
        # 調整尺寸
        img = self.resize_if_needed(img)
        
        # 確保數據類型為uint8以節省記憶體
        if img.dtype != np.uint8:
            img = img.astype(np.uint8)
        
        return img
    
    def resize_to_match(self, img1: np.ndarray, img2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        將兩個圖像調整為相同尺寸
        
        Args:
            img1: 第一個圖像
            img2: 第二個圖像
            
        Returns:
            調整後的兩個圖像元組
        """
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        # 如果尺寸已經相同，直接返回
        if h1 == h2 and w1 == w2:
            return img1, img2
        
        # 選擇較小的尺寸作為目標尺寸（保持品質）
        target_height = min(h1, h2)
        target_width = min(w1, w2)
        
        # 調整兩個圖像到相同尺寸
        resized_img1 = cv2.resize(img1, (target_width, target_height), interpolation=cv2.INTER_AREA)
        resized_img2 = cv2.resize(img2, (target_width, target_height), interpolation=cv2.INTER_AREA)
        
        return resized_img1, resized_img2