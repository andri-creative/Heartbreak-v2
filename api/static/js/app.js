/**
 * Heartbreak AI V2 — Interactive Frontend Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const form = document.getElementById("heartbreak-form");
  const btnSubmit = document.getElementById("btn-submit");
  const btnText = btnSubmit.querySelector(".btn-text");
  const spinner = btnSubmit.querySelector(".spinner");

  // Inputs
  const inputNama = document.getElementById("nama");
  const inputUmur = document.getElementById("umur");
  const selectJK = document.getElementById("jenis_kelamin");
  const selectPend = document.getElementById("pendidikan");
  const inputHubNilai = document.getElementById("lama_hubungan_nilai");
  const selectHubSatuan = document.getElementById("lama_hubungan_satuan");
  const inputPutusNilai = document.getElementById("sejak_putus_nilai");
  const selectPutusSatuan = document.getElementById("sejak_putus_satuan");

  // Helpers
  const helperHub = document.getElementById("helper-hubungan");
  const helperPutus = document.getElementById("helper-putus");

  // Views
  const placeholderView = document.getElementById("placeholder-view");
  const resultsView = document.getElementById("results-view");

  // Duration Helper Calculation
  function updateDurationHelpers() {
    const hubVal = parseFloat(inputHubNilai.value) || 0;
    const hubUnit = selectHubSatuan.value;
    const putusVal = parseFloat(inputPutusNilai.value) || 0;
    const putusUnit = selectPutusSatuan.value;

    const unitFactors = { hari: 1 / 30, minggu: 1 / 4, bulan: 1, tahun: 12 };

    const hubBulan = hubVal * (unitFactors[hubUnit] || 1);
    const putusBulan = putusVal * (unitFactors[putusUnit] || 1);
    const ratio = putusBulan / (hubBulan + 1e-5);

    if (hubVal > 0) {
      helperHub.textContent = `~ Estimasi: ${hubBulan.toFixed(1)} bulan`;
    } else {
      helperHub.textContent = `~ Estimasi: 0 bulan`;
    }

    if (putusVal > 0 && hubVal > 0) {
      helperPutus.textContent = `~ Estimasi: ${putusBulan.toFixed(1)} bulan (Rasio Pemulihan: ${ratio.toFixed(3)})`;
    } else if (putusVal > 0) {
      helperPutus.textContent = `~ Estimasi: ${putusBulan.toFixed(1)} bulan`;
    } else {
      helperPutus.textContent = `~ Estimasi: 0 bulan`;
    }
  }

  [inputHubNilai, selectHubSatuan, inputPutusNilai, selectPutusSatuan].forEach((el) => {
    el.addEventListener("input", updateDurationHelpers);
    el.addEventListener("change", updateDurationHelpers);
  });

  // Presets Handlers
  document.getElementById("preset-akut").addEventListener("click", () => {
    inputNama.value = "Dimas Anggara";
    inputUmur.value = "22";
    selectJK.value = "Laki-laki";
    selectPend.value = "S1";
    inputHubNilai.value = "5";
    selectHubSatuan.value = "tahun";
    inputPutusNilai.value = "2";
    selectPutusSatuan.value = "hari";

    updateDurationHelpers();
    form.dispatchEvent(new Event("submit"));
  });

  document.getElementById("preset-sedang").addEventListener("click", () => {
    inputNama.value = "Budi Pratama";
    inputUmur.value = "23";
    selectJK.value = "Laki-laki";
    selectPend.value = "S1";
    inputHubNilai.value = "2";
    selectHubSatuan.value = "tahun";
    inputPutusNilai.value = "2";
    selectPutusSatuan.value = "bulan";

    updateDurationHelpers();
    form.dispatchEvent(new Event("submit"));
  });

  document.getElementById("preset-ringan").addEventListener("click", () => {
    inputNama.value = "Rian Ardiansyah";
    inputUmur.value = "25";
    selectJK.value = "Laki-laki";
    selectPend.value = "S1";
    inputHubNilai.value = "2";
    selectHubSatuan.value = "tahun";
    inputPutusNilai.value = "2";
    selectPutusSatuan.value = "tahun";

    updateDurationHelpers();
    form.dispatchEvent(new Event("submit"));
  });

  // Form Submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      nama: inputNama.value.trim(),
      umur: parseFloat(inputUmur.value),
      jenis_kelamin: selectJK.value || "Laki-laki",
      pendidikan: selectPend.value || "S1",
      lama_hubungan_nilai: parseFloat(inputHubNilai.value),
      lama_hubungan_satuan: selectHubSatuan.value,
      sejak_putus_nilai: parseFloat(inputPutusNilai.value),
      sejak_putus_satuan: selectPutusSatuan.value,
      siapa_mengakhiri: null,
      masih_komunikasi: null,
      frekuensi_medsos: null,
    };

    // Loading State
    btnText.style.display = "none";
    spinner.style.display = "inline-flex";
    btnSubmit.disabled = true;

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const json = await response.json();

      if (!response.ok) {
        throw new Error(json.detail || "Terjadi kesalahan pada sistem.");
      }

      if (json.success && json.data) {
        renderResults(json.data);
      }
    } catch (err) {
      alert("❌ Gagal menganalisis: " + err.message);
    } finally {
      btnText.style.display = "inline-flex";
      spinner.style.display = "none";
      btnSubmit.disabled = false;
    }
  });

  // Render Result Function
  function renderResults(data) {
    placeholderView.style.display = "none";
    resultsView.style.display = "block";

    // 1. Banner Severity
    const banner = document.getElementById("banner-severity");
    const badgeIcon = document.getElementById("badge-icon");
    const labelSev = document.getElementById("result-severity-label");
    const descSev = document.getElementById("result-status-desc");

    banner.className = "severity-banner " + data.kategori_severity.toLowerCase();
    badgeIcon.textContent = data.badge;
    labelSev.textContent = data.kategori_severity.toUpperCase();
    descSev.textContent = data.deskripsi_status;

    // 2. Metrics & Progress Bars
    document.getElementById("metric-distres").textContent = data.probabilitas_distres + "%";
    document.getElementById("bar-distres").style.width = data.probabilitas_distres + "%";

    document.getElementById("metric-kestabilan").textContent = data.probabilitas_ringan + "%";
    document.getElementById("bar-kestabilan").style.width = data.probabilitas_ringan + "%";

    // 3. Duration Summary
    document.getElementById("info-dur-hubungan").textContent =
      `${data.detail_durasi.durasi_hubungan_bulan} Bulan (${data.detail_durasi.kategori_lama_hubungan})`;
    document.getElementById("info-dur-putus").textContent =
      `${data.detail_durasi.durasi_putus_bulan} Bulan (${data.detail_durasi.kategori_sejak_putus})`;
    document.getElementById("info-recovery-ratio").textContent =
      data.detail_durasi.rasio_pemulihan.toFixed(4);

    // 4. AI Coach Insights
    const insight = data.ai_psychologist_insight;
    document.getElementById("coach-headline").textContent = `"${insight.headline_empati}"`;
    document.getElementById("coach-analysis").innerHTML = insight.analisis_kondisi.replace(/\n\n/g, "<br><br>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    document.getElementById("coach-affirmation").textContent = insight.afirmasi_harian;

    const warningBox = document.getElementById("coach-warning");
    const warningText = document.getElementById("coach-warning-text");
    if (insight.peringatan_psikologis) {
      warningText.textContent = insight.peringatan_psikologis;
      warningBox.style.display = "flex";
    } else {
      warningBox.style.display = "none";
    }

    // 5. Recovery Checklist
    const checklistContainer = document.getElementById("recovery-checklist");
    checklistContainer.innerHTML = "";
    insight.langkah_pemulihan_personal.forEach((step) => {
      const item = document.createElement("div");
      item.className = "check-item";
      item.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>${step.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")}</span>`;
      checklistContainer.appendChild(item);
    });

    // Reset Chat Box
    document.getElementById("curhat-response-box").style.display = "none";
    document.getElementById("user-curhat-text").value = "";

    // Smooth Scroll to result if on mobile
    if (window.innerWidth < 960) {
      resultsView.scrollIntoView({ behavior: "smooth" });
    }
  }

  // Curhat Counselor Handler
  const btnSendCurhat = document.getElementById("btn-send-curhat");
  const userCurhatText = document.getElementById("user-curhat-text");
  const curhatResponseBox = document.getElementById("curhat-response-box");
  const curhatResponseText = document.getElementById("curhat-response-text");

  btnSendCurhat.addEventListener("click", async () => {
    const text = userCurhatText.value.trim();
    if (!text) {
      alert("Silakan tuliskan apa yang sedang kamu rasakan terlebih dahulu.");
      return;
    }

    btnSendCurhat.disabled = true;
    btnSendCurhat.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Menjawab AI...`;

    try {
      const payload = {
        prediction_context: {
          nama: inputNama.value.trim() || "Sahabat",
          umur: parseFloat(inputUmur.value) || 22,
          jenis_kelamin: selectJK.value || "Laki-laki",
          pendidikan: selectPend.value || "S1",
          lama_hubungan_nilai: parseFloat(inputHubNilai.value) || 1,
          lama_hubungan_satuan: selectHubSatuan.value,
          sejak_putus_nilai: parseFloat(inputPutusNilai.value) || 1,
          sejak_putus_satuan: selectPutusSatuan.value,
          siapa_mengakhiri: null,
          masih_komunikasi: null,
          frekuensi_medsos: null,
        },
        user_curhat: text,
      };

      const res = await fetch("/api/counsel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const json = await res.json();
      curhatResponseBox.style.display = "block";
      
      const formattedAnalysis = json.analisis_kondisi.replace(/\n\n/g, "<br><br>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
      
      let stepsHtml = "";
      if (json.langkah_pemulihan_personal && json.langkah_pemulihan_personal.length > 0) {
        stepsHtml = "<div style='margin-top:12px;'><strong>Saran Langkah Konkret:</strong><ul style='padding-left:18px; margin-top:6px; font-size:12.5px;'>" +
          json.langkah_pemulihan_personal.map(s => `<li style='margin-bottom:4px;'>${s.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")}</li>`).join("") +
          "</ul></div>";
      }

      curhatResponseText.innerHTML = `
        <h5 style="color:#e0e7ff; font-size:14px; font-weight:700; margin-bottom:8px;">${json.headline_empati}</h5>
        <div style="font-size:13px; line-height:1.6; color:#cbd5e1;">${formattedAnalysis}</div>
        ${stepsHtml}
        <div style="margin-top:12px; font-style:italic; color:#a5b4fc; border-left:3px solid #818cf8; padding-left:10px;">
          ${json.afirmasi_harian}
        </div>
      `;
    } catch (err) {
      alert("Gagal mengirim curhat: " + err.message);
    } finally {
      btnSendCurhat.disabled = false;
      btnSendCurhat.innerHTML = `<i class="fa-solid fa-paper-plane"></i> Konsultasikan`;
    }
  });

  // Initial update
  updateDurationHelpers();
});
