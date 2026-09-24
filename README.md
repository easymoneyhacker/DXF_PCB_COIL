# 線圈 DXF 產生器

Python 整合 HTML、CSS、JavaScript 的單檔網頁。輸入線寬、線距、內外徑，即時預覽並下載 DXF。只需 Python 3.10 以上，無須 pip 安裝套件。

## 本機執行

在此資料夾開啟終端機：

```bash
python app.py
```

瀏覽器開啟 http://127.0.0.1:8000 。macOS 若沒有 `python` 指令，改用 `python3`。按 Ctrl+C 結束。

## 部署到 GitHub Pages

GitHub Pages 提供靜態網頁，不執行常駐 Python 後端。本專案由 GitHub Actions 執行 Python 產生完整 HTML，訪客的瀏覽器負責預覽與 DXF 下載。

1. 在 GitHub 建立一個儲存庫，例如 `coil-dxf-generator`。
2. 將解壓縮資料夾內的檔案上傳到儲存庫根目錄，包含 `.github/workflows/pages.yml`。不要只上傳 ZIP，也不要多包一層資料夾。若看不到 `.github`，請啟用顯示隱藏檔。
3. 分支使用 `main`；若你的分支名稱不同，請修改 `pages.yml` 的 `branches`。
4. 到儲存庫 **Settings → Pages → Build and deployment → Source**，選擇 **GitHub Actions**。
5. 到 **Actions → Deploy coil generator to GitHub Pages → Run workflow** 執行。之後每次推送到 `main` 都會自動更新。
6. 完成後，在工作流程的部署結果或 Settings → Pages 取得網址。一般專案網址為 `https://你的帳號.github.io/coil-dxf-generator/`。

GitHub Pages 的可用性依儲存庫可見性與帳號方案而定。

官方文件：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## 檔案說明

| 檔案 | 用途 |
| --- | --- |
| `app.py` | 主程式；`HTML` 常數內含完整網頁，可直接修改 |
| `.github/workflows/pages.yml` | 自動產生及部署網頁 |
| `README.md` | 執行及部署說明 |

可手動輸出單一 HTML：

```bash
python app.py --export dist
```

產生的 `dist/index.html` 內嵌所有程式，可直接用瀏覽器開啟。修改網頁時以 `app.py` 為準，再重新輸出。

## 幾何與 DXF

- 預設：線寬 1.5 mm、線距 1.0 mm、外徑 120 mm、中心開口 40 mm。
- 使用等節距阿基米德螺旋，節距為線寬 + 線距。線距為名義徑向間距，曲線法向最短間距可能略有差異。
- 匝數自動向下取 0.5 的倍數；預設為 15 匝。
- 當匝數限制使螺旋本身無法恰好符合內徑時，內端增加徑向短導線至指定開口。預設為 1.75 mm 的導線；此導線不計入匝數。
- 外徑指以螺旋中心為圓心的外接圓名義直徑，並非左右或上下包圍框尺寸；中心開口以內端導線邊界定義。
- DXF 為 R2000 / AC1015、mm 單位、COIL_COPPER 圖層，一條未封閉 LWPOLYLINE，固定線寬。無填色圖元。
- 曲線以每匝 180 段近似，最大 100 匝。尺寸為名義設計值，端點與離散線段可能產生細微偏差。
- 匯入 EasyEDA 後請確認 mm 單位、銅層與線寬，並完成焊盤及 DRC；本程式未直接輸出 Gerber。

## 驗證範圍

已確認 Python 匯出流程、內嵌 JavaScript 語法，以及預設參數輸出的 DXF 可由 ezdxf 解析。未替你的 GitHub 儲存庫執行部署，也未在 EasyEDA 內實際匯入測試。
