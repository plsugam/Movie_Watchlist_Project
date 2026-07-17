// =====================
// HELPER FUNCTIONS
// =====================

function showError(inputId, message) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(inputId + "-error");
    if (!input || !error) return;

    input.classList.add("input-error");
    input.classList.remove("input-success");
    error.textContent = message;
    error.classList.add("visible");
}

function showSuccess(inputId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(inputId + "-error");
    if (!input || !error) return;

    input.classList.remove("input-error");
    input.classList.add("input-success");
    error.textContent = "";
    error.classList.remove("visible");
}

function clearValidation(inputId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(inputId + "-error");
    if (!input || !error) return;

    input.classList.remove("input-error", "input-success");
    error.textContent = "";
    error.classList.remove("visible");
}

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// =====================
// LOGIN FORM
// =====================

const loginForm = document.getElementById("login-form");
if (loginForm) {
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let isValid = true;

        const email = document.getElementById("email").value.trim();
        if (email === "") {
            showError("email", "Email is required.");
            isValid = false;
        } else if (!emailPattern.test(email)) {
            showError("email", "Please enter a valid email address.");
            isValid = false;
        } else {
            showSuccess("email");
        }

        const password = document.getElementById("password").value;
        if (password === "") {
            showError("password", "Password is required.");
            isValid = false;
        } else {
            showSuccess("password");
        }

        if (isValid) {
            loginForm.submit();
        }
    });

    // Real-time: clear error once email looks valid
    document.getElementById("email").addEventListener("input", function() {
        const email = this.value.trim();
        if (email === "") {
            clearValidation("email");
        } else if (emailPattern.test(email)) {
            showSuccess("email");
        }
    });

    // Real-time: clear password error once something is typed
    document.getElementById("password").addEventListener("input", function() {
        if (this.value.length > 0) {
            showSuccess("password");
        } else {
            clearValidation("password");
        }
    });
}

// =====================
// REGISTER FORM
// =====================

const registerForm = document.getElementById("register-form");
if (registerForm) {
    registerForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let isValid = true;

        // Name
        const name = document.getElementById("name").value.trim();
        if (name === "") {
            showError("name", "Full name is required.");
            isValid = false;
        } else if (name.length > 100) {
            showError("name", "Name must be under 100 characters.");
            isValid = false;
        } else {
            showSuccess("name");
        }

        // Email
        const email = document.getElementById("email").value.trim();
        if (email === "") {
            showError("email", "Email is required.");
            isValid = false;
        } else if (!emailPattern.test(email)) {
            showError("email", "Please enter a valid email address.");
            isValid = false;
        } else {
            showSuccess("email");
        }

        // Password
        const password = document.getElementById("password").value;
        if (password === "") {
            showError("password", "Password is required.");
            isValid = false;
        } else if (password.length < 6) {
            showError("password", "Password must be at least 6 characters.");
            isValid = false;
        } else if (password.length > 200) {
            showError("password", "Password is too long.");
            isValid = false;
        } else {
            showSuccess("password");
        }

        if (isValid) {
            registerForm.submit();
        }
    });

    // Real-time feedback
    document.getElementById("name").addEventListener("blur", function() {
        const name = this.value.trim();
        if (name !== "" && name.length < 2) {
            showError("name", "Name is too short.");
        } else if (name !== "") {
            showSuccess("name");
        }
    });

    document.getElementById("email").addEventListener("input", function() {
        const email = this.value.trim();
        if (email === "") {
            clearValidation("email");
        } else if (emailPattern.test(email)) {
            showSuccess("email");
        }
    });

    document.getElementById("password").addEventListener("input", function() {
        const password = this.value;
        if (password === "") {
            clearValidation("password");
        } else if (password.length < 6) {
            showError("password", "Password must be at least 6 characters.");
        } else {
            showSuccess("password");
        }
    });
}

// =====================
// ADD TITLE FORM
// =====================

const addForm = document.getElementById("add-form");
if (addForm) {
    addForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let isValid = true;

        // Title
        const title = document.getElementById("title").value.trim();
        if (title === "") {
            showError("title", "Title is required.");
            isValid = false;
        } else if (title.length > 200) {
            showError("title", "Title must be under 200 characters.");
            isValid = false;
        } else {
            showSuccess("title");
        }

        // Type
        const type = document.getElementById("type").value;
        if (type === "") {
            showError("type", "Please select a type.");
            isValid = false;
        } else {
            showSuccess("type");
        }

        // Year (optional but validated if filled)
        const year = document.getElementById("year").value.trim();
        if (year !== "") {
            const yearNum = parseInt(year);
            if (isNaN(yearNum) || yearNum < 1900 || yearNum > 2030) {
                showError("year", "Enter a valid year between 1900 and 2030.");
                isValid = false;
            } else {
                showSuccess("year");
            }
        }

        // Rating (optional but validated if filled)
        const rating = document.getElementById("rating").value.trim();
        if (rating !== "") {
            const ratingNum = parseInt(rating);
            if (isNaN(ratingNum) || ratingNum < 1 || ratingNum > 5) {
                showError("rating", "Rating must be between 1 and 5.");
                isValid = false;
            } else {
                showSuccess("rating");
            }
        }

        if (isValid) {
            addForm.submit();
        }
    });

    // Real-time title feedback
    document.getElementById("title").addEventListener("input", function() {
        if (this.value.trim() !== "") {
            showSuccess("title");
        } else {
            clearValidation("title");
        }
    });
}
