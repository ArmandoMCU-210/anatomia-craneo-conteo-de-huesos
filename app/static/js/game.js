(function () {
  "use strict";

  const config = window.SKULL_GAME;
  if (!config) return;

  let selectedKey = null;
  let selectedChip = null;
  let solvedCount = 0;
  let startTime = Date.now();
  let timerHandle = null;
  let finished = false;

  const feedbackEl = document.getElementById("feedback");
  const progressFill = document.getElementById("progress-fill");
  const solvedCountEl = document.getElementById("solved-count");
  const timerEl = document.getElementById("timer");
  const resultsBackdrop = document.getElementById("results-backdrop");

  function formatTime(totalSeconds) {
    const m = Math.floor(totalSeconds / 60).toString().padStart(2, "0");
    const s = Math.floor(totalSeconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  }

  function startTimer() {
    timerHandle = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      timerEl.textContent = formatTime(elapsed);
    }, 1000);
  }

  function setFeedback(message, kind) {
    feedbackEl.textContent = message;
    feedbackEl.className = "feedback" + (kind ? " " + kind : "");
  }

  function selectChip(chip) {
    if (chip.classList.contains("used")) return;
    if (selectedChip) selectedChip.classList.remove("selected");
    if (selectedChip === chip) {
      selectedChip = null;
      selectedKey = null;
      setFeedback("", "");
      return;
    }
    chip.classList.add("selected");
    selectedChip = chip;
    selectedKey = chip.dataset.key;
    setFeedback("Ahora haz clic sobre el punto del cráneo donde ubicarías ese hueso.", "");
  }

  document.querySelectorAll(".bone-chip").forEach((chip) => {
    chip.addEventListener("click", () => selectChip(chip));
  });

  function updateProgress() {
    const pct = (solvedCount / config.total) * 100;
    progressFill.style.width = pct + "%";
    solvedCountEl.textContent = solvedCount;
  }

  function markSolved(regionId, boneName) {
    const marker = document.querySelector(`.marker-group[data-region="${regionId}"]`);
    marker.classList.add("solved");
    marker.querySelector(".marker-glyph").textContent = "✓";
    marker.setAttribute("aria-label", boneName);
    marker.title = boneName;
  }

  function flashWrong(regionId) {
    const marker = document.querySelector(`.marker-group[data-region="${regionId}"]`);
    marker.classList.add("wrong-flash");
    setTimeout(() => marker.classList.remove("wrong-flash"), 550);
  }

  function handleMarkerClick(marker) {
    if (finished) return;
    if (marker.classList.contains("solved")) return;
    if (!selectedKey) {
      setFeedback("Primero selecciona un hueso del banco de palabras.", "bad");
      return;
    }
    const regionId = marker.dataset.region;

    fetch(config.answerUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ region_id: regionId, bone_key: selectedKey }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setFeedback(data.error, "bad");
          return;
        }
        if (data.correct) {
          markSolved(regionId, data.correct_bone_name);
          if (selectedChip) {
            selectedChip.classList.add("used");
            selectedChip.classList.remove("selected");
          }
          selectedChip = null;
          selectedKey = null;
          solvedCount = data.solved_count;
          updateProgress();
          setFeedback(`¡Correcto! ${data.correct_bone_name} ubicado correctamente.`, "ok");
          if (data.all_solved) {
            finishGame();
          }
        } else {
          flashWrong(regionId);
          setFeedback("Incorrecto. Ese no es el hueso de esa región, intenta con otro.", "bad");
        }
      })
      .catch(() => setFeedback("Ocurrió un error de conexión. Intenta de nuevo.", "bad"));
  }

  document.querySelectorAll(".marker-group").forEach((marker) => {
    marker.addEventListener("click", () => handleMarkerClick(marker));
  });

  function finishGame() {
    finished = true;
    clearInterval(timerHandle);
    setFeedback("¡Actividad completada! Calculando resultados…", "ok");

    fetch(config.finishUrl, { method: "POST" })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setFeedback(data.error, "bad");
          return;
        }
        renderResults(data);
      })
      .catch(() => setFeedback("No se pudo guardar el resultado. Revisa tu conexión.", "bad"));
  }

  function renderResults(data) {
    const summary = data.summary;
    document.getElementById("score-percent").textContent = summary.score_percent + "%";
    document.getElementById("score-circle").style.setProperty("--pct", summary.score_percent);
    document.getElementById("result-correct").textContent = summary.correct_count;
    document.getElementById("result-incorrect").textContent = summary.incorrect_count;
    document.getElementById("result-time").textContent = formatTime(summary.duration_seconds);

    const note = document.getElementById("attempts-note");
    note.textContent = `Has realizado esta actividad ${data.attempts_count} vez${data.attempts_count === 1 ? "" : "es"} desde tu dirección IP.`;

    const list = document.getElementById("results-list");
    list.innerHTML = "";
    data.details.forEach((d) => {
      const li = document.createElement("li");
      li.className = d.correct ? "correct" : "incorrect";
      li.innerHTML = `<span>${d.bone}</span><span>${d.correct ? "Correcto ✓" : "Incorrecto ✗"}</span>`;
      list.appendChild(li);
    });

    resultsBackdrop.hidden = false;
  }

  updateProgress();
  startTimer();
})();
