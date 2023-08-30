function toggleTable(tableId) {
    var table = document.getElementById(tableId);
    var otherTables = document.querySelectorAll('table:not(#' + tableId + ')');

    otherTables.forEach(function (otherTable) {
      otherTable.style.display = "none";
    });

    table.style.display = table.style.display === "none" ? "table" : "none";
  }

function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0px";
    } else {
        sidebar.style.width = "250px";
    }
}
const modeToggle = document.getElementById('mode-toggle');
const body = document.body;

function toggleMode() {
    body.classList.toggle('light-mode');
}

modeToggle.addEventListener('click', toggleMode);
function toggleLoadingOverlay(show) {
  if (show) {
    document.getElementById("loading").style.display = 'flex';
  } else {
    document.getElementById("loading").style.display = 'none';
  }
  }
function spinActivated(){
  toggleLoadingOverlay(true);}
  document.addEventListener("DOMContentLoaded", spinActivated());


