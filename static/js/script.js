function navbtn() {
  var x = document.getElementById("navbar");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function profile() {
  var x = document.getElementById("profile");
  var y = document.getElementById("create-profile");
  if (x.style.display === "none") {
    x.style.display = "block";
    y.style.display = "none";
  }
}




function createprofile() {
  var x = document.getElementById("profile");
  var y = document.getElementById("create-profile");
  if (y.style.display === "none") {
    x.style.display = "none";
    y.style.display = "block";
  } 
}