function makered(){
  console.log("in make red")
	document.body.style.backgroundColor = "red";
}

console.log("In javascript")

document.getElementById("makered").addEventListener("click", makered);