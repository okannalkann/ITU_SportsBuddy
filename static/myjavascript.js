
function myFunction() { 
  var elmnt = document.getElementById("actiongames");
  elmnt.scrollLeft+=194;
}

function myFunction1() { 
  var elmnt = document.getElementById("actiongames1");
  elmnt.scrollLeft+=194;
}
function myFunction2() { 
  var elmnt = document.getElementById("actiongames2");
  elmnt.scrollLeft+=194;
}
function myFunction3() { 
  var elmnt = document.getElementById("actiongames3");
  elmnt.scrollLeft+=194;
}


function scrollleft() { 
  var elmnt = document.getElementById("actiongames");
  elmnt.scrollLeft-=194;
}

function scrollleft1() { 
  var elmnt = document.getElementById("actiongames1");
  elmnt.scrollLeft-=194;
}
function scrollleft2() { 
  var elmnt = document.getElementById("actiongames2");
  elmnt.scrollLeft-=194;
}
function scrollleft3() { 
  var elmnt = document.getElementById("actiongames3");
  elmnt.scrollLeft-=194;
}
 

var header = document.getElementById("navbarNavDropdown");
var btns = header.getElementsByClassName("nav-link");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
  var current = document.getElementsByClassName("active");
  current[0].className = current[0].className.replace(" active", "");
  this.className += " active";
  });
  console.log("degisti");
}