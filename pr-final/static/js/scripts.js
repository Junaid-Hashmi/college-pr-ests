$("form[name=signup_form").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      window.location.href = "/dashboard/";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });

  e.preventDefault();
});

$("form[name=login_form").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      window.location.href = "/dashboard/";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });

  e.preventDefault();
});

//------------------------------Admin---------------------------------

$("form[name=admin_signup_form").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      window.location.href = "/admin/dashboard/";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });

  e.preventDefault();
});


$("form[name=admin_login_form").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      window.location.href = "/admin/dashboard/";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });

  e.preventDefault();
});

//------------------------datatable design Bootstrap---------------------

$(document).ready(function() 
{ 
    $('#sample_data').DataTable( 
    { 
        dom: 'Blfrtip',
    } );

} );

//-------------------- delete dunction on datatable-----------------------

function del(ID, title, email){
  if (confirm("Are you sure you want to delete '" + title + "'")){
      window.location.href = '/delete/' + ID + "/" + email;
  }
}

// Password Show and Hide
// const pwdShowHide = document.querySelectorAll(".showHidePw");
// const pwFields = document.querySelectorAll(".password");
// pwdShowHide.forEach((eyeIcon) => {
//   eyeIcon.addEventListener("click", () => {
//     pwFields.forEach((pwField) => {
//       if (pwField.type === "password") {
//         pwField.type = "text";

//         pwdShowHide.forEach((icon) => {
//           icon.classList.replace("uil-eye-slash", "uil-eye");
//         });
//       } else {
//         pwField.type = "password";

//         pwdShowHide.forEach((icon) => {
//           icon.classList.replace("uil-eye", "uil-eye-slash");
//         });
//       }
//     });
//   });
// });

// Confirm Password check
// const signupBtn = document.getElementById("signup-btn");
// signupBtn.addEventListener("click", () => {
//   const pwd = document.getElementById("create-pwd").value;
//   const confirmPwd = document.getElementById("confirm-pwd").value;
//   if (pwd.length !== 0 && confirmPwd.length !== 0) {
//     if (pwd !== confirmPwd) {
//       alert("Error: Passwords don't match");
//     }
//   } else {
//     alert("Error: Password cannot be empty");
//   }
