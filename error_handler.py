"""
錯誤處理模組
提供統一的錯誤處理和用戶反饋機制
"""

import streamlit as st
from typing import Optional, Any
import traceback


class ErrorHandler:
    """錯誤處理器類別，負責處理各種錯誤情況"""
    
    def __init__(self):
        """初始化錯誤處理器"""
        pass
    
    def handle_file_error(self, error_type: str, details: str = "") -> None:
        """
        處理文件相關錯誤
        
        Args:
            error_type: 錯誤類型
            details: 錯誤詳細資訊
        """
        if error_type == "不支援的格式":
            error_msg = f"""
            ❌ **不支援的文件格式**
            
            文件: {details}
            
            請上傳以下格式的圖像文件：
            - PNG (.png)
            - JPEG (.jpg, .jpeg)
            """
            st.error(error_msg)
        elif error_type == "載入失敗":
            error_msg = f"""
            ❌ **圖像載入失敗**
            
            {details}
            
            請檢查文件是否損壞或格式是否正確。
            """
            st.error(error_msg)
        else:
            st.error(f"文件錯誤: {error_type} - {details}")
    
    def handle_processing_error(self, error: Exception) -> None:
        """
        處理圖像處理錯誤
        
        Args:
            error: 異常對象
        """
        if isinstance(error, ValueError):
            if "圖像尺寸不匹配" in str(error):
                # 解析尺寸資訊
                error_str = str(error)
                if "vs" in error_str:
                    shapes = error_str.split("vs")
                    if len(shapes) == 2:
                        try:
                            # 簡化的尺寸顯示
                            st.error(f"❌ 圖像尺寸不匹配，請確保兩個圖像具有相同的尺寸。")
                        except:
                            st.error("❌ 圖像尺寸不匹配")
                else:
                    st.error("❌ 圖像尺寸不匹配")
            else:
                st.error(f"❌ 處理錯誤: {str(error)}")
        else:
            st.error(f"❌ 未預期的錯誤: {str(error)}")
            self.log_error(error, "圖像處理")
    
    def handle_dimension_error(self, img1_shape: tuple, img2_shape: tuple) -> None:
        """
        處理圖像尺寸不匹配錯誤
        
        Args:
            img1_shape: 第一個圖像的尺寸
            img2_shape: 第二個圖像的尺寸
        """
        error_msg = f"""
        ❌ **圖像尺寸不匹配**
        
        - 圖像 1 尺寸: {img1_shape[1]} x {img1_shape[0]} 像素
        - 圖像 2 尺寸: {img2_shape[1]} x {img2_shape[0]} 像素
        
        請確保兩個圖像具有相同的寬度和高度。
        """
        st.error(error_msg)
    
    def display_error_message(self, message: str, error_type: str = "error") -> None:
        """
        在UI中顯示錯誤訊息
        
        Args:
            message: 錯誤訊息
            error_type: 錯誤類型 (error, warning, info)
        """
        if error_type == "error":
            st.error(message)
        elif error_type == "warning":
            st.warning(message)
        elif error_type == "info":
            st.info(message)
        else:
            st.error(message)
    
    def display_success_message(self, message: str) -> None:
        """
        顯示成功訊息
        
        Args:
            message: 成功訊息
        """
        st.success(message)
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """
        記錄錯誤日誌
        
        Args:
            error: 異常對象
            context: 錯誤上下文
        """
        # 在開發環境中，可以打印到控制台
        error_info = f"錯誤上下文: {context}\n錯誤類型: {type(error).__name__}\n錯誤訊息: {str(error)}\n"
        print(f"[ERROR] {error_info}")
        
        # 在生產環境中，可以寫入日誌文件或發送到日誌服務
        # 這裡暫時只打印到控制台