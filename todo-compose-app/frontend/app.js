const API_URL = "http://localhost:5000";

const taskInput = document.getElementById("taskInput");
const addButton = document.getElementById("addButton");
const taskList = document.getElementById("taskList");

// Récupère la liste des tâches depuis le backend et l'affiche
async function loadTasks() {
  try {
    const response = await fetch(`${API_URL}/tasks`);
    const tasks = await response.json();

    taskList.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.textContent = `#${task.id} - ${task.title}`;
      taskList.appendChild(li);
    });
  } catch (error) {
    console.error("Erreur lors du chargement des tâches :", error);
  }
}

// Envoie une nouvelle tâche au backend
async function addTask() {
  const title = taskInput.value.trim();
  if (!title) {
    return;
  }

  try {
    await fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    });

    taskInput.value = "";
    loadTasks();
  } catch (error) {
    console.error("Erreur lors de l'ajout de la tâche :", error);
  }
}

addButton.addEventListener("click", addTask);

taskInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    addTask();
  }
});

// Charger les tâches au démarrage de la page
loadTasks();