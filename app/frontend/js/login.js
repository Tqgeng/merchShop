document.getElementById("loginBtn").addEventListener("click", async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Пожалуйста, заполните все поля.");
        return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);

    const response = await fetch("/jwt/login/", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        const token = data.access_token;

        
        localStorage.setItem("token", token);

        
        window.location.href = "/frontend/dashboard.html";
    } else {
        
        const errorData = await response.json();
        console.log('Ошибка при авторизации:', errorData.detail || errorData.message);
        document.getElementById("error-message").style.display = "block";
    }
});