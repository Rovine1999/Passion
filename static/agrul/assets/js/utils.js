
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const getFormErrorHolders = (form_id, target) => {
  if (target === 0) {
    return `#${form_id} #msgSubmit`
  }
  return `#${form_id} #msgSubmitErrors`
}

const spinner = () => {
  return `
        <div class="d-flex align-items-center justify-content-center flex-column py-2">
          <div class="spinner-border ml-auto mb-2" role="status" aria-hidden="true"></div>
          <strong>Loading...</strong>
        </div>
  `
}

function removeNonAlphanumericCharacters(str) {
  return str.replace(/[^a-z0-9]+/gi, "");
}

function makeToastrNotifications() {
  toastr.options = {
    positionClass: "toast-bottom-right",
    progressBar: true,
    timeOut: 60000
  }
  for (const field in errors) {
    if (errors.hasOwnProperty(field)) {
      const errorMessages = errors[field].join('<br>');
      toastr.error(`${field}: ${errorMessages}`);
    }
  }
}

function attachPasswordChangeListeners() {
  // Find all input elements with type 'password' using jQuery
  const passwordInputs = $('input[type="password"]');

  // Loop over each password input and attach an input listener
  passwordInputs.each(function () {
    $(this).on('input', function () {
      // Get the input's value
      let password = $(this).val();
      // Check if the password meets the security requirements
      if (password.length >= 8) {
        if (testPassword(password)) {
          toastr.success('Password is secure!');
        }
      }
    });
  });
  passwordInputs.each(function () {
    $(this).on('change', function () {
      // Get the input's value
      let password = $(this).val();
      // Check if the password meets the security requirements
      if (password.length < 8) {
        toastr.warning('Password must be atleast 8 characters long!');
      }
    });
  });
}

function testPassword(password) {
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/.test(password)
}

attachPasswordChangeListeners()

function displayToastrErrors(errors, parentKey = null) {
  toastr.options = {
    positionClass: "toast-bottom-right",
    progressBar: true,
    timeOut: 60000
  }
  for (const field in errors) {
    if (errors.hasOwnProperty(field)) {
      const key = parentKey ? `${parentKey}.${field}` : field;
      const value = errors[field];

      if (Array.isArray(value)) {
        const errorMessages = value.join('<br>');
        toastr.error(`${key}: ${errorMessages}`);
      }
      else {
        displayToastrErrors(value, key);
      }
    }
  }
}
