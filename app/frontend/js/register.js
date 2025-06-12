async function registerUser(email, password) {
    const response = await fetch('/jwt/register', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    if (response.ok) {
        await loginUser(email, password);
        console.log("Регистрация успешна, выполняем вход...");
    } else {
        const error = await response.json();
        console.error('Ошибка регистрации:', error.detail)
    }
}

async function loginUser(email, password) {
    const response = await fetch("/jwt/login", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            email: email,
            password: password
        })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        console.log("Вход выполнен, токен сохранён.");
        window.location.href = "/frontend/dashboard.html"; 
    } else {
        const error = await response.json();
        console.error("Ошибка входа:", error.detail);
    }
}

document.getElementById("register-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    await registerUser(email, password);
});
