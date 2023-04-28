document.getElementById("edit").addEventListener("click", function() {
  var fields = document.querySelectorAll("table input[type='text']");
  for (var i = 0; i < fields.length; i++) {
    fields[i].readOnly = false;
  }

  document.getElementById("save").style.display = "inline-block";
});

document.getElementById("save").addEventListener("click", function() {
  var data = {};
  data.email = document.getElementById("email").value;
  data.first_name = document.getElementById("first_name").value;
  data.last_name = document.getElementById("last_name").value;
  data.gender = document.getElementById("gender").value;
  data.age = document.getElementById("age").value;
  data.major = document.getElementById("major").value;
  window.localStorage.formData = JSON.stringify(data);
  // localStorage will not work in this snippet editor
  // uncomment it in your code

  var fields = document.querySelectorAll("table input[type='text']");
  for (var i = 0; i < fields.length; i++) {
    fields[i].readOnly = true;
  }

  document.getElementById("save").style.display = "none";
});