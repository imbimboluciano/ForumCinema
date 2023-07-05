function showDiv() {
   
    var x = document.getElementById("myDIV");
    if (x.classList.contains("d-none")) {
      x.classList.remove("d-none")
      x.classList.add("d-flex")
    } else {
      x.classList.remove("d-flex")
      x.classList.add("d-none")
    }
} 