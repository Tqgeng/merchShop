const API_BASE = "/";
const token = localStorage.getItem("token");
const headers = {
  "Authorization": `Bearer ${token}`,
  "Content-Type": "application/json"
};

let isAdmin = false;

async function fetchUser() {
  const res = await fetch(`${API_BASE}users/me`, { headers });
  if (!res.ok) logout();
  return res.json();
}

async function fetchJwtUser() {
  const res = await fetch(`${API_BASE}jwt/users/me`, {
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  });
  if (!res.ok) throw new Error("Ошибка получения JWT-пользователя");
  return await res.json();
}

async function fetchMerch() {
  const res = await fetch(`${API_BASE}merch`, { headers });
  const items = await res.json();
  renderMerch(items);
}

function renderMerch(items) {
  const container = document.getElementById("merch-container");
  container.innerHTML = "";

  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "merch-item";

    let imgUrl = item.image_url;
    if (!imgUrl || imgUrl === "string" || !imgUrl.startsWith("http")) {
      imgUrl = "https://placehold.co/150x150?text=Нет+фото";
    }

    card.innerHTML = `
      <img src="${imgUrl}" alt="${item.name}">
      <h3>${item.name}</h3>
      <p>Цена: ${item.price} coin</p>
      <p>Остаток: ${item.quantity_available}</p>
      <button class="buy-btn" ${item.quantity_available <= 0 ? "disabled" : ""} onclick="buyMerch(${item.id})">
        ${item.quantity_available <= 0 ? "Нет в наличии" : "Купить"}
      </button>
      ${isAdmin ? `
        <button class="buy-btn" onclick="editMerch(${item.id})">Редактировать</button>
        <button class="buy-btn" onclick="deleteMerch(${item.id})">Удалить</button>
      ` : ""}
    `;
    container.appendChild(card);
  });
}

function openAdminModal() {
  document.getElementById("admin-modal").style.display = "flex";
}

async function buyMerch(id) {
  const res = await fetch(`${API_BASE}merch/purchase/`, {
    method: "POST",
    headers: {
      ...headers,
      'Content-Type': "application/json"
    },
    body: JSON.stringify({ merch_item_id: id })
  });
  if (res.ok) {
    alert("Покупка успешна");
    fetchMerch();
  } else {
    const err = await res.json();
    alert(err.detail || "Ошибка при покупке");
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

async function showProfile() {
  const user = await fetchUser();

  document.getElementById("profile-email").textContent = user.email;
  document.getElementById("profile-coins").textContent = user.coins;

  const merchList = document.getElementById("user-merch-list");
  merchList.innerHTML = "";
  user.purchased_items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = `${item.name} (${item.count})`;
    merchList.appendChild(li);
  });

  document.getElementById("profile-modal").style.display = "flex";
}

function closeModal(id) {
  document.getElementById(id).style.display = "none";
}

function openTransferModal() {
  document.getElementById("transfer-modal").style.display = "flex";
}

document.getElementById("transfer-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  data.amount = parseInt(data.amount);

  const res = await fetch(`${API_BASE}users/transfer`, {
    method: "POST",
    headers,
    body: JSON.stringify(data)
  });

  if (res.ok) {
    alert("Перевод выполнен");
    closeModal("transfer-modal");
  } else {
    const err = await res.json();
    alert(err.detail || "Ошибка перевода");
  }
});


document.getElementById("admin-add-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  data.price = parseInt(data.price);
  data.quantity_available = parseInt(data.quantity_available);

  const res = await fetch(`${API_BASE}admin/merch/`, {
    method: "POST",
    headers,
    body: JSON.stringify(data)
  });

  if (res.ok) {
    alert("Товар добавлен");
    fetchMerch();
    e.target.reset();
  } else {
    const err = await res.json();
    alert(err.detail || "Ошибка добавления товара");
  }
});

async function editMerch(id) {
  const res = await fetch(`${API_BASE}merch/`, { headers });
  if (!res.ok) {
    alert("Ошибка загрузки товара");
    return;
  }

  const items = await res.json();
  const item = items.find(m => m.id === id);
  if (!item) {
    alert("Товар не найден");
    return;
  }
  const form = document.getElementById("edit-form");

  form.id.value = item.id;
  form.name.value = item.name;
  form.description.value = item.description;
  form.price.value = item.price;
  form.quantity_available.value = item.quantity_available;
  form.image_url.value = item.image_url || "";

  document.getElementById("edit-modal").style.display = "flex";
}

document.getElementById("edit-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const id = form.id.value;

  const data = {
    name: form.name.value,
    description: form.description.value,
    price: parseInt(form.price.value),
    quantity_available: parseInt(form.quantity_available.value),
    image_url: form.image_url.value
  };

  const res = await fetch(`${API_BASE}admin/merch/${id}`, {
    method: "PATCH",
    headers,
    body: JSON.stringify(data)
  });

  if (res.ok) {
    alert("Товар обновлен");
    closeModal("edit-modal");
    fetchMerch();
  } else {
    const err = await res.json();
    alert(err.detail || "Ошибка обновления товара");
  }
});


async function deleteMerch(id) {
  if (!confirm("Вы уверены, что хотите удалить этот товар?")) return;

  const res = await fetch(`${API_BASE}admin/merch/${id}`, {
    method: "DELETE",
    headers
  });

  if (res.ok) {
    alert("Товар удален");
    fetchMerch();
  } else {
    const err = await res.json();
    alert(err.detail || "Ошибка удаления товара");
  }
}


(async function init() {
  const user = await fetchJwtUser();
  isAdmin = user.is_admin;
  if (isAdmin) {
    document.getElementById("admin-btn").style.display = "inline-block";
  }
  fetchMerch();
})();
