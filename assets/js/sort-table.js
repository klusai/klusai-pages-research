// Minimal dependency-free column sorter for the EuroPriv-Bench leaderboard.
(function () {
  var table = document.getElementById("leaderboard");
  if (!table) return;
  var headers = table.querySelectorAll("thead th");
  var tbody = table.querySelector("tbody");

  headers.forEach(function (th, idx) {
    th.style.cursor = "pointer";
    th.addEventListener("click", function () {
      var type = th.getAttribute("data-type");
      var asc = th.getAttribute("data-asc") !== "true";
      headers.forEach(function (h) { h.removeAttribute("data-asc"); });
      th.setAttribute("data-asc", asc);

      var rows = Array.prototype.slice.call(tbody.querySelectorAll("tr"));
      rows.sort(function (a, b) {
        var x = a.children[idx].textContent.trim();
        var y = b.children[idx].textContent.trim();
        if (type === "num") {
          return (parseFloat(x) - parseFloat(y)) * (asc ? 1 : -1);
        }
        return x.localeCompare(y) * (asc ? 1 : -1);
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
    });
  });

  // Default: sort by F1 descending (best-first). Seed data-asc="true" so the
  // click toggles to descending on first load.
  var f1 = table.querySelector("thead th.f1");
  if (f1) { f1.setAttribute("data-asc", "true"); f1.click(); }
})();
