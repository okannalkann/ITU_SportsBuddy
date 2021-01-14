
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


$(document).ready(function(){
  console.log("asdiasda");
  $('.nav-item').click(function(e){
    $(this).toggleClass("active");
    console.log("deneme",e);
    e.stopPropagation();
  })
})