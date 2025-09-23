<<<<<<< HEAD
=======
// impede seleção duplicada de valores
>>>>>>> 41e954fada5d3360a5540019e9f442d1d1acfa30
document.addEventListener("DOMContentLoaded", function () {
  const selects = Array.from(document.querySelectorAll(".val-select"));

  function updateOptions() {
    const chosen = selects.map(s => s.value).filter(v => v);
    selects.forEach(s => {
      Array.from(s.options).forEach(opt => {
        if (opt.value === "") return;
        const usedElsewhere = chosen.includes(opt.value) && s.value !== opt.value;
        opt.disabled = usedElsewhere;
      });
    });
  }

  selects.forEach(s => {
    s.addEventListener("change", updateOptions);
  });
});
