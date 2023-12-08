document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
  
    if (loginForm) {
      loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(loginForm);
        loginUser(formData);
      });
    }
  
    if (registerForm) {
      registerForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(registerForm);
        registerUser(formData);
      });
    }
  
    function loginUser(formData) {
      fetch("{% url 'login' %}", {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log("Login successful!", data);
        })
        .catch(error => {
          console.error("Login failed!", error);
        });
    }
  
    function registerUser(formData) {
      fetch("{% url 'register' %}", {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log("Registration successful!", data);
        })
        .catch(error => {
          console.error("Registration failed!", error);
        });
    }
  });