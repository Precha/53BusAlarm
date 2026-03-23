# 53 Metro Alarm

這個項目提供檢查阿姆斯特丹捷運53線從Weesperplein到Diemen Zuid的下一班車到站時間。

## 在桌面運行（Python腳本）

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 設置Google Maps API

1. 前往 [Google Cloud Console](https://console.developers.google.com/)
2. 創建一個新項目或選擇現有項目
3. 啟用 Directions API
4. 創建一個API密鑰
5. 設置環境變數：

```bash
export GOOGLE_MAPS_API_KEY=your_api_key_here
```

### 運行

```bash
python main.py
```

## 在iPhone上運行（Web應用）

### 選項1：本地服務器（推薦）

1. 獲取Google Maps API密鑰（如上所述）
2. 設置環境變數：

```bash
export GOOGLE_MAPS_API_KEY=your_api_key_here
```

3. 運行本地服務器：

```bash
python server.py
```

4. 在同一網絡的iPhone上，打開Safari並訪問`http://你的電腦IP:8000`
5. 當你到達Weesperplein站時，點擊"檢查下一班車"按鈕

> 這樣可以避免瀏覽器跨域（CORS）限制，因為前端用`/directions`向本機代理發請求，代理再向Google API查數據。

### 選項2：上傳到web服務器

1. 獲取Google Maps API密鑰
2. 在`index.html`中替換API密鑰
3. 將`index.html`上傳到任何web服務器（如GitHub Pages）
4. 在iPhone的Safari中打開URL

注意：Google Maps API可能有使用限制和費用。請檢查Google的定價。