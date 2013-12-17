var count = 0;

/* AJAX */
function getXMLHttpObject() {
   var xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
   if(window.XMLHttpRequest) { 
	   xmlhttp = new XMLHttpRequest(); 
   }
   return xmlhttp;
}

function editTitle(element, surveyId) {
	var xmlhttp = getXMLHttpObject();
	var newTitle = element.innerHTML.replace("&nbsp;", " ");
	xmlhttp.open("POST", "/survey/edit_title/" + surveyId + "/", true);
	xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xmlhttp.send("survey_title=" + newTitle);
}

/* DOM Manipulations */
function addChoice() {
	var rList = document.getElementById("response_options");
	var listItem = document.createElement("li");
	listItem.innerHTML = "<input id=\"" + count + "\" type=\"text\" name=\"response_text\" maxlength=\"200\" />";
	rList.appendChild(listItem);
	document.getElementById(count).focus();
	count = count + 1;
}

function removeChoice() {
	var rList = document.getElementById("response_options");
	var length = rList.childNodes.length;
	if(length > 2) {
		rList.removeChild(rList.childNodes[length - 1]);
	}
}