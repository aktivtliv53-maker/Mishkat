# =========================================================
# 9) 🗺️ Surah Map v6 — الخريطة الدائرية (Root Engine v6.6)
#    مع إخفاء العقدة المركزية عبر CSS فقط
#    بدون fallback، بدون تجزئة، بدون حذف من JSON
# =========================================================
with tabs[8]:
    st.subheader("🗺️ Surah Map v6 — الخريطة الدائرية (Root Engine v6.6)")

    surah_number = st.number_input("اختر رقم السورة:", min_value=1, max_value=114, value=1, key="surah_map_v6_radial")

    # ============================================================
    # الربط المباشر بـ get_surah_roots_canonical - لا fallback
    # ============================================================
    currentSurahRoots = get_surah_roots_canonical(quran, surah_number)

    def is_center_node(root):
        """تحديد العقدة المركزية (مثل منن أو مكرر الحروف)"""
        if root in ["منن", "مـنـن", "م ن ن"]:
            return True
        if len(root) == 3 and root[0] == root[1] == root[2]:
            return True
        return False

    def build_roots_json(t):
        """بناء JSON للجذور - بدون حذف، فقط تصفية للعرض"""
        roots_list = []
        seen = set()
        
        for r, c in currentSurahRoots:
            # منع التكرار
            if r in seen:
                continue
            seen.add(r)
            
            color = hsv_color_for_root(r, c, t)
            layer = assign_radial_layer(c)
            letters = [L for L in r]
            domains = []
            for L in letters:
                card = get_letter_card(L)
                if card:
                    domains.append(card.get("المجال_الغالب", "عام"))
                else:
                    domains.append("عام")
            
            # إضافة علامة للعقدة المركزية لتخفيفها في CSS
            is_center = is_center_node(r)
            
            roots_list.append({
                "root": r,
                "weight": c,
                "color": color,
                "layer": layer,
                "letters": "، ".join(letters),
                "domains": "، ".join(domains[:3]),
                "isCenter": is_center
            })
        return json.dumps(roots_list)

    if not currentSurahRoots:
        st.warning("⚠️ لم يتم العثور على جذور لهذه السورة")
    else:
        # إحصاء الجذور الفريدة (للعرض فقط)
        unique_roots = []
        seen_names = set()
        for r, c in currentSurahRoots:
            if r not in seen_names and not is_center_node(r):
                seen_names.add(r)
                unique_roots.append((r, c))
        
        st.success(f"✅ {len(unique_roots)} جذراً فريداً مستخرجاً من Root Engine v6.6")

        html_code = """
        <div style="width:100%; display:flex; justify-content:center;">
          <div style="position:relative; width:100%; max-width:700px;">

            <canvas id="bgCanvas"
                    style="width:100%; aspect-ratio:1/1;
                           background:#05060a; border-radius:50%; display:block;">
            </canvas>

            <canvas id="rootCanvas"
                    style="width:100%; aspect-ratio:1/1;
                           position:absolute; top:0; left:0; pointer-events:auto;">
            </canvas>

            <div id="rootTooltip"
                 style="position:absolute; padding:6px 10px; background:rgba(15,23,42,0.95);
                        color:#e5e7eb; border-radius:6px; font-size:12px; pointer-events:none;
                        border:1px solid #4b5563; display:none; z-index:10;">
            </div>

          </div>
        </div>

        <script>
        (function () {

          const bgCanvas = document.getElementById('bgCanvas');
          const rootCanvas = document.getElementById('rootCanvas');
          const tooltip = document.getElementById('rootTooltip');

          function resize() {
            const size = bgCanvas.clientWidth;
            bgCanvas.width = size;
            bgCanvas.height = size;
            rootCanvas.width = size;
            rootCanvas.height = size;
          }
          resize();
          window.addEventListener('resize', resize);

          const bg = bgCanvas.getContext('2d');
          const ctx = rootCanvas.getContext('2d');

          let scale = 1;
          let offsetX = 0;
          let offsetY = 0;
          let isDragging = false;
          let lastX = 0;
          let lastY = 0;
          let lastTouchDistance = null;
          let hoverRoot = null;
          let baseRotation = 0;

          function drawBackground() {
            const W = bgCanvas.width;
            const CX = W / 2;
            const CY = W / 2;
            const baseRadius = W * 0.17;
            const maxRadius = W * 0.40;

            bg.clearRect(0, 0, W, W);

            const grd = bg.createRadialGradient(CX, CY, W * 0.05, CX, CY, maxRadius);
            grd.addColorStop(0, '#111827');
            grd.addColorStop(1, '#020617');
            bg.fillStyle = grd;
            bg.beginPath();
            bg.arc(CX, CY, maxRadius, 0, 2 * Math.PI);
            bg.fill();

            bg.strokeStyle = '#22c55e';
            bg.lineWidth = W * 0.002;
            bg.beginPath();
            bg.arc(CX, CY, baseRadius, 0, 2 * Math.PI);
            bg.stroke();

            bg.fillStyle = '#a5b4fc';
            bg.font = (W * 0.03) + 'px sans-serif';
            bg.textAlign = 'center';
            bg.fillText('الخريطة الدائرية للجذور — Root Engine v6.6', CX, CY - W * 0.02);
          }

          drawBackground();

          function getRoots() {
            const raw = window.surahRoots || [];
            return raw.map((r, i) => ({
              root: r.root,
              weight: r.weight,
              angle: (2 * Math.PI * i) / Math.max(1, raw.length),
              isCenter: r.isCenter || false
            }));
          }

          function screenToWorld(clientX, clientY) {
            const rect = rootCanvas.getBoundingClientRect();
            const x = (clientX - rect.left - offsetX) / scale;
            const y = (clientY - rect.top - offsetY) / scale;
            return { x, y };
          }

          function getRootAt(x, y, roots, CX, CY, baseRadius) {
            for (let i = 0; i < roots.length; i++) {
              const r = roots[i];
              // تجاهل العقدة المركزية في الـ hit detection
              if (r.isCenter) continue;
              
              const angle = r.angle + baseRotation;
              const dynamicRadius = baseRadius + 60 + r.weight * 25;
              const rx = CX + dynamicRadius * Math.cos(angle);
              const ry = CY + dynamicRadius * Math.sin(angle);
              const dist = Math.sqrt((x - rx)**2 + (y - ry)**2);
              if (dist < 20) return { r, rx, ry };
            }
            return null;
          }

          rootCanvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
          });

          rootCanvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
              offsetX += (e.clientX - lastX);
              offsetY += (e.clientY - lastY);
              lastX = e.clientX;
              lastY = e.clientY;
              tooltip.style.display = 'none';
              hoverRoot = null;
            } else {
              const { x, y } = screenToWorld(e.clientX, e.clientY);
              const W = rootCanvas.width;
              const CX = W / 2;
              const CY = W / 2;
              const baseRadius = W * 0.17;
              const roots = getRoots();
              const hit = getRootAt(x, y, roots, CX, CY, baseRadius);
              if (hit) {
                hoverRoot = hit;
                tooltip.style.display = 'block';
                tooltip.innerHTML = '<b>' + hit.r.root + '</b><br>الوزن: ' + hit.r.weight;
                tooltip.style.left = (e.clientX - rootCanvas.getBoundingClientRect().left + 10) + 'px';
                tooltip.style.top = (e.clientY - rootCanvas.getBoundingClientRect().top - 10) + 'px';
              } else {
                hoverRoot = null;
                tooltip.style.display = 'none';
              }
            }
          });

          rootCanvas.addEventListener('mouseup', () => isDragging = false);
          rootCanvas.addEventListener('mouseleave', () => isDragging = false);

          rootCanvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = -e.deltaY * 0.001;
            const oldScale = scale;
            scale += delta;
            scale = Math.max(0.4, Math.min(scale, 3));

            const rect = rootCanvas.getBoundingClientRect();
            const cx = e.clientX - rect.left;
            const cy = e.clientY - rect.top;

            offsetX = cx - (cx - offsetX) * (scale / oldScale);
            offsetY = cy - (cy - offsetY) * (scale / oldScale);
          }, { passive: false });

          rootCanvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
              isDragging = true;
              lastX = e.touches[0].clientX;
              lastY = e.touches[0].clientY;
            }
          });

          rootCanvas.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1 && isDragging) {
              const t = e.touches[0];
              offsetX += (t.clientX - lastX);
              offsetY += (t.clientY - lastY);
              lastX = t.clientX;
              lastY = t.clientY;
              tooltip.style.display = 'none';
              hoverRoot = null;
            }
          });

          rootCanvas.addEventListener('touchend', () => isDragging = false);

          function drawRoots(t) {
            const W = rootCanvas.width;
            const CX = W / 2;
            const CY = W / 2;
            const baseRadius = W * 0.17;

            ctx.setTransform(scale, 0, 0, scale, offsetX, offsetY);
            ctx.clearRect(-offsetX/scale, -offsetY/scale, W/scale, W/scale);

            baseRotation += 0.0002;

            const roots = getRoots();

            roots.forEach((r, idx) => {
              // العقدة المركزية: اجعلها شفافة تماماً
              if (r.isCenter) {
                return; // لا ترسمها إطلاقاً
              }
              
              const angle = r.angle + baseRotation;
              const dynamicRadius = baseRadius + 60 + r.weight * 25 + 10 * Math.sin(t / 600 + idx);

              const x = CX + dynamicRadius * Math.cos(angle);
              const y = CY + dynamicRadius * Math.sin(angle);

              ctx.strokeStyle = 'rgba(96,165,250,0.5)';
              ctx.lineWidth = W * 0.0015;
              ctx.beginPath();
              ctx.moveTo(CX, CY);
              ctx.lineTo(x, y);
              ctx.stroke();

              const nodeRadius = (W * 0.008) + r.weight * (W * 0.002);

              if (hoverRoot && hoverRoot.r === r) {
                ctx.fillStyle = '#facc15';
              } else {
                ctx.fillStyle = '#f97316';
              }

              ctx.beginPath();
              ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI);
              ctx.fill();

              ctx.fillStyle = '#e5e7eb';
              ctx.font = (W * 0.02) + 'px sans-serif';
              ctx.textAlign = x >= CX ? 'left' : 'right';
              ctx.fillText(r.root, x + (x >= CX ? W * 0.015 : -W * 0.015), y - W * 0.01);
            });
          }

          function animate(t) {
            drawRoots(t || 0);
            requestAnimationFrame(animate);
          }

          function updateRoots() {
            window.surahRoots = JSON.parse('""" + build_roots_json(0) + """');
          }

          updateRoots();
          setInterval(updateRoots, 800);
          requestAnimationFrame(animate);
        })();
        </script>
        """

        st.components.v1.html(html_code, height=800)
