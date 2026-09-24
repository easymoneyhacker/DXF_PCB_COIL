#!/usr/bin/env python3
"""線圈 DXF 網頁：Python 3.10+，僅使用標準函式庫。

本機執行：python app.py
輸出網頁：python app.py --export dist
HTML / CSS / JavaScript 完整內嵌於 HTML 常數。
GitHub Pages 由瀏覽器計算與匯出 DXF，無須常駐 Python 伺服器。
"""
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HTML = r'''
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0c1824">
  <title>線圈 DXF 產生器</title>
  <meta name="description" content="輸入線寬、線距與內外徑，預覽平面螺旋線圈並下載可匯入 EasyEDA 的 DXF 檔。">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230c1824'/%3E%3Cpath d='M49 31c0-13-11-21-23-17C9 20 11 46 29 49c12 2 19-8 17-18-2-9-10-13-18-10-8 3-12 13-6 20 5 6 15 5 18-1 3-6-1-13-7-13-5 0-8 5-6 8' fill='none' stroke='%2336d5c0' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E">
  <style>
    :root{font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Noto Sans TC",sans-serif;color:#e9f1f4;background:#0c1824;font-synthesis:none}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(circle at 75% 10%,#173949 0,#0c1824 45%)}button,input{font:inherit}button{cursor:pointer}.shell{max-width:1400px;margin:auto;padding:24px 28px 38px}.top{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #315064;padding-bottom:20px;margin-bottom:24px}.brand{display:flex;align-items:center;gap:13px;font-size:19px;font-weight:730;letter-spacing:.02em}.mark{width:34px;height:34px;border:2px solid #38d4c1;border-radius:50%;display:grid;place-items:center;color:#38d4c1;font-size:23px;line-height:1}.tag{font-size:13px;color:#a8c2ca;letter-spacing:.08em}.workspace{display:grid;grid-template-columns:minmax(310px,405px) minmax(0,1fr);gap:24px}.panel{border:1px solid #355064;border-radius:20px;background:#112434;box-shadow:0 16px 48px #07121c55}.controls{padding:26px}.eyebrow{color:#4ae0ca;text-transform:uppercase;font-size:12px;letter-spacing:.16em;font-weight:700;margin:0 0 8px}h1{font-size:28px;line-height:1.2;margin:0 0 8px;letter-spacing:-.035em}p{margin:0}.intro{color:#aac0ca;font-size:15px;line-height:1.6;margin-bottom:27px}.section-label{font-size:14px;font-weight:700;color:#e4f0f3;margin-bottom:14px}.field-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.field{display:block}.field span{display:block;font-size:14px;color:#b8cdd4;margin-bottom:8px}.input-wrap{position:relative}.field input{width:100%;height:52px;background:#0b1c29;border:1px solid #406070;border-radius:11px;color:white;padding:0 44px 0 14px;outline:none;font-size:18px;font-variant-numeric:tabular-nums}.field input:focus{border-color:#36d5c0;box-shadow:0 0 0 3px #36d5c026}.unit{position:absolute;right:13px;top:16px;color:#93aeba;font-size:14px}.divider{height:1px;background:#304c5e;margin:24px 0}.readout{display:grid;grid-template-columns:1fr 1fr;gap:10px}.metric{padding:15px;background:#0d202d;border:1px solid #304c5e;border-radius:11px}.metric small{display:block;color:#9bb6c1;font-size:13px;margin-bottom:5px}.metric strong{font-size:20px;font-variant-numeric:tabular-nums}.download{margin-top:24px;display:flex;align-items:center;justify-content:center;gap:10px;width:100%;min-height:54px;border:0;border-radius:11px;background:#3bd7c2;color:#092630;font-size:16px;font-weight:750}.download:hover{background:#72efdc}.download:disabled{opacity:.45;cursor:not-allowed}.help{font-size:13px;color:#9eb7c0;line-height:1.55;margin-top:13px}.error{color:#ffad9e;font-size:14px;line-height:1.5;min-height:0;margin-top:12px}.error:empty{display:none}.preview{padding:20px;display:flex;flex-direction:column;min-height:670px}.preview-head{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:5px 6px 16px}.preview-head strong{font-size:16px}.preview-head span{color:#9ab9c3;font-size:13px}.drawing{position:relative;flex:1;min-height:530px;border:1px solid #365265;border-radius:14px;background-color:#0a1a26;background-image:linear-gradient(#41607024 1px,transparent 1px),linear-gradient(90deg,#41607024 1px,transparent 1px);background-size:24px 24px;overflow:hidden;display:grid;place-items:center}.drawing svg{display:block;width:min(100%,680px);height:min(100%,680px);max-height:75vh}.drawing .axis{stroke:#608b9555;stroke-width:.11;vector-effect:non-scaling-stroke}.drawing .outer-ring,.drawing .inner-ring{fill:none;stroke:#8bb9c055;stroke-width:.16;stroke-dasharray:.8 1.2}.drawing .coil{fill:none;stroke:#39d7c1;stroke-linecap:butt;stroke-linejoin:round}.legend{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:15px 6px 3px;color:#a8c0c8;font-size:13px}.legend b{color:#e8f0f2;font-weight:600}.swatch{display:inline-block;width:13px;height:3px;background:#39d7c1;vertical-align:middle;margin-right:7px}.note{max-width:1400px;margin:18px auto 0;color:#8ba9b4;font-size:13px;line-height:1.5}input::-webkit-inner-spin-button{-webkit-appearance:none}input[type=number]{appearance:textfield}@media(max-width:900px){.workspace{grid-template-columns:1fr}.preview{min-height:490px}.drawing{min-height:410px}.drawing svg{height:440px}}@media(max-width:530px){.shell{padding:17px 14px}.tag{display:none}.controls{padding:20px}.preview{padding:12px}.drawing{min-height:330px}.drawing svg{height:360px}.legend{flex-direction:column;align-items:flex-start}.field-grid{gap:10px}h1{font-size:25px}}
  </style>
</head>
<body>
  <main class="shell">
    <header class="top"><div class="brand"><div class="mark" aria-hidden="true">◎</div><span>線圈 DXF 產生器</span></div><span class="tag">EASYEDA · mm</span></header>
    <div class="workspace">
      <section class="panel controls" aria-labelledby="title">
        <p class="eyebrow">平面螺旋線圈</p><h1 id="title">設定線圈尺寸</h1><p class="intro">填入線寬、線距與直徑；右側即時預覽。匝數自動取 0.5 的倍數；內端以短導線延伸至指定開口。</p>
        <div class="section-label">導線尺寸</div>
        <div class="field-grid">
          <label class="field"><span>線寬 Line</span><div class="input-wrap"><input id="width" type="number" inputmode="decimal" min="0.05" step="0.1" value="1.5"><span class="unit">mm</span></div></label>
          <label class="field"><span>線距 Space</span><div class="input-wrap"><input id="space" type="number" inputmode="decimal" min="0.05" step="0.1" value="1.0"><span class="unit">mm</span></div></label>
        </div>
        <div class="divider"></div><div class="section-label">線圈直徑</div>
        <div class="field-grid">
          <label class="field"><span>外徑</span><div class="input-wrap"><input id="outer" type="number" inputmode="decimal" min="1" step="0.1" value="120"><span class="unit">mm</span></div></label>
          <label class="field"><span>內徑</span><div class="input-wrap"><input id="inner" type="number" inputmode="decimal" min="1" step="0.1" value="40"><span class="unit">mm</span></div></label>
        </div>
        <div class="divider"></div><div class="readout"><div class="metric"><small>自動匝數</small><strong id="turns">—</strong></div><div class="metric"><small>中心線節距</small><strong id="pitch">—</strong></div></div>
        <p class="error" id="error" role="alert"></p>
        <button class="download" id="download" type="button"><span aria-hidden="true">↓</span> 下載 DXF</button>
        <p class="help">輸出為開放式線圈線段，與 0505.dxf 一樣使用固定線寬；單位為 mm。下載後可匯入 EasyEDA。</p>
      </section>
      <section class="panel preview" aria-label="線圈即時預覽"><div class="preview-head"><strong>線圈預覽</strong><span>依實際尺寸比例繪製</span></div><div class="drawing"><svg id="drawing" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="線圈預覽"></svg></div><div class="legend"><span><i class="swatch"></i>銅線　<span id="spec">—</span></span><span>匯出格式 <b>DXF · R2000</b></span></div></section>
    </div><p class="note">圖示僅供尺寸確認；完成佈線後，請在 EasyEDA 檢查焊盤、端點連接與設計規則。</p>
  </main>
  <script>
function buildCoil(raw) {
  const width = Number(raw.width);
  const space = Number(raw.space);
  const outer = Number(raw.outer);
  const inner = Number(raw.inner);
  if (![width, space, outer, inner].every(Number.isFinite)) throw Error('請輸入有效的數字。');
  if (width <= 0 || space <= 0 || inner <= 0 || outer <= inner) throw Error('尺寸必須大於 0，且外徑需大於內徑。');
  if (outer > 1000 || width < 0.05 || space < 0.05) throw Error('請將外徑設在 1000 mm 以下、線寬與線距設在 0.05 mm 以上。');
  const pitch = width + space;
  const available = (outer - inner) / 2 - width;
  const turns = Math.floor((available / pitch + 1e-9) * 2) / 2;
  if (turns < 0.5) throw Error('內外徑之間放不下至少 0.5 匝；請加大外徑或減小內徑、線寬、線距。');
  if (turns > 100) throw Error('超過 100 匝，請調整尺寸或線距。');
  const steps = Math.round(turns * 180);
  const radiusStart = outer / 2 - width / 2;
  const radiusEnd = radiusStart - turns * pitch;
  const target = inner / 2;
  // The short inward lead makes the central opening exact while preserving
  // the specified pitch throughout the actual winding.
  const points = Array.from({ length: steps + 1 }, (_, i) => {
    const theta = -Math.PI / 2 + 2 * Math.PI * i / 180;
    const r = radiusStart - pitch * i / 180;
    return [r * Math.cos(theta), r * Math.sin(theta)];
  });
  if (radiusEnd - target > 1e-7) {
    const theta = -Math.PI / 2 + turns * 2 * Math.PI;
    points.push([target * Math.cos(theta), target * Math.sin(theta)]);
  }
  return { width, space, outer, inner, pitch, turns, points, lead: Math.max(0, radiusEnd - target) };
}

function toDXF(coil) {
  const lines = [
    '0','SECTION','2','HEADER','9','$ACADVER','1','AC1015','9','$INSUNITS','70','4','0','ENDSEC',
    '0','SECTION','2','TABLES','0','TABLE','2','LAYER','70','1','0','LAYER','2','COIL_COPPER','70','0','62','1','6','CONTINUOUS','0','ENDTAB','0','ENDSEC',
    '0','SECTION','2','BLOCKS','0','ENDSEC',
    '0','SECTION','2','ENTITIES','0','LWPOLYLINE','100','AcDbEntity','8','COIL_COPPER','100','AcDbPolyline','90',String(coil.points.length),'70','0','43',String(coil.width),
  ];
  for (const [x, y] of coil.points) lines.push('10',x.toFixed(8),'20',y.toFixed(8));
  lines.push('0','ENDSEC','0','EOF');
  return lines.join('\n') + '\n';
}

const ids = ['width','space','outer','inner'];
const fields = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
const svg = document.getElementById('drawing');
const download = document.getElementById('download');
let current = null;
function render() {
  try {
    const coil = buildCoil(Object.fromEntries(ids.map(id => [id, fields[id].value])));
    current = coil;
    document.getElementById('turns').textContent = `${coil.turns.toFixed(1)} 匝`;
    document.getElementById('pitch').textContent = `${coil.pitch.toFixed(2)} mm`;
    document.getElementById('spec').textContent = `${coil.width} / ${coil.space} mm`;
    document.getElementById('error').textContent = '';
    download.disabled = false;
    const r = coil.outer / 2;
    const extent = r + Math.max(6, r * .13);
    svg.setAttribute('viewBox', `${-extent} ${-extent} ${extent*2} ${extent*2}`);
    const path = coil.points.map(([x,y],i) => `${i?'L':'M'}${x.toFixed(4)} ${y.toFixed(4)}`).join(' ');
    svg.innerHTML = `<line class="axis" x1="${-extent}" x2="${extent}" y1="0" y2="0"/><line class="axis" x1="0" x2="0" y1="${-extent}" y2="${extent}"/><circle class="outer-ring" r="${r}"/><circle class="inner-ring" r="${coil.inner/2}"/><path class="coil" stroke-width="${coil.width}" d="${path}"/>`;
  } catch (err) {
    current = null; download.disabled = true;
    document.getElementById('error').textContent = err.message;
    document.getElementById('turns').textContent = '—';
    document.getElementById('pitch').textContent = '—';
    document.getElementById('spec').textContent = '—';
    svg.replaceChildren();
  }
}
ids.forEach(id => fields[id].addEventListener('input',render));
download.addEventListener('click',() => {
  if (!current) return;
  const blob = new Blob([toDXF(current)],{type:'application/dxf'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Coil_OD${current.outer}_ID${current.inner}_W${current.width}_S${current.space}_${current.turns}turns.dxf`;
  document.body.append(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
});
try {
  document.modelContext?.registerTool?.({
    name:'configure_coil', title:'設定線圈尺寸',
    description:'依 mm 設定線寬、線距及內外徑，並更新網頁線圈預覽與自動匝數。',
    inputSchema:{type:'object',properties:{width:{type:'number'},space:{type:'number'},outer:{type:'number'},inner:{type:'number'}},required:ids,additionalProperties:false},
    annotations:{readOnlyHint:false},
    execute(args) {
      const coil=buildCoil(args);
      ids.forEach(id=>fields[id].value=String(coil[id]));render();
      return {turns:coil.turns,pitch_mm:coil.pitch,outer_mm:coil.outer,inner_mm:coil.inner};
    }
  });
} catch (_) { /* Optional browser API. */ }
render();

</script>
</body>
</html>

'''

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?", 1)[0] not in ("/", "/index.html"):
            self.send_error(404)
            return
        data = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    parser = ArgumentParser(description="線圈 DXF 網頁伺服器與靜態匯出")
    parser.add_argument("--export", metavar="DIRECTORY", help="輸出 index.html 後結束")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.export:
        folder = Path(args.export)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(HTML, encoding="utf-8")
        (folder / ".nojekyll").touch()
        print(f"已輸出：{folder / 'index.html'}")
        return
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"開啟 http://{args.host}:{args.port} ，按 Ctrl+C 結束。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
