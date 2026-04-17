<!-- ============================= -->
<!--   Surah Map v6 (Visual)      -->
<!--   Radial Dynamic Root Map    -->
<!--   نسخة كاملة جاهزة          -->
<!-- ============================= -->

<div id="surah-map-v6" style="padding: 10px; color: #e5e7eb; background:#020617;">
  <h3 style="margin-bottom:8px;">Surah Map v6 – الخريطة الدائرية البصرية للجذور</h3>

  <!-- Canvas -->
  <canvas id="surahRadialMap" width="700" height="700"
          style="background:#05060a; border-radius:50%; display:block; margin:auto;"></canvas>

  <small style="color:#9ca3af; display:block; margin-top:8px;">
    الخريطة تستخدم نفس بيانات الجذور للسورة المختارة في النظام.
  </small>
</div>

<!-- ============================= -->
<!--   بيانات الجذور               -->
<!--   ملاحظة: النظام عندك لديه   -->
<!--   بيانات جاهزة. فقط اربطها   -->
<!--   هنا بنفس الشكل.            -->
<!-- ============================= -->

<script>
  // ⚠️ استبدل هذا بالمصفوفة الحقيقية التي ينتجها النظام عندك
  // مثال فقط:
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
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const CX = W / 2;
  const CY = H / 2;
  const baseRadius = 120;
  const maxRadius = 280;

  // قراءة الجذور من النظام
  const roots = (window.surahRoots || []).map((r, i) => ({
    root: r.root || r,
    weight: r.weight || 1,
    angle: (2 * Math.PI * i) / Math.max(1, (window.surahRoots || []).length)
  }));

  function drawFrame(t) {
    ctx.clearRect(0, 0, W, H);

    // خلفية دائرية
    const grd = ctx.createRadialGradient(CX, CY, 50, CX, CY, maxRadius);
    grd.addColorStop(0, '#111827');
    grd.addColorStop(1, '#020617');
    ctx.fillStyle = grd;
    ctx.beginPath();
    ctx.arc(CX, CY, maxRadius, 0, 2 * Math.PI);
    ctx.fill();

    // دائرة مركزية
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.arc(CX, CY, baseRadius, 0, 2 * Math.PI);
    ctx.stroke();

    // نبض مركزي
    const pulse = 8 * Math.sin(t / 800);
    ctx.strokeStyle = 'rgba(34,197,94,0.4)';
    ctx.beginPath();
    ctx.arc(CX, CY, baseRadius + pulse, 0, 2 * Math.PI);
    ctx.stroke();

    // رسم الجذور
    roots.forEach((r, idx) => {
      const dynamicRadius = baseRadius + 60 + r.weight * 25 + 10 * Math.sin(t / 600 + idx);
      const x = CX + dynamicRadius * Math.cos(r.angle);
      const y = CY + dynamicRadius * Math.sin(r.angle);

      // رابط
      ctx.strokeStyle = 'rgba(96,165,250,0.5)';
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(CX, CY);
      ctx.lineTo(x, y);
      ctx.stroke();

      // عقدة
      const nodeRadius = 6 + r.weight * 1.5;
      ctx.fillStyle = '#f97316';
      ctx.beginPath();
      ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI);
      ctx.fill();

      // هالة
      ctx.strokeStyle = 'rgba(249,115,22,0.4)';
      ctx.beginPath();
      ctx.arc(x, y, nodeRadius + 4 * Math.sin(t / 700 + idx), 0, 2 * Math.PI);
      ctx.stroke();

      // اسم الجذر
      ctx.fillStyle = '#e5e7eb';
      ctx.font = '12px sans-serif';
      ctx.textAlign = x >= CX ? 'left' : 'right';
      ctx.fillText(r.root, x + (x >= CX ? 8 : -8), y - 4);
    });

    // عنوان
    ctx.fillStyle = '#a5b4fc';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('الخريطة الدائرية للجذور', CX, CY - 6);
  }

  function animate(t) {
    drawFrame(t || 0);
    requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);
})();
</script>