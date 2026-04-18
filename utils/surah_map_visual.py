<!-- ============================= -->
<!--   Surah Map v6 (Visual)      -->
<!--   Radial Dynamic Root Map    -->
<!--   نسخة كاملة جاهزة          -->
<!-- ============================= -->

<div id="surah-map-v6" style="padding: 10px; color: #e5e7eb; background:#020617;">
  <h3 style="margin-bottom:8px;">Surah Map v6 – الخريطة الدائرية البصرية للجذور</h3>

  <!-- Canvas (Responsive) -->
  <canvas id="surahRadialMap"
          style="width:100%; max-width:700px; aspect-ratio:1/1;
                 background:#05060a; border-radius:50%; display:block; margin:auto;">
  </canvas>

  <small style="color:#9ca3af; display:block; margin-top:8px;">
    الخريطة تستخدم نفس بيانات الجذور للسورة المختارة في النظام.
  </small>
</div>

<!-- ============================= -->
<!--   بيانات الجذور               -->
<!-- ============================= -->

<script>
  // ⚠️ استبدل هذا بالمصفوفة الحقيقية التي ينتجها النظام عندك
  window.surahRoots = [
    { root: "حمد", weight: 3 },
    { root: "ربب", weight: 2 },
    { root: "دين", weight: 1 },
    { root: "صرط", weight: 2 },
    { root: "نعم", weight: 1 }
  ];
</script>

<!-- ============================= -->
<!--   JavaScript — الرسم          -->
<!--   نسخة كاملة ديناميكية       -->
<!-- ============================= -->

<script>
(function () {
  const canvas = document.getElementById('surahRadialMap');
  if (!canvas) return;

  // 🔥 اجعل الحجم ديناميكيًا حسب عرض الشاشة
  function resizeCanvas() {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientWidth;
  }
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  const ctx = canvas.getContext('2d');

  function drawFrame(t) {
    const W = canvas.width;
    const H = canvas.height;
    const CX = W / 2;
    const CY = H / 2;

    const baseRadius = W * 0.17;
    const maxRadius = W * 0.40;

    ctx.clearRect(0, 0, W, H);

    // خلفية دائرية
    const grd = ctx.createRadialGradient(CX, CY, W * 0.05, CX, CY, maxRadius);
    grd.addColorStop(0, '#111827');
    grd.addColorStop(1, '#020617');
    ctx.fillStyle = grd;
    ctx.beginPath();
    ctx.arc(CX, CY, maxRadius, 0, 2 * Math.PI);
    ctx.fill();

    // دائرة مركزية
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = W * 0.002;
    ctx.beginPath();
    ctx.arc(CX, CY, baseRadius, 0, 2 * Math.PI);
    ctx.stroke();

    // نبض مركزي
    const pulse = (W * 0.01) * Math.sin(t / 800);
    ctx.strokeStyle = 'rgba(34,197,94,0.4)';
    ctx.beginPath();
    ctx.arc(CX, CY, baseRadius + pulse, 0, 2 * Math.PI);
    ctx.stroke();

    // قراءة الجذور
    const roots = (window.surahRoots || []).map((r, i) => ({
      root: r.root || r,
      weight: r.weight || 1,
      angle: (2 * Math.PI * i) / Math.max(1, (window.surahRoots || []).length)
    }));

    // رسم الجذور
    roots.forEach((r, idx) => {
      const dynamicRadius = baseRadius + (W * 0.08) + r.weight * (W * 0.03)
                            + (W * 0.01) * Math.sin(t / 600 + idx);

      const x = CX + dynamicRadius * Math.cos(r.angle);
      const y = CY + dynamicRadius * Math.sin(r.angle);

      // رابط
      ctx.strokeStyle = 'rgba(96,165,250,0.5)';
      ctx.lineWidth = W * 0.0015;
      ctx.beginPath();
      ctx.moveTo(CX, CY);
      ctx.lineTo(x, y);
      ctx.stroke();

      // عقدة
      const nodeRadius = (W * 0.008) + r.weight * (W * 0.002);
      ctx.fillStyle = '#f97316';
      ctx.beginPath();
      ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI);
      ctx.fill();

      // هالة
      ctx.strokeStyle = 'rgba(249,115,22,0.4)';
      ctx.beginPath();
      ctx.arc(x, y, nodeRadius + (W * 0.005) * Math.sin(t / 700 + idx), 0, 2 * Math.PI);
      ctx.stroke();

      // اسم الجذر
      ctx.fillStyle = '#e5e7eb';
      ctx.font = `${W * 0.02}px sans-serif`;
      ctx.textAlign = x >= CX ? 'left' : 'right';
      ctx.fillText(r.root, x + (x >= CX ? W * 0.015 : -W * 0.015), y - W * 0.01);
    });

    // عنوان
    ctx.fillStyle = '#a5b4fc';
    ctx.font = `${W * 0.03}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillText('الخريطة الدائرية للجذور', CX, CY - W * 0.02);
  }

  function animate(t) {
    drawFrame(t || 0);
    requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);
})();
</script>
