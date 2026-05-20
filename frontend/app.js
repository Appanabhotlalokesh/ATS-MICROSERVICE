const API_BASE = "http://localhost:3000/local";
const jobList = document.getElementById("jobList");
const jobStatus = document.getElementById("jobStatus");
const refreshJobs = document.getElementById("refreshJobs");
const candidateForm = document.getElementById("candidateForm");
const formMessage = document.getElementById("formMessage");

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let body;

  try {
    body = text ? JSON.parse(text) : {};
  } catch (error) {
    throw new Error("Invalid JSON response from server.");
  }

  if (!response.ok) {
    const message = body.error || response.statusText || "Request failed.";
    throw new Error(message);
  }

  return body;
}

function setStatus(message) {
  jobStatus.textContent = message;
}

function renderJobs(jobs) {
  jobList.innerHTML = "";

  if (!jobs.length) {
    jobList.innerHTML = "<li class=\"job-card\">No open jobs found.</li>";
    return;
  }

  jobs.forEach((job) => {
    const item = document.createElement("li");
    item.className = "job-card";
    item.innerHTML = `
      <h3>${job.title || "Untitled role"}</h3>
      <p><strong>Location:</strong> ${job.location || "Unknown"}</p>
      <p><strong>Status:</strong> ${job.status || "Unknown"}</p>
      <p><a href="${job.external_url || "#"}" target="_blank" rel="noopener">View job page</a></p>
    `;
    jobList.appendChild(item);
  });
}

async function loadJobs() {
  setStatus("Loading jobs...");
  try {
    const result = await fetchJson(`${API_BASE}/jobs`);
    renderJobs(result);
    setStatus(`Loaded ${result.length} jobs.`);
  } catch (error) {
    setStatus(`Error: ${error.message}`);
    jobList.innerHTML = "";
  }
}

function showMessage(text, success = true) {
  formMessage.textContent = text;
  formMessage.style.backgroundColor = success ? "#ecfdf5" : "#fee2e2";
  formMessage.style.color = success ? "#065f46" : "#991b1b";
}

candidateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  formMessage.textContent = "";

  const payload = {
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
  };

  try {
    const result = await fetchJson(`${API_BASE}/candidates`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    showMessage(result.message || "Candidate submitted successfully.");
    candidateForm.reset();
  } catch (error) {
    showMessage(`Error: ${error.message}`, false);
  }
});

refreshJobs.addEventListener("click", loadJobs);
loadJobs();
