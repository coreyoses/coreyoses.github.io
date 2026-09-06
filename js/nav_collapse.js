/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function collapseNav() {
    var x = document.getElementById("nL");
    if (x.className === "navList") {
        x.className += " responsive";
    } else {
        x.className = "navList";
    }
}
