async function runAction(action) {
  const status = document.getElementById("status");
  if (status) status.innerText = "⏳ Running " + action + "...";

  try {
    const response = await fetch("/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action })
    });

    const result = await response.json();
    if (status) status.innerText = result.message;
  } catch (err) {
    if (status) status.innerText = "❌ Error: " + err;
  }
}
