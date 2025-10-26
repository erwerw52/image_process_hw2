# 圖像邏輯運算應用程式

這是一個基於 Streamlit 的圖像邏輯運算工具，支援兩個圖像之間的邏輯 AND 運算和聯合運算。

## 專案結構

```
├── streamlit_app.py          # 主應用程式文件
├── image_processor.py        # 圖像處理核心模組
├── file_handler.py          # 文件處理模組
├── error_handler.py         # 錯誤處理模組
├── requirements.txt         # Python 依賴套件
├── .streamlit/
│   └── config.toml         # Streamlit 配置文件
└── README.md               # 專案說明文件
```

## 安裝和運行

### 本地運行

1. 克隆或下載專案文件
2. 安裝依賴套件：
```bash
pip install -r requirements.txt
```

3. 運行應用程式：
```bash
streamlit run app.py
```

4. 在瀏覽器中打開 `http://localhost:8501`

### Streamlit Cloud 部署

1. 將專案上傳到 GitHub 儲存庫
2. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
3. 連接您的 GitHub 帳戶
4. 選擇儲存庫和分支
5. 設置主文件為 `app.py`
6. 點擊 "Deploy" 開始部署

部署完成後，您將獲得一個公開的 URL 來訪問您的應用程式。

## 功能特色

- 支援 PNG 和 JPEG 格式圖像
- 邏輯 AND 運算
- 聯合運算（邏輯 OR）
- 圖像尺寸驗證
- 結果圖像下載
- 友善的錯誤處理

## 技術棧

- Streamlit: 網頁界面框架
- OpenCV: 圖像處理
- PIL/Pillow: 圖像格式處理
- NumPy: 數值計算

## 部署注意事項

### Streamlit Cloud 部署要求

- 確保 `requirements.txt` 包含所有必要的依賴套件
- 主應用程式文件為 `app.py`
- `.streamlit/config.toml` 配置文件已正確設置
- 圖像上傳限制設為 200MB（可在配置中調整）

### 性能優化

- 圖像會自動調整至最大 2048x2048 像素以優化處理速度
- 使用 Streamlit 快取機制減少重複計算
- 支援的圖像格式：PNG、JPEG

### 使用限制

- 最大圖像尺寸：2048x2048 像素
- 支援的文件格式：PNG (.png)、JPEG (.jpg, .jpeg)
- 不同尺寸的圖像會自動調整至較小尺寸進行運算