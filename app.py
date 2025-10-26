"""
Streamlit 主應用程式
提供圖像邏輯運算的網頁界面
"""

import streamlit as st
import numpy as np
import cv2
from typing import Optional, Tuple
from image_processor import ImageProcessor
from file_handler import FileHandler
from error_handler import ErrorHandler


class ImageLogicalOperationsApp:
    """圖像邏輯運算應用程式主類別"""
    
    def __init__(self):
        """初始化應用程式"""
        self.image_processor = ImageProcessor()
        self.file_handler = FileHandler()
        self.error_handler = ErrorHandler()
        self.setup_page_config()
        
        # 初始化會話狀態
        if 'processed_result' not in st.session_state:
            st.session_state.processed_result = None
        if 'last_operation' not in st.session_state:
            st.session_state.last_operation = None
    
    def setup_page_config(self) -> None:
        """設置頁面配置"""
        st.set_page_config(
            page_title="圖像邏輯運算工具",
            page_icon="🖼️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    def main(self) -> None:
        """主應用程式入口點"""
        self.render_header()
        
        # 上傳圖像
        img1, img2 = self.upload_images()
        
        # 顯示圖像預覽
        if img1 is not None and img2 is not None:
            # 檢查是否需要調整尺寸
            if not self.image_processor.validate_dimensions(img1, img2):
                info1 = self.image_processor.get_image_info(img1)
                info2 = self.image_processor.get_image_info(img2)
                st.info(f"📏 圖像尺寸不同，將自動調整至較小尺寸進行運算\n- 圖像1: {info1['width']}x{info1['height']}\n- 圖像2: {info2['width']}x{info2['height']}")
            
            # 運算控制
            operation_type = self.render_operation_controls()
            
            # 執行運算
            if st.button("執行運算", type="primary"):
                result = self.handle_operation(img1, img2, operation_type)
                if result is not None:
                    # 顯示結果
                    self.display_images(img1, img2, result)
                    # 下載按鈕
                    self.render_download_button(result)
        elif img1 is not None or img2 is not None:
            # 顯示已上傳的圖像
            self.display_images(img1, img2)
            
            # 提示需要上傳第二個圖像
            if img1 is not None and img2 is None:
                st.info("請上傳第二個圖像以開始運算")
            elif img1 is None and img2 is not None:
                st.info("請上傳第一個圖像以開始運算")
    
    def render_header(self) -> None:
        """渲染頁面標題和說明"""
        st.title("🖼️ 圖像邏輯運算工具")
        st.markdown("""
        這個工具可以對兩個圖像執行邏輯運算：
        - **邏輯AND運算**：只有當兩個圖像的對應像素都為白色時，結果才為白色
        - **聯合運算（OR）**：當兩個圖像的對應像素至少有一個為白色時，結果就為白色
        
        請上傳兩個圖像來開始。如果尺寸不同，系統會自動調整至較小尺寸。
        """)
        st.divider()
    
    def upload_images(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        處理圖像上傳
        
        Returns:
            兩個圖像的NumPy數組元組
        """
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("圖像 1")
            uploaded_file1 = st.file_uploader(
                "選擇第一個圖像",
                type=['png', 'jpg', 'jpeg'],
                key="image1"
            )
            
            img1 = None
            if uploaded_file1 is not None:
                if self.file_handler.validate_image_format(uploaded_file1):
                    img1 = self.file_handler.load_image_from_upload(uploaded_file1)
                    if img1 is not None:
                        # 顯示圖像資訊
                        info = self.image_processor.get_image_info(img1)
                        st.success(f"✅ 載入成功 ({info['width']}x{info['height']})")
                        
                        # 檢查圖像尺寸
                        if info['width'] > 2048 or info['height'] > 2048:
                            st.info("📏 圖像將自動調整至適當尺寸以優化處理速度")
                else:
                    self.error_handler.handle_file_error("不支援的格式", uploaded_file1.name)
        
        with col2:
            st.subheader("圖像 2")
            uploaded_file2 = st.file_uploader(
                "選擇第二個圖像",
                type=['png', 'jpg', 'jpeg'],
                key="image2"
            )
            
            img2 = None
            if uploaded_file2 is not None:
                if self.file_handler.validate_image_format(uploaded_file2):
                    img2 = self.file_handler.load_image_from_upload(uploaded_file2)
                    if img2 is not None:
                        # 顯示圖像資訊
                        info = self.image_processor.get_image_info(img2)
                        st.success(f"✅ 載入成功 ({info['width']}x{info['height']})")
                        
                        # 檢查圖像尺寸
                        if info['width'] > 2048 or info['height'] > 2048:
                            st.info("📏 圖像將自動調整至適當尺寸以優化處理速度")
                else:
                    self.error_handler.handle_file_error("不支援的格式", uploaded_file2.name)
        
        return img1, img2
    
    def display_images(self, img1: Optional[np.ndarray], img2: Optional[np.ndarray], 
                      result: Optional[np.ndarray] = None) -> None:
        """
        顯示圖像預覽
        
        Args:
            img1: 第一個圖像
            img2: 第二個圖像
            result: 結果圖像（可選）
        """
        if result is not None:
            # 顯示三個圖像：原圖1、原圖2、結果
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("原圖像 1")
                if img1 is not None:
                    # 轉換為RGB顯示
                    display_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                    st.image(display_img1, width='stretch')
            
            with col2:
                st.subheader("原圖像 2")
                if img2 is not None:
                    # 轉換為RGB顯示
                    display_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                    st.image(display_img2, width='stretch')
            
            with col3:
                st.subheader("運算結果")
                st.image(result, width='stretch')
        else:
            # 只顯示已上傳的圖像
            col1, col2 = st.columns(2)
            
            with col1:
                if img1 is not None:
                    st.subheader("圖像 1 預覽")
                    display_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                    st.image(display_img1, width='stretch')
            
            with col2:
                if img2 is not None:
                    st.subheader("圖像 2 預覽")
                    display_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                    st.image(display_img2, width='stretch')
    
    def handle_operation(self, img1: np.ndarray, img2: np.ndarray, operation_type: str) -> Optional[np.ndarray]:
        """
        處理運算執行
        
        Args:
            img1: 第一個圖像
            img2: 第二個圖像
            operation_type: 運算類型
            
        Returns:
            運算結果圖像
        """
        try:
            with st.spinner("正在處理圖像..."):
                if operation_type == "邏輯AND運算":
                    result = self.image_processor.logical_and(img1, img2)
                    self.error_handler.display_success_message("邏輯AND運算完成！")
                elif operation_type == "聯合運算（OR）":
                    result = self.image_processor.union_operation(img1, img2)
                    self.error_handler.display_success_message("聯合運算完成！")
                else:
                    st.error("未知的運算類型")
                    return None
                
                return result
                
        except ValueError as e:
            self.error_handler.handle_processing_error(e)
            return None
        except Exception as e:
            self.error_handler.handle_processing_error(e)
            return None
    
    def render_operation_controls(self) -> str:
        """
        渲染運算控制界面
        
        Returns:
            選擇的運算類型
        """
        st.subheader("選擇運算類型")
        
        operation_type = st.selectbox(
            "請選擇要執行的運算：",
            ["邏輯AND運算", "聯合運算（OR）"],
            help="邏輯AND：兩個像素都為白色時結果才為白色\n聯合運算：至少一個像素為白色時結果就為白色"
        )
        
        return operation_type
    
    def render_download_button(self, result_image: np.ndarray) -> None:
        """
        渲染下載按鈕
        
        Args:
            result_image: 要下載的結果圖像
        """
        st.subheader("下載結果")
        
        # 生成下載文件
        img_bytes = self.file_handler.save_result_image(result_image, "logical_operation_result.png")
        
        if img_bytes:
            st.download_button(
                label="📥 下載結果圖像",
                data=img_bytes,
                file_name="logical_operation_result.png",
                mime="image/png",
                type="secondary"
            )
        else:
            st.error("無法生成下載文件")


def main():
    """應用程式入口點"""
    app = ImageLogicalOperationsApp()
    app.main()


if __name__ == "__main__":
    main()